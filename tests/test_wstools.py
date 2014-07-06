#!/usr/bin/env python

############################################################################
# Joshua R. Boverhof, David W. Robertson, LBNL
# See LBNLCopyright for copyright notice!
###########################################################################

import unittest
import test_wsdl


SECTION = 'files'
CONFIG_FILE = 'config.txt'


def makeTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(test_wsdl.makeTestSuite("services_by_file"))
    return suite


def main():
    unittest.main(defaultTest="makeTestSuite")

if __name__ == "__main__":
    main()
