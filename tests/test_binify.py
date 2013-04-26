#!/usr/bin/env python

import unittest

from gdalconst import GA_ReadOnly
from osgeo import ogr, osr

from binify.binify import Binifier

class TestBinify(unittest.TestCase):

    def setUp(self):
        self.args = [
            'tests/test-shapefiles/simple-points.shp',
            'tests/test-shapefiles/simple-points-grid.shp',
            '--overwrite',
            '--suppress-output',
        ]
        self.b = Binifier(self.args)
        self.b.main()

        self.driver = ogr.GetDriverByName('ESRI Shapefile')
        self.in_shapefile = self.driver.Open(
            'tests/test-shapefiles/simple-points-grid.shp',
            GA_ReadOnly
        )
        self.in_layer = self.in_shapefile.GetLayer()

    def test_simple(self):
        extent = self.in_layer.GetExtent()

        self.assertEqual(extent, (
            -0.7789222489017765,
            -0.03954617630398981,
            -0.3489926778373724,
            0.1998517180083852)
        )

    def tearDown(self):
        self.in_shapefile.Destroy()
 
