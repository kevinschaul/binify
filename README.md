Binify
======
A command-line tool to better visualize crowded dot density maps.

Don't miss the [introductory blog post](http://kevin.schaul.io/2013/04/19/introducing-binify/).

Developed as part of a visualization course at the University of Minnesota.

Have an idea? Open up an [issue](https://github.com/kevinschaul/binify/issues).

![ScreenShot](http://kevin.schaul.io/assets/posts/2013-04-19-introducing-binify/binify-before-after.png)

In the wild
-----------

- [Binify + D3 = Gorgeous honeycomb maps](http://mechanicalscribe.com/notes/binify-d3-topojson-tutorial/) - Chris Wilson, Mechanical Scribe
- [The Drone War: A Comprehesive Map of Lethal U.S. Attacks](http://www.businessweek.com/articles/2013-05-23/the-drone-war-a-comprehensive-map-of-lethal-u-dot-s-dot-attacks) - Allsion McCann, Bloomberg Businessweek
- [Crimes reported in Waterloo, Iowa](http://wcfcourier.com/app/crime_map2013/index_wloo.php) - Chris Essig, Waterloo Cedar Falls Courier

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
      -E EAST_LNG WEST_LNG SOUTH_LAT NORTH_LAT, --extent EAST_LNG WEST_LNG SOUTH_LAT NORTH_LAT
                            Use a custom extent.
      -e, --exclude-empty   Exclude shapes that end up binning zero points.
      -o, --overwrite       Overwrite output file.
      --ignore-type         Ignore the geometry type of the input shapefile.
      --suppress-output     Supress console output (excluding any warnings).

A basic execution may look like this:

    $ binify MN_FFLS/MN_FFLS.shp MN_FFLS-grid/MN_FFLS-grid.shp

