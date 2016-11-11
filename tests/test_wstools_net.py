#!/usr/bin/env python

############################################################################
# Joshua R. Boverhof, David W. Robertson, LBNL
# See LBNLCopyright for copyright notice!
###########################################################################
import test_wsdl
import unittest


def makeTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(test_wsdl.makeTestSuite("services_by_http"))
    return suite


def test_runner():
    runner = unittest.TextTestRunner()
    runner.run(makeTestSuite())

if __name__ == "__main__":
    test_runner()
