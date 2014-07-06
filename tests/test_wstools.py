#!/usr/bin/env python

############################################################################
# Joshua R. Boverhof, David W. Robertson, LBNL
# See LBNLCopyright for copyright notice!
###########################################################################

import unittest
import test_wsdl

def makeTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(test_wsdl.makeTestSuite("services_by_file"))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(makeTestSuite())
