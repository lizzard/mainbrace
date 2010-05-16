#!/usr/bin/env python
##
# convert_s57_to_osm.py
###
"""convert_s57_to_osm.py

"""

__version__ = "0.1"
__author__ = "Danny O'Brien <http://www.spesh.com/danny/>"
__copyright__ = "Copyright Danny O'Brien"
__contributors__ = None
__license__ = "GPL v3"

from osgeo import ogr

def get_example_s57_buoy():
    data_source = ogr.Open("../../data/ENC_ROOT/US5CA16M/US5CA16M.000")
    layer = data_source.GetLayer('BOYSPP')
    feature = layer.GetFeature(637)
    return feature


def s57_to_osm(feature, layer_name=None):
    osm_tags = {}
    # get hold of what layer this feature is in
    # if it's BOYSPP, create seamark:buoy, seamark=buoy, buoy=special_purpose
    if layer_name == 'BOYSPP':
        osm_tags['seamark'] = 'buoy'
        osm_tags['buoy'] = 'special_purpose'
    
    # grab LNAM, stuff into buoy:ref
    osm_tags['buoy:ref'] = feature.LNAM
    #
    # grab BOYSHIP=2, look up in some mystery lookup, set buoy:shape=can
 
    boyshp_values = [None, 'conical','can', 'spherical', 'pillar', 'spar', 'barrel', 'super-buoy', 'ice buoy']  
    osm_tags['buoy:shape'] = boyshp_values[feature.BOYSHP]

    # grab CATSPM=

    # CATSPM = 27     seamark:buoy_special_purpose:category=general_warning_mark
    catspm_values = []
    osm_tags['seamark:buoy_special_purpose:category'] = catspm_values(feature.CATSPM)
    # OBJNAM=SF Airport  Buoy N         name=(name)       seamark:name=(name)
    osm_tags['name'] = feature.OBJNAM
    osm_tags['seamark:name'] = feature.OBJNAM
    # STATUS=8      buoy:status=private
    status_values = []
    osm_tags['buoy:status'] = status_values(feature.STATUS)
    # SCAMIN=120000   buoy:scale_minimum
    osm_tags['buoy:scale_minimum']=feature.SCAMIN
    # SORDAT=20040914       source:date=20040914
    # How are dates stored in open seamap??
    # POINT (-122.381666999999993 37.640278000000002)    latitude=  37.640278000000002      longitude=-122.381666999999993
    
    return osm_tags

def main(args):
    # Get a particular feature from the S-57 file
    s57_buoy = get_example_s57_buoy() # TODO

    # Convert that buoy data into tags
    tags = s57_to_osm(s57_buoy, layer_name = 'BOYSPP')

    # print them (check them with what we expect)
    print tags
    # send 'em to OSM via the OSMApi

    

import sys, getopt
class Main():
    """ Encapsulates option handling. Subclass to add new options,
        add 'handle_x' method for an -x option,
        add 'handle_xlong' method for an --xlong option
        help (-h, --help) should be automatically created from module
        docstring and handler docstrings.
        test (-t, --test) will run all docstring and unittests it finds
        """
    class Usage(Exception):
        """ Use this to generate a Usage message """
        def __init__(self, msg):
            self.msg = msg
    def __init__(self):
        handlers  = [i[7:] for i in dir(self) if i.startswith('handle_') ]
        self.shortopts = ''.join([i for i in handlers if len(i) == 1])
        self.longopts = [i for i in handlers if (len(i) > 1)]
    def handler(self, option):
        i = 'handle_%s' % option.lstrip('-')
        if hasattr(self, i):
            return getattr(self, i)
    def default_main(self, args):
        print sys.argv[0], " called with ", args
    def handle_help(self, v):
        """ Shows this message """
        print sys.modules.get(__name__).__doc__
        descriptions = {}
        for i in list(self.shortopts) + self.longopts:
            d = self.handler(i).__doc__
            if d in descriptions:
                descriptions[d].append(i)
            else:
                descriptions[d] = [i]
        for d, opts in descriptions.iteritems():
            for i in opts:
                if len(i) == 1:
                    print '-%s' % i,
                else:
                    print '--%s' % i,
            print 
            print d
        sys.exit(0)
    handle_h = handle_help

    def handle_test(self, v):
        """ Runs test suite for file """
        import doctest
        import unittest
        suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules.get(__name__))
        suite.addTest(doctest.DocTestSuite())
        runner = unittest.TextTestRunner()
        runner.run(suite)
        sys.exit(0)
    handle_t = handle_test

    def run(self, main= None, argv=None):
        """ Execute main function, having stripped out options and called the
        responsible handler functions within the class. Main defaults to
        listing the remaining arguments.
        """
        if not callable(main):
            main = self.default_main
        if argv is None:
            argv = sys.argv
        try:
            try:
                opts, args = getopt.getopt(argv[1:], self.shortopts, self.longopts)
            except getopt.error, msg:
                raise self.Usage(msg)
            for o, a in opts:
                (self.handler(o))(a)
            return main(args) 
        except self.Usage, err:
            print >>sys.stderr, err.msg
            self.handle_help(None)
            return 2

if __name__ == "__main__":
    sys.exit(Main().run(main) or 0)

