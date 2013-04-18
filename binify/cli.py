#!/usr/bin/env python

import argparse

class CLI(object):
    """
    Handles command-line interface options
    """

    def parse_arguments(self, *args, **kwargs):
        """
        Implement command-line arguments
        """
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('infile', help='A point shapefile to create \
                bins from.')
        self.parser.add_argument('outfile', help='A shapefile to write to. \
                Will be created if it does not exist.')
        self.parser.add_argument('-n', '--num-across', type=int,
                dest='num_across', default=10, help='Number of hexagons for \
                the grid to have across (approximate)')
        self.parser.add_argument('-o', '--overwrite', action='store_true', \
                help='Overwrite output file.')
        self.parser.add_argument('--ignore-type', action='store_true', \
                dest='ignore_type', help='Ignore the geometry type of the \
                input shapefile.')
        return self.parser.parse_args()

