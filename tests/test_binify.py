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
        self.out_shapefile = self.driver.Open(
            'tests/test-shapefiles/simple-points-grid.shp',
            GA_ReadOnly
        )
        self.out_layer = self.out_shapefile.GetLayer()

    def test_extent(self):
        extent = self.out_layer.GetExtent()
        self.assertEqual(extent, (
            -0.7789222489017765,
            -0.03954617630398981,
            -0.3489926778373724,
            0.1998517180083852)
        )

    def test_count(self):
        count = 0
        another_feature = True
        while (another_feature):
            feature = self.out_layer.GetNextFeature()
            if feature:
                count += feature.GetFieldAsInteger('COUNT')
            else:
                another_feature = False
        self.assertEqual(count, 10)

    def tearDown(self):
        self.out_shapefile.Destroy()

