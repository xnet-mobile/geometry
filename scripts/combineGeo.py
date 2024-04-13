## combineGeo.py
## created by Sint Connexa, Fri Apr 12 17:28:36 PDT 2024

"""
script to take a list of GeoJSON files and combine them into a
single output

"""

debug = True

import json
import os

def loadJSON(infile):
    rval = {}
    with open(infile) as f:
        rval = json.load(f)
    return rval

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 4:
        print(f"""syntax: $ python3 {sys.argv[0]} [outfile] [zip1] [zip2...]
        Where [outfile] is the combined GeoJSON file to create and 
           the remaining argments are the GeoJSON input files.""")
        quit()

    outfile = sys.argv[1]

    if debug:
        print(f"reading {sys.argv[2]}",end="")

    cjson = loadJSON(sys.argv[2])
    
    for inf in sys.argv[3:]:
        if debug:
            print(f" - {len(cjson['features'])} features, {inf}", end="")
        nj = loadJSON(inf)
        cjson["features"] += nj["features"]
    if debug:
        print(f" - {len(cjson['features'])} features... done\nWriting {outfile}...",end="")
    with open(outfile, 'w', encoding='utf-8') as f:
        json.dump(cjson,f, ensure_ascii=False)
    if debug:
        print("done")
    

