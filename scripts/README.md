# XNET X5 hex mapping system
Created by Sint Connexa, aka Rich DeVaul. @xnet-mobile and @rdevaul

This is the home for the X5 JavaScript implementation that is the
reference implementation of the [X5 Grid System](../docs/X5.md),
code conversion of the X5 code to Python3, and some related tools.

## What is X5?

X5 is the XNET hex mapping system that assigns every location on the
planet between 70 degrees north and south latitude to a hex of about
1.8 km^2, and gives each hex a unique 32 bit address, as well as a
unique three-word name. For more information, please see the [X5 Grid
System](../docs/X5.md) documentation.

## Contents

* [geom.js](geom.js) &mdash; the reference implementation for core X5
  hex mapping
  * [x5geom.py](x5geom.py) &mdash; geom.js translated to Python3 by
    way of `js2py`
* [words2index.js](words2index.js) &mdash; map X5 hex indices into
  three-word names, and vice versa.
  * [x5words2index.py](x5words2index.py) &mdash; words2index.js
  translated to Pyhthon3 by way of `js2py` three-word names, and vice
  versa.
* [zip2map.py](zip2map.py) &mdash; a
  [yapCAD](https://github.com/rdevaul/yapCAD)-based tool for
  generating hex tilings of zipcodes

## Core Geometry Code

The core X5 code is found in [geom.js](./geom.js) and
[words2index.js](./words2index.js) source files, which provide the
foundational hex grid and hex-index-to-three-word-name functionality.

## zip2map.py &mdash; Batch Processing for Zip code Conversion

To make the XNET visualizer work, and to perform on-chain validation,
it is necessary to map a set of allowed zip codes to a set of
corresponding X5 hexes, where a hex is included if the zip code
overlaps any portion of that hex.

Because the mapping of zip codes to hexes doesn't change often and is
computationally intensive, it makes sense to compute this mapping as a
batch job, which is what `zip2map.py` does.  As new zip codes are
added, it will be necessary to re-run this script from time to time.

## zip2map.py dependencies

To run `zip2map.py` you will need to install a recent version of
Python3 and the latest version of YapCAD.  Installing Python3 is
operating-system specific, and beyond the scope of this document. Once
Python3 is installed, you can use pip to install YapCAD as follows:

	pip3 install yapcad
	
You will also need the zip code outlines in GeoJSON format, which you
can find here: https://github.com/OpenDataDE/State-zip-code-GeoJSON
&mdash; **NOTE** these GeoJSON files are large, and you will need gigs
of disk and RAM to store the GeoJSON files and run this script.

## running zip2map.py

A typical run will involve generating the mapping for many zip codes,
so the result of running the script will be a bunch of separate JSON
and DXF files, as well as one larger JSON file with the consolidated
output mapping. For that reason, we recommend running `zip2map.py` in
a working directory, and have helpfully created the `output` directory
for this purpose.

The `zip2map.py` script takes zip codes as individual command-line
arguments, but since you will likely want to operate on many zip codes
at once, we recommend using a list of zip codes stored in a text file
and using the `cat` utility to expand that file on the command line. 

For example, imagine you wanted to regenerate the XNET hex mappings
for Chicago, and you have a GeoJSON file of zip code boundaries for
Illinois called `il_illinois_zip_codes_geo.json` which you've also
copied into the `output` directory for convenience.  You might invoke
the script as:

	cd ../output
	python3 ../scripts/zip2map.py il_illinois_zip_codes_geo.json `cat chicagoZIPS.txt`

## zip code to hex mapping problem overview

For those who want to understand a little more about why the problem
of mapping zip codes to hexes is non-trivial, and the specifics of the
approach taken here, please read on:

### why zip code to hex mapping is hard

The mapping problem is hard because zip codes can be strange. Some
zip codes are fairly boring &mdash; convex, compact, and seemingly
rational geographic divisions.  However, zip cods can also be long and
skinny, organic and snakey, or be broken many separate discontiguous
chunks.  Zip codes can range in size from hundreds of X5 hexes to
smaller than a single hex, can have complex non-convex shapes, and can
be discontiguous.  Taken together, this makes the zip code to hex
mapping problem a non-trivial computational geometry task.

### why choose Python3 and YapCAD as the computational geometry engine?

We chose YapCAD because there was no obvious choice for solving this
type of computational geometry problem in a pure Node/JavaScript
framework, and at that point Python3 and YapCAD were the next logical
choices.

There is an excellent tool for translating JavaScript to
Python3, namely [`js2py`](https://github.com/PiotrDabkowski/Js2Py), and
this tool works quite well for the core X5 code. That meant we could
use the reference X5 implementation without modification.

YapCAD is a pure Python3 package with few external
dependences. YapCAD provides the core computational geometry
features, namely computing the intersections of complex
line-segment-defined boundaries, in a simple-to-use form.  Also, we
wrote YapCAD, so we know who to blame if there are any bugs ;)

### hex inclusion rule

To solve the problem we establish the rule that if any portion of a
zip code outline intersects with any portion of a hex outline, the hex
is included. Also, if a zip code or a discontiguous portion of a
zip code falls entirely inside a hex without intersection, that hex is
included. Similarly, if a hex is entirely inside a zip code without
intersection, the hex is included.

### data output format

We start with a list of allowed zip codes and zip code outlines in
GeoJSON format. The output of the script is a JSON list of X5 hexes
that overlap in any way with the specified zip codes, and DXF
renderings of the zip codes and hexes for debugging purposes.

