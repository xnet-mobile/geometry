# Computational Geometry for XNET
Created by Sint Connexa, aka Rich DeVaul @xnet-mobile and @rdevaul

This folder is the home for the core [X5 Hex Grid](docs/X5.md)
libraries and some related tools and code conversions. X5 provides the
basis for the XNET hex grid system, and differs in important ways in
design and implementation from Uber's H3 system. See the [X5 Hex Grid
documentation](docs/X5.md) for more information.

This folder is also the home to computation geometry tools that are
used for the batch processing of geo data in order to build the maps
and dictionaries used by the XNET visualizer, and ultimately the
on-chain smart-contract implementations. 

## Contents
Here are some of the more interesting contents of this repo:

* [scripts/geom.js](scripts/geom.js) &mdash; the reference
  implementation for core X5 hex mapping
* [scripts/words2index.js](scripts/words2index.js) &mdash; map X5 hex
  indices into three-word names, and vice versa.
* [scripts/zip2map.py](scripts/zip2map.py) &mdash; a
  [yapCAD](https://github.com/rdevaul/yapCAD)-based tool for
  generating hex tilings of zipcodes

And here is the top-level oraganization:
* [LICENSE](LICENSE) &mdash; MIT license, which applies to all contents unless otherwise stated.
* [docs](docs) &mdash; documentation home
* [assets](assets) &mdash; images and reference data
* [scripts](scripts) &mdash; source code
* [output](output) &mdash; a working directory for the `zip2map.py` script

## Contact
For questions about this repo, please jump into the XNET discord
server at https://discord.gg/qJFJwkBZwj or email connexa@xnet.company
