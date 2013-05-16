#!/usr/bin/env python

import math

from osgeo import ogr

from shapegrid import ShapeGrid

SQRT_3_DIV_4 = math.sqrt(3) / 4

class HexagonGrid(ShapeGrid):
    """
    Generic shape grid interface.
    """

    def __init__(self):
        pass

    def create_grid(self, layer, extent, num_across=10):
        """
        Creates a grid of hexagon features in `layer`.
        """
        definition = layer.GetLayerDefn()
        width = extent[1] - extent[0]
        height = extent[3] - extent[2]
        scale_width = width / num_across

        row = 0
        column = 0
        y = extent[2] - scale_width
        while y < extent[3] + scale_width:
            x = extent[0] - scale_width
            if column % 2 == 0:
                x += 0.75 * scale_width
            row = 0
            while x < extent[1] + scale_width:
                hexagon = self.create_hexagon(x, y, scale_width)
                feature = ogr.Feature(definition)
                feature.SetGeometry(hexagon)
                feature.SetField('COUNT', 0)
                layer.CreateFeature(feature)
                feature.Destroy()
                x += (1.5 * scale_width)
                row += 1
            y += SQRT_3_DIV_4 * scale_width
            column += 1
        # TODO Test column count edge cases
        return row, column / 2

    def create_hexagon(self, center_x, center_y, width):
        """
        Returns a hexagon geometry around the center point.
        """
        h_val = SQRT_3_DIV_4 * width
        width_quarter = width / 4
        width_half = width / 2
        ring = ogr.Geometry(ogr.wkbLinearRing)

        # Draw hexagon clockwise, beginning with northwest vertice
        ring.AddPoint(center_x - width_quarter, center_y + h_val)
        ring.AddPoint(center_x + width_quarter, center_y + h_val)
        ring.AddPoint(center_x + width_half, center_y)
        ring.AddPoint(center_x + width_quarter, center_y - h_val)
        ring.AddPoint(center_x - width_quarter, center_y - h_val)
        ring.AddPoint(center_x - width_half, center_y)
        ring.AddPoint(center_x - width_quarter, center_y + h_val)

        hexagon = ogr.Geometry(type=ogr.wkbPolygon)
        hexagon.AddGeometry(ring)
        return hexagon

