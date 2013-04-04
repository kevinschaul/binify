Binify
======
A command-line tool to [bin geospatial data](http://mapbox.com/blog/binning-alternative-point-maps/).

Binify will create a grid of hexagons to cover the input shapefile. The output shapefile will have an attribute `COUNT`, which contains how many points intersect that hexagon. This attribute can later be used to color code the grid, resulting in a visual density headmap.

Developed as part of a visualization course at the University of Minnesota.

Have an idea? Open up an [issue](https://github.com/kevinschaul/binify/issues).

Installation
------------

    mkvirtualenv binify
    python setup.py install

Example usage
-------------

    binify tests/test-shapefiles/MN_FFLS.shp tests/test-shapefiles/MN_FFLS-grid.shp

