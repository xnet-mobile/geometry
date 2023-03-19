## zip2map.py
## created by Sint Connexa, Mon Jan  2 15:58:38 PST 2023

"""
Read a geoJSON file contiaining the outlines of US zipcodes, and
for each specified zipcode, generate a list of hexes that overalp with
that zipcode
"""

#from yapcad.geom import *
from yapcad.pyglet_drawable import *
from yapcad.ezdxf_drawable import *
from x5geom import geom
from x5words2index import x5words2index
from yapcad.geom import *
import json
import os

#set up DXF rendering
def setupDXF(filename):
    d=ezdxfDraw()
    print("\nOutput file name is {}.dxf".format(filename))
    d.filename = filename
    return d
    
#set up openGL rendering
def setupGL():
    dGl =pygletDraw()
    dGl.magnify = 1.0
    dGl.linecolor = 'white'
    dGl.cameradist = 30
    return dGl


# load a geojson file, return the object
def geofile2obj(fname):
    f = open(fname,)
    geo = json.load(f)
    f.close()
    return geo

def geo2polyline(geopoly):
    if geopoly["type"] == "MultiPolygon":
        return geomultipoly2polyline(geopoly)
    if geopoly["type"] == "Polygon":
        return geopoly2polyline(geopoly)
    print("bad object passed to geo2polyline")
    return []

def geomultipoly2polyline(geopoly):
    if geopoly["type"] != "MultiPolygon":
        print("bad object passed to geomultipoly2polyline")
        return []
    multy = []
    for donut in geopoly["coordinates"]:
        for ply in donut:
            poly = []
            for c in ply:
                poly.append(point(c[0],c[1]))
            poly.append(poly[0])
            multy.append(poly)
    return multy

# given a geoJSON-style geometry object of type Polygon, return a
# yapCAD polyline
def geopoly2polyline(geopoly):
    if geopoly["type"] != "Polygon":
        print("bad object passed to geopoly2polyline")
        return []
    coordinates = geopoly["coordinates"][0]
    poly = []
    for c in coordinates:
        poly.append(point(c[0],c[1]))
    poly.append(poly[0])
    return poly

def makeHexes(outline,countScore=False):
    box = bbox(outline)
    print(f"bbox: {box}")
    ll = geom.latLon2grid(box[0][1],box[0][0])
    ul = geom.latLon2grid(box[0][1],box[1][0])
    lr = geom.latLon2grid(box[1][1],box[0][0])
    ur = geom.latLon2grid(box[1][1],box[1][0])
    print(f"ll: {ll}")
    print(f"ur: {ur}")
    print(f"grid2latLon({ll[0],ll[1]}): {geom.grid2latLon(ll[0],ll[1])}")

    mini = min(ll[0],ul[0],lr[0],ur[0])
    maxi = max(ll[0],ul[0],lr[0],ur[0])
    minj = min(ll[1],ul[1],lr[1],ur[1])
    maxj = max(ll[1],ul[1],lr[1],ur[1])
    print(f"min i,j: {mini,minj}  max i,j: {maxi,maxj}")
    print(f"grid2latLon({mini,minj}): {geom.grid2latLon(mini,minj)}")
        
    irange = maxi-mini
    jrange = maxj-minj
        
    hexpolys=[]
    hexlist=[]
    scores=[]
    maphex=[]

    tinyzip=False
    i,j = [0,0]

    # zip falls entirely inside one hex
    if irange == 0 and jrange == 0:
        i=mini
        j=minj
        tinyzip=True

    # zip most likely falls inside one hex or the other
    if (irange == 0 and jrange == 1) or (jrange == 0 and irange ==1):
        cen = center(outline1)
        i,j = geom.latLon2grid(cen[1],cen[0])
        tinyzip=True

    # handle tiny zip case
    if tinyzip:
        maphex = geom.grid2latLonHex(i,j)
        maphex[len(maphex)]=maphex[0]
        maphex = list(map(lambda p : point(p[1],p[0]) ,maphex))
        hexpolys.append(maphex)
        hexlist.append([i,j])
        score=1 
        scores.append(score)
        print(f"hex [{i},{j}] score {score}")
        return hexpolys,hexlist, scores

    scalef=100
    scaleoutline = scale(outline,scalef)
    for ii in range(irange+1):
        for jj in range(jrange+1):
            i=ii+mini
            j=jj+minj
            maphex  = geom.grid2latLonHex(i,j)
            maphex[len(maphex)]=maphex[0]
            maphex = list(map(lambda p : point(p[1],p[0]) ,maphex))
            # print(f"maphex: {maphex}")
            testpoints = scale(maphex,scalef)
            cntr = geom.grid2latLon(i,j)
            cntr = scale(point(cntr[1],cntr[0]),scalef)
            # testpoints.append(point(cntr[1],cntr[0]))
            # testpoints = [ point(cntr[1],cntr[0]) ]
            inside=False
            score=0
            if isinsideXY(scaleoutline,cntr):
                inside=True
                score=1
            else:
                if intersectXY(testpoints,scaleoutline):
                    inside=True
                    score=1
            # for p in testpoints:
            #     if isinsideXY(scaleoutline,p):
            #         inside=True
            #         score+=1
            #         if not countScore: break
            if inside:
                maphex.append(maphex[0])
                hexpolys.append(maphex)
                hexlist.append([i,j])
                scores.append(score)
                print(f"hex [{i},{j}] score {score}")
                    
    return hexpolys,hexlist, scores


# given a geojson object and a zipcode string, return the yapCAD
# polyline representation
def zip2poly(geo,inzip):
    inzip = inzip.strip()
    for feature in geo["features"]:
        if feature["properties"]["ZCTA5CE10"] == inzip:
            print(f"got a hit for zipcode {inzip}")
            return geo2polyline(feature["geometry"])
    print(f"no hit for zipcode {inzip}")
    return []


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print(f"syntax: $ python3 {sys.argv[0]} [geojson-file] [namebase] [zip1] [zip2...]")
        print("    Where [geojson-file] is a geojson file of zipcode outlines,")
        print("    [namebase].json is the name of the combined map file to overwrite, and")
        print("    [namebase]_[zip].json will the name of the zipcode map file to overwrite")
        print("    for each zip. The remaining arguments are zipcodes to process.")
        print("")
        print("    If the environment variable YAPRENDER is set to opengl, make an")
        print("    interactive 3D visualization of the map. Otherwise create DXF files for")
        print("    each zipcode showing the hex overlay")
        quit()
    geomap=sys.argv[1]
    namebase=sys.argv[2]
    zips=sys.argv[3:]
    print(f"geojson filename: {geomap}  namebase: {namebase}  ziplist: {zips}")

    print("loading geoJSON file...")
    geo = geofile2obj(geomap)

    # read rendering mode from env
    YAPRENDER = os.getenv('YAPRENDER')
    if YAPRENDER == None:
        YAPRENDER='dxf'
        
    zipdict = {}
    zipdict["zips"] = []
    for zip1 in zips:
        localdict= {}
        print(f"converting geoJSON for {zip1}")
        outline1 = zip2poly(geo,zip1)

        if outline1 == []:
            continue

        zipdict["zips"].append(zip1)
        
        print("setting up rendering")
        ## setup OpenGL rendering
        if YAPRENDER == 'opengl':
            d = setupGL()
        else:
            fname = f"{namebase}_{zip1}"
            d = setupDXF(fname)

        print(f"building list of overlapping hexes")
        hexdraw,indices,scores = makeHexes(outline1,False)

        for idx in indices:
            i,j=idx
            ## key = x5words2index.ij2string(i,j)
            key = f"{i:05}{j:05}"
            localdict[key] = [ zip1 ]
            if key in zipdict:
                zipdict[key].append(zip1)
            else:
                zipdict[key] = [ zip1 ]

        ## scale and center the zipcodes and hexes for rendering
        cen = center(outline1)
        trns = scale(cen,-1.0)
        scalef = 200

        outline2 = translate(outline1,trns)
        outline2 = scale(outline2,scalef)

        hexdraw2 = translate(hexdraw,trns)
        hexdraw2 = scale(hexdraw2,scalef)

        # find the bounding box
        bb = bbox(hexdraw2)
        print(f"scaled bbox: {bb}")
        
        ## draw the geometry
        d.draw([outline2])

        d.layer = 'DOCUMENTATION'
        for idx in indices:
            i,j=idx
            lat,lon = geom.grid2latLon(i,j)
            cntr = translate(point(lon,lat),trns)
            cntr = scale(cntr,scalef)
            delta = point(0,0.15)
            hexname = x5words2index.ij2string(i,j)
            d.linecolor = 256 ## set layer default color
            d.draw_text(f"{hexname}", sub(cntr,delta),
                        align='CENTER',
                        attr={'height': 0.18})

            key = f"{i:05}{j:05}"
            d.linecolor = 'aqua'
            d.draw_text(f"{key}", add(cntr,delta),
                        align='CENTER',
                        attr={'height': 0.25})
            
        # for i in range(len(hexdraw2)):
        #     hexen = hexdraw2[i]
        #     score =scores[i]
        #     color = [64, 127, 2**(score+1)-1]
        #     dGl.linecolor = color
        #     dGl.draw(hexen)

        d.linecolor = 'red'
        d.draw(hexdraw2)
        d.layer = 'DOCUMENTATION'
        d.linecolor = 256 ## set layer default color
        d.draw_text(f"zip2map analysis of zipcode {zip1}",
                    sub(bb[0],point(0,1.0)),
                    attr={'style': 'OpenSans-Bold', # style for ezdxf
                          'font_name': 'OpenSans', # style for pyglet
                          'bold': True, # style for pyglet
                          'height': 1.0})
  
        d.display()
        fname = f"{namebase}_{zip1}.json"
        print(f"writing {fname} zipcode map")
        with open(fname, 'w') as outfile:
            json.dump(localdict, outfile,indent=4)


    fname = f"{namebase}.json"
    print(f"writing global {fname} zipcode map")
    with open(fname, 'w') as outfile:
        json.dump(zipdict, outfile,indent=4)

    
