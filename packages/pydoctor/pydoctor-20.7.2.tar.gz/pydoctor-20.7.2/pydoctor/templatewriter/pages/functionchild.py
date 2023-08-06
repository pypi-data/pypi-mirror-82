from __future__ import print_function

import ast

import astor
from pydoctor.templatewriter import util
from pydoctor.templatewriter.pages import signature
from twisted.web.template import Element, XMLFile, renderer, tags


class FunctionChild(Element):

    loader = XMLFile(util.templatefilepath('function-child.html'))

    def __init__(self, docgetter, ob, functionExtras):
        self.docgetter = docgetter
        self.ob = ob
        self._functionExtras = functionExtras

    @renderer
    def class_(self, request, tag):
        class_ = self.ob.css_class
        if self.ob.parent is not self.ob:
            class_ = 'base' + class_
        return class_

    @renderer
    def functionAnchor(self, request, tag):
        return self.ob.fullName()

    @renderer
    def shortFunctionAnchor(self, request, tag):
        return self.ob.name

    @renderer
    def decorator(self, request, tag):

        decorators = []

        if self.ob.decorators:
            for dec in self.ob.decorators:
                if isinstance(dec, ast.Call):
                    if isinstance(dec.func, ast.Name):
                        fn = self.ob.expandName(dec.func.id)
                        # We don't want to show the deprecated decorator, it shows up
                        # as an infobox
                        if fn == "twisted.python.deprecate.deprecated":
                            break

                decorators.append(astor.to_source(dec).strip())

        if decorators:
            decorator = [('@' + dec, tags.br()) for dec in decorators]
        else:
            decorator = ()

        return decorator

    @renderer
    def functionName(self, request, tag):
        return [self.ob.name, '(', signature(self.ob.argspec), '):']

    @renderer
    def sourceLink(self, request, tag):
        if self.ob.sourceHref:
            return tag.fillSlots(sourceHref=self.ob.sourceHref)
        else:
            return ()

    @renderer
    def functionExtras(self, request, tag):
        return self._functionExtras

    @renderer
    def functionBody(self, request, tag):
        return self.docgetter.get(self.ob)

    @renderer
    def functionDeprecated(self, request, tag):
        if hasattr(self.ob, "_deprecated_info"):
            return (tags.div(self.ob._deprecated_info, role="alert", class_="deprecationNotice alert alert-warning"),)
        else:
            return ()
