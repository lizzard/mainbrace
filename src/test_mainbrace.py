#!/usr/bin/env python
##
# test_mainbrace.py
###
"""test_mainbrace.py

"""

__version__ = "0.1"
__author__ = "Danny O'Brien <http://www.spesh.com/danny/>"
__copyright__ = "Copyright Danny O'Brien"
__contributors__ = None
__license__ = "GPL"

import doctest
import unittest
import mainbrace

class mainbraceTest(unittest.TestCase):
    def test_can_load_S57_file(self):
        a = mainbrace.S57_wrapper('../data/ENC_ROOT/US5CA16M/US5CA16M.000')
    def test_cant_load_fake_file(self):
        a = mainbrace.S57_wrapper('../data/fakefile.000')
        self.assertRaises(Exception, a.load)

    def test_is_this_an_S57_file(self):
        a = mainbrace.S57_wrapper('../data/ENC_ROOT/US5CA16M/US5CA16M.000')
        self.assert_(a.layer('DSID'),'DSID layer does not exist')

    def test_is_this_NOT_an_S57_file(self):
        a = mainbrace.S57_wrapper('../data/ENC_ROOT/US5CA16M/layers.txt')
        self.failIf(a.layer('DSID'),'Non S57 file seems to have DSID layer!')




if __name__ == '__main__':
    import __main__
    try:
        suite = doctest.DocTestSuite()
    except ValueError:
        suite = unittest.TestLoader().loadTestsFromModule(__main__)
    else:
        suite.addTest(unittest.TestLoader().loadTestsFromModule(__main__))
    unittest.TextTestRunner(verbosity=1).run(suite)

