#!/usr/bin/env python

import math
import os
import sys

try:
    from osgeo.gdalconst import GA_ReadOnly
    from osgeo import ogr, osr
except ImportError:
    from gdalconst import GA_ReadOnly
    import ogr, osr

import progressbar

import cli
from shapegrids import hexagon

class Binifier(object):
    """
    Main binify logic.
    """

    def __init__(self, args=None):
        """
        Get the options from cli or another source (in the future), and
        instantiate a ShapeGrid object.
        """
        self.cli = cli.CLI()
        self.args = self.cli.parse_arguments(args)
        self.grid = hexagon.HexagonGrid()

    def main(self):
        """
        Handle input shapefile, create grid (output) shapefile, do
        summary calculations.
        """
        driver = ogr.GetDriverByName('ESRI Shapefile')
        in_shapefile = driver.Open(self.args.infile, GA_ReadOnly)
        if in_shapefile is None:
            print('Could not open shapefile for read: %s' % self.args.infile)
            sys.exit(1)

        in_layer = in_shapefile.GetLayer()
        if not in_layer.GetGeomType() == ogr.wkbPoint \
                and not self.args.ignore_type:
            print('Input shapefile does not contain a point layer.')
            print('To force computation, use the --ignore-type option.')
            sys.exit(2)

        # If outfile exists and `--overwrite` is set, delete it first
        if os.path.exists(self.args.outfile):
            if not self.args.overwrite:
                print('Output file exists. To overwrite, use the --overwrite \
option.')
                sys.exit(3)
            driver.DeleteDataSource(self.args.outfile)

        out_shapefile = driver.CreateDataSource(self.args.outfile)
        out_layer = out_shapefile.CreateLayer('grid', geom_type=ogr.wkbPolygon)
        field_defn = ogr.FieldDefn('COUNT', ogr.OFTInteger)
        out_layer.CreateField(field_defn)

        # Write .prj file for output shapefile
        spatial_ref = in_layer.GetSpatialRef()
        with open(self.args.outfile[:-4] + '.prj', 'w') as proj_file:
            proj_file.write(spatial_ref.ExportToWkt())

        extent = in_layer.GetExtent()
        self.columns, self.rows = self.grid.create_grid(out_layer, extent,
                num_across=self.args.num_across)
        self.count_intersections(out_layer, in_layer)

        if self.args.exclude_empty:
            self.remove_empty_shapes(out_layer)

        in_shapefile.Destroy()
        out_shapefile.Destroy()

    def count_intersections(self, target, source):
        """
        Counts the number of points in `source` that intersect each polygon of
        `target`.
        """

        # TODO add this code back
        # Set up progress bar

        polygons = []

        another_polygon = True
        while (another_polygon):
            polygon = target.GetNextFeature()
            if polygon:
                poly_geom = polygon.GetGeometryRef()
                poly_points = poly_geom.Boundary().GetPoints()
                # TODO This is very hexagon-specific
                poly_extent = (
                    (
                        poly_points[5][0], # West extent
                        poly_points[0][1], # North extent
                    ),
                    (
                        poly_points[2][0], # East extent
                        poly_points[3][1], # South extent
                    ),
                )
                polygons.append([
                    polygon.GetFID(),
                    poly_extent,
                ])
                polygon.Destroy()
            else:
                another_polygon = False
                target.ResetReading()

        # Sort from top to bottom, and then (primarily) by left to right
        s = sorted(polygons, key=lambda poly: poly[1][0][0])
        polygons_sorted = sorted(s, key=lambda poly: 0 - poly[1][0][1])

        # TODO fix this in column counting
        #self.columns = self.columns * 2
        print ''
        print self.columns
        print self.rows
        print ''

        target_extent = target.GetExtent()
        target_width = target_extent[1] - target_extent[0]
        array_index_width = target_width / self.columns

        target_height = target_extent[3] - target_extent[2]
        array_index_height = target_height / self.rows

        another_point = True
        while (another_point):
            point = source.GetNextFeature()
            if point:
                point_geom = point.GetGeometryRef()
                point_points = point_geom.GetPoint_2D()

                first_index = int(math.floor((point_points[0] - target_extent[0]) / array_index_width))

                second_index = int(math.floor((target_extent[3] - point_points[1]) / array_index_height))

                index = (3 * second_index) + (first_index / 2)
                fid = polygons_sorted[index][0]
                print fid
                
                # `strict_columns` is the number of polygons in each strict
                # column (i.e. considering offset polygons their own column)
                strict_columns = self.columns / 2

                # The intersection does not necessarily occur in that polygon,
                # so we'll also check the surrounding polygons.
                fids_to_check = []
                fids_to_check.append(fid)
                fids_to_check.append(fid + strict_columns)
                fids_to_check.append(fid + strict_columns - 1)
                fids_to_check.append(fid - strict_columns)
                fids_to_check.append(fid - strict_columns - 1)

                for fid in fids_to_check:
                    if fid >= 0 and fid <= len(polygons_sorted) - 1:
                        poly = target.GetFeature(fid)
                        if poly:
                            poly_geom = poly.GetGeometryRef()
                            print poly_geom
                            if point_geom.Intersects(poly_geom):
                                print 'intersection!'
                                print ''
                                count = poly.GetFieldAsInteger('COUNT')
                                poly.SetField('COUNT', count + 1)
                                target.SetFeature(poly)
                                break
                            else:
                                print 'no intersection'
                            print ''
                            poly.Destroy()

            else:
                another_point = False
                source.ResetReading()

    def remove_empty_shapes(self, target):
        """
        Remove any shapes that ended up binning zero points.
        """
        another_polygon = True
        while (another_polygon):
            polygon = target.GetNextFeature()
            if polygon:
                count = polygon.GetFieldAsInteger('COUNT')
                if count == 0:
                    target.DeleteFeature(polygon.GetFID())
                target.SetFeature(polygon)
                polygon.Destroy()
            else:
                another_polygon = False
                target.ResetReading()

def launch_new_instance():
    """
    Launch an instance of Binifier.

    This is the entry function of the command-line tool `binify`.
    """
    binifier = Binifier()
    binifier.main()

if __name__ == '__main__':
    launch_new_instance()

