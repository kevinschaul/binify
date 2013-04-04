#!/usr/bin/env python

import argparse
import math
import os
import sys

from osgeo import ogr
from gdalconst import *

def parse_arguments():
    """
    Implement command-line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('infile',
            help='A point shapefile to create bins from.')
    parser.add_argument('outfile',
            help='A shapefile to write to. Will be created if it does not exist.')
    return parser.parse_args()

def main():
    args = parse_arguments()

    driver = ogr.GetDriverByName('ESRI Shapefile')
    in_shapefile = driver.Open(args.infile, GA_ReadOnly)
    if in_shapefile is None:
        print('Could not open shapefile for read: %s' % filename)
        sys.exit(1)
    in_layer = in_shapefile.GetLayer()
    extent = in_layer.GetExtent()

    # If outfile exists, delete it first
    if os.path.exists(args.outfile):
        driver.DeleteDataSource(args.outfile)

    out_shapefile = driver.CreateDataSource(args.outfile)
    out_layer = out_shapefile.CreateLayer('grid', geom_type=ogr.wkbPolygon)
    field_defn = ogr.FieldDefn('id', ogr.OFTInteger)
    out_layer.CreateField(field_defn)

    create_grid(out_layer, extent)

    in_shapefile.Destroy()
    out_shapefile.Destroy()

def create_grid(layer, extent, num_across=10, *args, **kwargs):
    """
    Creates a grid of hexagon features in `layer`.
    """
    definition = layer.GetLayerDefn()
    width = extent[1] - extent[0]
    height = extent[3] - extent[2]

    scale_width = width / num_across

    column = 0
    y = extent[2] - scale_width
    while y < extent[3] + scale_width:
        x = extent[0] - scale_width
        if column % 2 == 0:
            x += 0.75 * scale_width
        while x < extent[1] + scale_width:
            hexagon = create_hexagon(x, y, scale_width)
            feature = ogr.Feature(definition)
            feature.SetGeometry(hexagon)
            feature.SetField('id', 0)
            layer.CreateFeature(feature)
            feature.Destroy()
            x += (1.5 * scale_width)
        # TODO What is the math behind this value?
        y += (0.61625 * scale_width)
        column += 1

def create_hexagon(center_x, center_y, scale, *args, **kwargs):
    """
    Returns a hexagon geometry around the center point.
    """
    h_val = math.sqrt(3) / 4
    scale_quarter = scale / 4
    scale_half = scale / 2
    ring = ogr.Geometry(ogr.wkbLinearRing)

    # Draw hexagon clockwise, beginning with northwest vertice
    ring.AddPoint(center_x - scale_quarter, center_y + h_val)
    ring.AddPoint(center_x + scale_quarter, center_y + h_val)
    ring.AddPoint(center_x + scale_half, center_y)
    ring.AddPoint(center_x + scale_quarter, center_y - h_val)
    ring.AddPoint(center_x - scale_quarter, center_y - h_val)
    ring.AddPoint(center_x - scale_half, center_y)
    ring.AddPoint(center_x - scale_quarter, center_y + h_val)

    hexagon = ogr.Geometry(type=ogr.wkbPolygon)
    hexagon.AddGeometry(ring)
    return hexagon

if __name__ == '__main__':
        main()

