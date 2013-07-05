#!/usr/bin/env python

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

        if self.args.extent:
          extent = self.args.extent
        else:
          extent = in_layer.GetExtent()

        self.grid.create_grid(out_layer, extent,
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
        # Set up progress bar
        num_points = source.GetFeatureCount()
        if not self.args.suppress_output:
            pbar = progressbar.ProgressBar(
                widgets=[
                    'Binning: ',
                    progressbar.Percentage(),
                    progressbar.Bar()
                ],
                maxval=num_points
            )
            pbar.start()

        pbar_count = 0
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
            if not self.args.suppress_output:
                # Update progress bar
                pbar.update(pbar_count)
                pbar_count = pbar_count + 1
        if not self.args.suppress_output:
            pbar.finish()

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

