Binify
======
A command-line tool to better visualize crowded dot density maps.

Don't miss the [introductory blog post](http://www.kevinschaul.com/2013/04/18/introducing-binify/).

Developed as part of a visualization course at the University of Minnesota.

Have an idea? Open up an [issue](https://github.com/kevinschaul/binify/issues).

![ScreenShot](http://www.kevinschaul.com/wp-content/uploads/2013/04/binify-before-after.png)

Installation
------------

Binify is available in the Python Package Index. I recommend using a virtual environment.

    $ mkvirtualenv binify
    $ pip install binify

Node: This installation assumes GDAL is already installed.
To install GDAL with python bindings:

OS X:
Try the precompiled biniaries by [KyngChaos](http://www.kyngchaos.com/software/frameworks).

Ubuntu:
    
    $ sudo apt-add-repository ppa:ubuntugis/ppa
    $ sudo apt-get update
    $ sudo apt-get install python-gdal

Usage
-----

To view options for your installed version of Binify, use the help flag.

    $ binify --help
    usage: binify [-h] [-n NUM_ACROSS] [-o] [--ignore-type] infile outfile

    positional arguments:
      infile                A point shapefile to create bins from.
      outfile               A shapefile to write to. Will be created if it does
                            not exist.

    optional arguments:
      -h, --help            show this help message and exit
      -n NUM_ACROSS, --num-across NUM_ACROSS
                            Number of hexagons for the grid to have across
                            (approximate)
      -e, --exclude-empty   Exclude shapes that end up binning zero points.
      -o, --overwrite       Overwrite output file.
      --ignore-type         Ignore the geometry type of the input shapefile.
      --suppress-output     Supress console output (excluding any warnings).

A basic execution may look like this:

    $ binify MN_FFLS/MN_FFLS.shp MN_FFLS-grid/MN_FFLS-grid.shp

