#!/usr/bin/env python

class ShapeGrid(object):
    """
    Generic shape grid interface. Should be subclassed by specific shapes.
    """

    def __init__(self):
        pass

    def create_grid(self, layer, extent, num_across=10):
        raise NotImplementedError('Provided by each subclass of ShapeGrid.')

