# Computational Geometry for XNET

This folder is the home for the core [X5 Hex Grid](docs/X5.md)
libraries and some related tools and code conversions. X5 provides the
basis for the XNET hex grid system, and differs in important ways in
design and implementation from Uber's H3 system. See the [X5 Hex Grid
documentation](docs/X5.md) for more information.

This folder is also the home to computation geometry tools that are
used for the batch processing of geo data in order to build the maps
and dictionaries used by the XNET visualizer, and ultimately the
on-chain smart-contract implementations. 

## contents
There is a lot here, but here are some of the more interesting contents:

* [scripts/geom.js](scripts/geom.js) &mdash; the core reference implementation for X5 operations
* [scripts/zip2map.py](scripts/zip2map.py) &mdash; a
  [yapCAD](https://github.com/rdevaul/yapCAD)-based tool for
  generating hex tilings of zipcodes

  

