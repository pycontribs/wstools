#!/usr/bin/env python

############################################################################
# Joshua R. Boverhof, David W. Robertson, LBNL
# See LBNLCopyright for copyright notice!
###########################################################################
"""Unittests."""
import inspect
import os
import sys
import unittest
cmd_folder = os.path.abspath(os.path.join(os.path.split(inspect.getfile(
    inspect.currentframe()))[0], ".."))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
from wstools.TimeoutSocket import TimeoutError  # noqa E402
from wstools.Utility import DOM  # noqa E402
from wstools.WSDLTools import WSDLReader  # noqa E402
try:
    import configparser
except ImportError:
    from six.moves import configparser

cwd = 'tests'

# that's for tox/pytest
nameGenerator = None


def makeTestSuite(section='services_by_file'):
    """makeTestSuite."""
    global nameGenerator

    cp, numTests = setUpOptions(section)
    nameGenerator = getOption(cp, section)
    suite = unittest.TestSuite()
    for i in range(0, numTests):
        suite.addTest(unittest.makeSuite(WSDLToolsTestCase, 'test_'))
    return suite


class WSDLToolsTestCase(unittest.TestCase):
    """"""

    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName)

    def setUp(self):
        makeTestSuite()
        if hasattr(nameGenerator, '__next__'):
            self.path = nameGenerator.__next__()
        else:
            self.path = nameGenerator.next()
        # print(self.path)
        sys.stdout.flush()

    def __str__(self):
        teststr = unittest.TestCase.__str__(self)
        if hasattr(self, "path"):
            return "%s: %s" % (teststr, self.path)
        else:
            return "%s" % (teststr)

    def checkWSDLCollection(self, tag_name, component, key='name'):
        if self.wsdl is None:
            return
        definition = self.wsdl.document.documentElement
        version = DOM.WSDLUriToVersion(definition.namespaceURI)
        nspname = DOM.GetWSDLUri(version)
        for node in DOM.getElements(definition, tag_name, nspname):
            name = DOM.getAttr(node, key)
            comp = component[name]  # noqa F841
            self.failUnlessEqual(eval('comp.%s' % key), name)

    def checkXSDCollection(self, tag_name, component, node, key='name'):
        for cnode in DOM.getElements(node, tag_name):
            name = DOM.getAttr(cnode, key)
            component[name]

    def test_all(self):
        try:
            if self.path[:7] == 'http://':
                self.wsdl = WSDLReader().loadFromURL(self.path)
            else:
                self.wsdl = WSDLReader().loadFromFile('tests/' + self.path)

        except TimeoutError:
            print("connection timed out")
            sys.stdout.flush()
            return
        except Exception:
            self.path = self.path + ": load failed, unable to start"
            raise

        try:
            self.checkWSDLCollection('service', self.wsdl.services)
        except Exception:
            self.path = self.path + ": wsdl.services"
            raise

        try:
            self.checkWSDLCollection('message', self.wsdl.messages)
        except Exception:
            self.path = self.path + ": wsdl.messages"
            raise

        try:
            self.checkWSDLCollection('portType', self.wsdl.portTypes)
        except Exception:
            self.path = self.path + ": wsdl.portTypes"
            raise

        try:
            self.checkWSDLCollection('binding', self.wsdl.bindings)
        except Exception:
            self.path = self.path + ": wsdl.bindings"
            raise

        try:
            self.checkWSDLCollection('import', self.wsdl.imports,
                                     key='namespace')
        except Exception:
            self.path = self.path + ": wsdl.imports"
            raise

        try:
            for key in self.wsdl.types.keys():
                schema = self.wsdl.types[key]
                self.failUnlessEqual(key, schema.getTargetNamespace())

            definition = self.wsdl.document.documentElement
            version = DOM.WSDLUriToVersion(definition.namespaceURI)
            nspname = DOM.GetWSDLUri(version)
            for node in DOM.getElements(definition, 'types', nspname):
                for snode in DOM.getElements(node, 'schema'):
                    tns = DOM.findTargetNS(snode)
                    schema = self.wsdl.types[tns]
                    self.schemaAttributesDeclarations(schema, snode)
                    self.schemaAttributeGroupDeclarations(schema, snode)
                    self.schemaElementDeclarations(schema, snode)
                    self.schemaTypeDefinitions(schema, snode)
        except Exception:
            self.path = self.path + ": wsdl.types"
            raise

        if self.wsdl.extensions:
            print('No check for WSDLTools(%s) Extensions:' % (self.wsdl.name))
            for ext in self.wsdl.extensions:
                print('\t', ext)

    def schemaAttributesDeclarations(self, schema, node):
        self.checkXSDCollection('attribute', schema.attr_decl, node)

    def schemaAttributeGroupDeclarations(self, schema, node):
        self.checkXSDCollection('group', schema.attr_groups, node)

    def schemaElementDeclarations(self, schema, node):
        self.checkXSDCollection('element', schema.elements, node)

    def schemaTypeDefinitions(self, schema, node):
        self.checkXSDCollection('complexType', schema.types, node)
        self.checkXSDCollection('simpleType', schema.types, node)


def setUpOptions(section):
    cp = configparser.ConfigParser()
    cp.optionxform = str
    cp.read(cwd + '/config.txt')
    if not cp.sections():
        print('fatal error:  configuration file config.txt not present')
        sys.exit(0)
    if not cp.has_section(section):
        print('%s section not present in configuration file, exiting' % section)
        sys.exit(0)
    return cp, len(cp.options(section))


def getOption(cp, section):
    for name, value in cp.items(section):
        yield value
