"""Core pydoctor objects.

The two core objects are L{Documentable} and L{System}.  Instances of
(subclasses of) L{Documentable} represent the documentable 'things' in the
system being documented.  An instance of L{System} represents the whole system
being documented -- a System is a bad of Documentables, in some sense.
"""

from __future__ import print_function, unicode_literals

import datetime
import imp
import inspect
import os
import platform
import sys
import types
from collections import OrderedDict
from enum import Enum

from pydoctor.sphinx import SphinxInventory
from six.moves import builtins

# originally when I started to write pydoctor I had this idea of a big
# tree of Documentables arranged in an almost arbitrary tree.
#
# this was misguided.  the tree structure is important, to be sure,
# but the arrangement of the tree is far from arbitrary and there is
# at least some code that now relies on this.  so here's a list:
#
#   Packages can contain Packages and Modules
#   Modules can contain Functions and Classes
#   Classes can contain Functions (in this case they get called Methods) and
#       Classes
#   Functions can't contain anything.


_string_lineno_is_end = sys.version_info < (3,8) \
                    and platform.python_implementation() != 'PyPy'
"""True iff the 'lineno' attribute of an AST string node points to the last
line in the string, rather than the first line.
"""


class DocLocation(Enum):
    OWN_PAGE = 1
    PARENT_PAGE = 2
    # Nothing uses this yet.  Parameters will one day.
    #UNDER_PARENT_DOCSTRING = 3


class Documentable(object):
    """An object that can be documented.

    The interface is a bit ridiculously wide.

    @ivar docstring: The object's docstring.  But also see docsources.
    @ivar system: The system the object is part of.
    @ivar parent: ...
    @ivar parentMod: ...
    @ivar name: ...
    @ivar documentation_location: ...
    @ivar sourceHref: ...
    @ivar kind: ...
    """
    documentation_location = DocLocation.OWN_PAGE
    docstring = None
    docstring_lineno = 0
    linenumber = 0
    sourceHref = None

    @property
    def css_class(self):
        """A short, lower case description for use as a CSS class in HTML."""
        class_ = self.kind.lower().replace(' ', '')
        if self.privacyClass is PrivacyClass.PRIVATE:
            class_ += ' private'
        return class_

    def __init__(self, system, name, parent=None):
        self.system = system
        self.name = name
        self.parent = parent
        self.parentMod = None
        self.setup()
        if not isinstance(self, Package):
            self.doctarget = self

    def setup(self):
        self.contents = OrderedDict()

    def setDocstring(self, node):
        doc = node.s
        lineno = node.lineno
        if _string_lineno_is_end:
            # In older CPython versions, the AST only tells us the end line
            # number and we must approximate the start line number.
            # This approximation is correct if the docstring does not contain
            # explicit newlines ('\n') or joined lines ('\' at end of line).
            lineno -= doc.count('\n')

        # Leading blank lines are stripped by cleandoc(), so we must
        # return the line number of the first non-blank line.
        for ch in doc:
            if ch == '\n':
                lineno += 1
            elif not ch.isspace():
                break

        self.docstring = inspect.cleandoc(doc)
        self.docstring_lineno = lineno

    def setLineNumber(self, lineno):
        if not self.linenumber:
            self.linenumber = lineno
            parentMod = self.parentMod
            if parentMod is not None:
                parentSourceHref = parentMod.sourceHref
                if parentSourceHref:
                    self.sourceHref = '%s#L%d' % (parentSourceHref, lineno)

    def fullName(self):
        parent = self.parent
        if parent is not None:
            if (parent.parent and isinstance(parent.parent, Package)
                and isinstance(parent, Module)
                and parent.name == '__init__'):
                prefix = parent.parent.fullName() + '.'
            else:
                prefix = parent.fullName() + '.'
        else:
            prefix = ''
        return prefix + self.name

    def __repr__(self):
        return "%s %r"%(self.__class__.__name__, self.fullName())

    def docsources(self):
        """Objects that can be considered as a source of documentation.

        The motivating example for having multiple sources is looking at a
        superclass' implementation of a method for documentation for a
        subclass'.
        """
        yield self


    def reparent(self, new_parent, new_name):
        # this code attempts to preserve "rather a lot" of
        # invariants assumed by various bits of pydoctor
        # and that are of course not written down anywhere
        # :/
        self._handle_reparenting_pre()
        old_parent = self.parent
        old_name = self.name
        self.parent = self.parentMod = new_parent
        self.name = new_name
        self._handle_reparenting_post()
        del old_parent.contents[old_name]
        old_parent._localNameToFullName_map[old_name] = self.fullName()
        new_parent.contents[new_name] = self
        self._handle_reparenting_post()

    def _handle_reparenting_pre(self):
        del self.system.allobjects[self.fullName()]
        for o in self.contents.values():
            o._handle_reparenting_pre()

    def _handle_reparenting_post(self):
        self.system.allobjects[self.fullName()] = self
        for o in self.contents.values():
            o._handle_reparenting_post()

    def _localNameToFullName(self, name):
        raise NotImplementedError(self._localNameToFullName)

    def expandName(self, name):
        """Return a fully qualified name for the possibly-dotted `name`.

        To explain what this means, consider the following modules:

        mod1.py::

            from external_location import External
            class Local(object):
                pass

        mod2.py::

            from mod1 import External as RenamedExternal
            import mod1 as renamed_mod
            class E:
                pass

        In the context of mod2.E, expandName("RenamedExternal") should be
        "external_location.External" and expandName("renamed_mod.Local")
        should be "mod1.Local". """
        parts = name.split('.')
        obj = self
        for i, p in enumerate(parts):
            full_name = obj._localNameToFullName(p)
            obj = self.system.objForFullName(full_name)
            if obj is None:
                break
        remaning = parts[i+1:]
        return '.'.join([full_name] + remaning)

    def resolveName(self, name):
        """Return the object named by "name" (using Python's lookup rules) in
        this context, if any is known to pydoctor."""
        return self.system.objForFullName(self.expandName(name))

    @property
    def privacyClass(self):
        """How visible this object should be.

        @rtype: a member of the L{PrivacyClass} class/enum.
        """
        return self.system.privacyClass(self)

    @property
    def isVisible(self):
        """Is this object is so private as to be not shown at all?

        This is just a simple helper which defers to self.privacyClass.
        """
        return self.privacyClass is not PrivacyClass.HIDDEN

    @property
    def module(self):
        """This object's L{Module}.

        For modules, this returns the object itself, otherwise
        the module containing the object is returned.
        """
        parentMod = self.parentMod
        assert parentMod is not None
        return parentMod

    def report(self, descr, section='parsing', lineno_offset=0):
        """Log an error or warning about this documentable object."""

        if section == 'docstring':
            linenumber = self.docstring_lineno
        else:
            linenumber = self.linenumber
        if linenumber:
            linenumber += lineno_offset
        elif lineno_offset and self.module is self:
            linenumber = lineno_offset
        else:
            linenumber = '???'

        self.system.msg(
            section,
            '%s:%s: %s' % (self.module.description, linenumber, descr),
            thresh=-1)


class Package(Documentable):
    kind = "Package"
    def docsources(self):
        yield self.contents['__init__']
    @property
    def doctarget(self):
        return self.contents['__init__']
    @property
    def module(self):
        return self.contents['__init__']
    @property
    def state(self):
        return self.contents['__init__'].state

    def _localNameToFullName(self, name):
        if name in self.contents:
            o = self.contents[name]
            return o.fullName()
        else:
            return self.contents['__init__']._localNameToFullName(name)


class ProcessingState(Enum):
    UNPROCESSED = 0
    PROCESSING = 1
    PROCESSED = 2


class CanContainImportsDocumentable(Documentable):
    def setup(self):
        super(CanContainImportsDocumentable, self).setup()
        self._localNameToFullName_map = {}


class Module(CanContainImportsDocumentable):
    kind = "Module"
    state = ProcessingState.UNPROCESSED

    def setup(self):
        super(Module, self).setup()
        self.all = None

    def _localNameToFullName(self, name):
        if name in self.contents:
            o = self.contents[name]
            return o.fullName()
        elif name in self._localNameToFullName_map:
            return self._localNameToFullName_map[name]
        elif name in builtins.__dict__:
            return name
        else:
            return name

    @property
    def module(self):
        return self

    @property
    def description(self):
        """A string describing this module to the user.

        If this module's code was read from a file, this returns
        its file path. In other cases, such as during unit testing,
        the module's full name is returned.
        """
        filepath = getattr(self, 'filepath', None)
        return self.fullName() if filepath is None else filepath


class Class(CanContainImportsDocumentable):
    kind = "Class"
    def setup(self):
        super(Class, self).setup()
        self.rawbases = []
        self.subclasses = []

    def allbases(self, include_self=False):
        if include_self:
            yield self
        for b in self.baseobjects:
            if b is None:
                continue
            for b2 in b.allbases(True):
                yield b2
    def _localNameToFullName(self, name):
        if name in self.contents:
            o = self.contents[name]
            return o.fullName()
        elif name in self._localNameToFullName_map:
            return self._localNameToFullName_map[name]
        else:
            return self.parent._localNameToFullName(name)


class Inheritable(Documentable):
    documentation_location = DocLocation.PARENT_PAGE

    def docsources(self):
        yield self
        if not isinstance(self.parent, Class):
            return
        for b in self.parent.allbases(include_self=False):
            if self.name in b.contents:
                yield b.contents[self.name]

    def _localNameToFullName(self, name):
        return self.parent._localNameToFullName(name)

class Function(Inheritable):
    kind = "Function"

    def setup(self):
        super(Function, self).setup()
        if isinstance(self.parent, Class):
            self.kind = "Method"

class Attribute(Inheritable):
    kind = "Attribute"


class PrivacyClass(Enum):
    """L{Enum} containing values indicating how private an object should be.

    @cvar HIDDEN: Don't show the object at all.
    @cvar PRIVATE: Show, but de-emphasize the object.
    @cvar VISIBLE: Show the object as normal.
    """

    HIDDEN = 0
    PRIVATE = 1
    VISIBLE = 2



class System(object):
    """A collection of related documentable objects.

    PyDoctor documents collections of objects, often the contents of a
    package.
    """

    Class = Class
    Module = Module
    Package = Package
    Function = Function
    Attribute = Attribute
    # not done here for circularity reasons:
    #defaultBuilder = astbuilder.ASTBuilder
    sourcebase = None

    def __init__(self, options=None):
        self.allobjects = OrderedDict()
        self.rootobjects = []
        self.warnings = {}
        self.packages = []

        if options:
            self.options = options
        else:
            from pydoctor.driver import parse_args
            self.options, _ = parse_args([])
            self.options.verbosity = 3

        self.abbrevmapping = {}
        self.projectname = 'my project'

        self.docstring_syntax_errors = set()
        """FullNames of objects for which the docstring failed to parse."""

        self.verboselevel = 0
        self.needsnl = False
        self.once_msgs = set()
        self.unprocessed_modules = set()
        self.module_count = 0
        self.processing_modules = []
        self.buildtime = datetime.datetime.now()
        self.intersphinx = SphinxInventory(logger=self.msg)

    def verbosity(self, section=None):
        if isinstance(section, str):
            section = (section,)
        delta = max([self.options.verbosity_details.get(sect, 0) for sect in section])
        return self.options.verbosity + delta

    def progress(self, section, i, n, msg):
        if n is None:
            i = str(i)
        else:
            i = '%s/%s'%(i,n)
        if self.verbosity(section) == 0 and sys.stdout.isatty():
            print('\r'+i, msg, end='')
            sys.stdout.flush()
            if i == n:
                self.needsnl = False
                print()
            else:
                self.needsnl = True

    def msg(self, section, msg, thresh=0, topthresh=100, nonl=False, wantsnl=True, once=False):
        if once:
            if (section, msg) in self.once_msgs:
                return
            else:
                self.once_msgs.add((section, msg))
        if thresh <= self.verbosity(section) <= topthresh:
            if self.needsnl and wantsnl:
                print()
            print(msg, end='')
            if nonl:
                self.needsnl = True
                sys.stdout.flush()
            else:
                self.needsnl = False
                print('')

    def objForFullName(self, fullName):
        return self.allobjects.get(fullName)

    def _warning(self, current, type, detail):
        if current is not None:
            fn = current.fullName()
        else:
            fn = '<None>'
        if self.options.verbosity > 0:
            print(fn, type, detail)
        self.warnings.setdefault(type, []).append((fn, detail))

    def objectsOfType(self, cls):
        """Iterate over all instances of C{cls} present in the system. """
        for o in self.allobjects.values():
            if isinstance(o, cls):
                yield o

    def privacyClass(self, ob):
        if ob.kind is None:
            return PrivacyClass.HIDDEN
        if ob.name.startswith('_') and \
               not (ob.name.startswith('__') and ob.name.endswith('__')):
            return PrivacyClass.PRIVATE
        return PrivacyClass.VISIBLE

    def addObject(self, obj):
        """Add C{object} to the system."""
        fullName = obj.fullName()
        if obj.parent and obj.parent.fullName() != fullName:
            obj.parent.contents[obj.name] = obj
        else:
            self.rootobjects.append(obj)
        if fullName in self.allobjects:
            self.handleDuplicate(obj)
        else:
            self.allobjects[fullName] = obj

    # if we assume:
    #
    # - that svn://divmod.org/trunk is checked out into ~/src/Divmod
    #
    # - that http://divmod.org/trac/browser/trunk is the trac URL to the
    #   above directory
    #
    # - that ~/src/Divmod/Nevow/nevow is passed to pydoctor as an
    #   "--add-package" argument
    #
    # we want to work out the sourceHref for nevow.flat.ten.  the answer
    # is http://divmod.org/trac/browser/trunk/Nevow/nevow/flat/ten.py.
    #
    # we can work this out by finding that Divmod is the top of the svn
    # checkout, and posixpath.join-ing the parts of the filePath that
    # follows that.
    #
    #  http://divmod.org/trac/browser/trunk
    #                          ~/src/Divmod/Nevow/nevow/flat/ten.py

    def setSourceHref(self, mod):
        if self.sourcebase is None:
            mod.sourceHref = None
        else:
            projBaseDir = mod.system.options.projectbasedirectory
            mod.sourceHref = (
                self.sourcebase +
                mod.filepath[len(projBaseDir):])

    def addModule(self, modpath, modname, parentPackage=None):
        mod = self.Module(self, modname, parentPackage)
        self.addObject(mod)
        self.progress(
            "addModule", len(self.allobjects),
            None, "modules and packages discovered")
        mod.filepath = modpath
        self.unprocessed_modules.add(mod)
        self.module_count += 1
        self.setSourceHref(mod)

    def ensureModule(self, module_full_name):
        if module_full_name in self.allobjects:
            return self.allobjects[module_full_name]
        if '.' in module_full_name:
            parent_name, module_name = module_full_name.rsplit('.', 1)
            parent_package = self.ensurePackage(parent_name)
        else:
            parent_package = None
            module_name = module_full_name
        module = self.Module(self, module_name, parent_package)
        self.addObject(module)
        return module

    def ensurePackage(self, package_full_name):
        if package_full_name in self.allobjects:
            return self.allobjects[package_full_name]
        if '.' in package_full_name:
            parent_name, package_name = package_full_name.rsplit('.', 1)
            parent_package = self.ensurePackage(parent_name)
        else:
            parent_package = None
            package_name = package_full_name
        package = self.Package(self, package_name, parent_package)
        self.addObject(package)
        return package

    def _introspectThing(self, thing, parent, parentMod):
        for k, v in thing.__dict__.items():
            if isinstance(v, (types.BuiltinFunctionType,
                              types.FunctionType)):
                f = self.Function(self, k, parent)
                f.parentMod = parentMod
                f.docstring = v.__doc__
                f.decorators = None
                f.argspec = ((), None, None, ())
                self.addObject(f)
            elif isinstance(v, type):
                c = self.Class(self, k, parent)
                c.bases = []
                c.baseobjects = []
                c.rawbases = []
                c.parentMod = parentMod
                c.docstring = v.__doc__
                self.addObject(c)
                self._introspectThing(v, c, parentMod)

    def introspectModule(self, py_mod, module_full_name):
        module = self.ensureModule(module_full_name)
        module.docstring = py_mod.__doc__
        self._introspectThing(py_mod, module, module)

    def addPackage(self, dirpath, parentPackage=None):
        if not os.path.exists(dirpath):
            raise Exception("package path %r does not exist!"
                            %(dirpath,))
        if not os.path.exists(os.path.join(dirpath, '__init__.py')):
            raise Exception("you must pass a package directory to "
                            "addPackage")
        if parentPackage:
            prefix = parentPackage.fullName() + '.'
        else:
            prefix = ''
        package_name = os.path.basename(dirpath)
        package_full_name = prefix + package_name
        package = self.ensurePackage(package_full_name)
        package.filepath = dirpath
        self.setSourceHref(package)
        for fname in sorted(os.listdir(dirpath)):
            fullname = os.path.join(dirpath, fname)
            if os.path.isdir(fullname):
                initname = os.path.join(fullname, '__init__.py')
                if os.path.exists(initname):
                    self.addPackage(fullname, package)
            elif not fname.startswith('.'):
                self.addModuleFromPath(package, fullname)

    def addModuleFromPath(self, package, path):
        for (suffix, mode, type) in imp.get_suffixes():
            if not path.endswith(suffix):
                continue
            module_name = os.path.basename(path[:-len(suffix)])
            if type == imp.C_EXTENSION:
                if not self.options.introspect_c_modules:
                    continue
                if package is not None:
                    module_full_name = "%s.%s" % (
                        package.fullName(), module_name)
                else:
                    module_full_name = module_name
                py_mod = imp.load_module(
                    module_full_name, open(path, 'rb'), path,
                    (suffix, mode, type))
                self.introspectModule(py_mod, module_full_name)
            elif type == imp.PY_SOURCE:
                self.addModule(path, module_name, package)
            break

    def handleDuplicate(self, obj):
        '''This is called when we see two objects with the same
        .fullName(), for example:

        class C:
            if something:
                def meth(self):
                    implementation 1
            else:
                def meth(self):
                    implementation 2

        The default is that the second definition "wins".
        '''
        i = 0
        fullName = obj.fullName()
        while (fullName + ' ' + str(i)) in self.allobjects:
            i += 1
        prev = self.allobjects[fullName]
        self._warning(obj.parent, "duplicate", prev)
        def remove(o):
            del self.allobjects[o.fullName()]
            oc = list(o.contents.values())
            for c in oc:
                remove(c)
        remove(prev)
        prev.name = obj.name + ' ' + str(i)
        def readd(o):
            self.allobjects[o.fullName()] = o
            for c in o.contents.values():
                readd(c)
        readd(prev)
        self.allobjects[fullName] = obj


    def getProcessedModule(self, modname):
        mod = self.allobjects.get(modname)
        if mod is None:
            return None
        if isinstance(mod, Package):
            return self.getProcessedModule(modname + '.__init__').parent
        if not isinstance(mod, Module):
            return None

        if mod.state is ProcessingState.UNPROCESSED:
            self.processModule(mod)

        return mod


    def processModule(self, mod):
        assert mod.state is ProcessingState.UNPROCESSED
        mod.state = ProcessingState.PROCESSING
        if getattr(mod, 'filepath', None) is None:
            return
        builder = self.defaultBuilder(self)
        ast = builder.parseFile(mod.filepath)
        if ast:
            self.processing_modules.append(mod.fullName())
            self.msg("processModule", "processing %s"%(self.processing_modules), 1)
            builder.processModuleAST(ast, mod)
            mod.state = ProcessingState.PROCESSED
            head = self.processing_modules.pop()
            assert head == mod.fullName()
        self.unprocessed_modules.remove(mod)
        self.progress(
            'process',
            self.module_count - len(self.unprocessed_modules),
            self.module_count,
            "modules processed %s warnings"%(
            sum(len(v) for v in self.warnings.values()),))


    def process(self):
        while self.unprocessed_modules:
            mod = next(iter(self.unprocessed_modules))
            self.processModule(mod)


    def fetchIntersphinxInventories(self, cache):
        """
        Download and parse intersphinx inventories based on configuration.
        """
        for url in self.options.intersphinx:
            self.intersphinx.update(cache, url)
