#!/usr/bin/env python

import os
import sys

from osgeo import ogr
from gdalconst import GA_ReadOnly

import cli
from binshapes import hexagon

class Binifier(object):
    """
    Main binify logic.
    """

    def __init__(self):
        """
        Get the options from cli or another source (in the future), and
        instantiate a ShapeGrid object.
        """
        self.cli = cli.CLI()
        self.args = self.cli.parse_arguments()
        self.grid = hexagon.HexagonGrid()

    def main(self):
        """
        Handle input shapefile, create grid (output) shapefile, do
        summary calculations.
        """
        driver = ogr.GetDriverByName('ESRI Shapefile')
        in_shapefile = driver.Open(self.args.infile, GA_ReadOnly)
        if in_shapefile is None:
            print('Could not open shapefile for read: %s' % filename)
            sys.exit(1)
        in_layer = in_shapefile.GetLayer()
        extent = in_layer.GetExtent()

        # If outfile exists, delete it first
        if os.path.exists(self.args.outfile):
            driver.DeleteDataSource(self.args.outfile)

        out_shapefile = driver.CreateDataSource(self.args.outfile)
        out_layer = out_shapefile.CreateLayer('grid', geom_type=ogr.wkbPolygon)
        field_defn = ogr.FieldDefn('COUNT', ogr.OFTInteger)
        out_layer.CreateField(field_defn)

        self.grid.create_grid(out_layer, extent,
                num_across=self.args.num_across)
        self.count_intersections(out_layer, in_layer)

        in_shapefile.Destroy()
        out_shapefile.Destroy()

    def count_intersections(self, target, source):
        """
        Counts the number of points in `source` that intersect each polygon of
        `target`.
        """
        another_point = True
        while (another_point):
            point = source.GetNextFeature()
            if point:
                point_geom = point.GetGeometryRef()
                another_polygon = True
                while (another_polygon):
                    polygon = target.GetNextFeature()
                    if polygon:
                        poly_geom = polygon.GetGeometryRef()
                        if point_geom.Intersects(poly_geom):
                            # Intersection
                            count = polygon.GetFieldAsInteger('COUNT')
                            polygon.SetField('COUNT', count + 1)
                            target.SetFeature(polygon)
                        polygon.Destroy()
                    else:
                        another_polygon = False
                        target.ResetReading()
                point.Destroy()
            else:
                another_point = False
                source.ResetReading()

def launch_new_instance():
    """
    Launch an instance of Binifier.

    This is the entry function of the command-line tool `binify`.
    """
    binifier = Binifier()
    binifier.main()

if __name__ == '__main__':
    launch_new_instance()

