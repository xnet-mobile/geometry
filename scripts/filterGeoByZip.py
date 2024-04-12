## filterGeoByZip.py
## created by Sint Connexa, Tue Apr  9 21:22:51 PDT 2024

"""
script to take a geoJSON file with zipcode geometry and filter it by
a list of zipcodes provided on the command line
"""

debug = True

def loadGeo(infile):
    rval = {}
    with open(infile) as f:
        rval = json.load(f)
    return rval


import json
import os

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 4:
        print(f"""syntax: $ python3 {sys.argv[0]} [geojson-file] [outfile]  [zip1] [zip2...]
    Where [geojson-file] is a geojson file of zipcode outlines,
        and [outfile] is the name of the filtered output file.
        The remaining arguments are zipcodes to process. """)
        quit()
    geomap=sys.argv[1]
    outfile=sys.argv[2]
    zips=sys.argv[3:]
    if len(zips) == 1 and zips[0].split('.')[1]=="json":
        if debug:
            print(f"loading zips in XNET zipcodes file {zips[0]}")
        foo = loadGeo(zips[0])
        zips = foo["zips"]
    print(f"geomap: {geomap}, outfile: {outfile}, zips: {zips}")

    geojson = loadGeo(geomap)
    features = geojson["features"]
    rval = {}
    rval["type"] = geojson["type"]
    rval["features"] = []
    if debug:
        print(f"length of features: {len(features)}")
    for feat in features:
        prop = feat["properties"]
        matched = False
        for z in zips:
            if prop["ZCTA5CE10"].strip() == z.strip():
                matched= True
                if debug:
                    print(f"matched zip {z}")
                break
        if matched:
            rval["features"] += [ feat ]

    if debug:
        print(f"writing to {outfile}...",end="")
    with open(outfile, 'w', encoding='utf-8') as f:
        json.dump(rval, f, ensure_ascii=False)
    if debug:
        print("done")
        
