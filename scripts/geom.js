// Javascript library for X5, XNET's hexagonal mapping system
// Core geometry functions
// Created by Sint Connexa, 18 August 2022

// haversine distance between two lat-lon points, value in meters.
// based on example provided by
// https://www.movable-type.co.uk/scripts/latlong.html

const earthR = 6371e3; // radius of the Earth in meters

function haversine(lat1, lon1, lat2, lon2) {
    // coerce arguments to numbers (may be strings)
    lat1 = Number(lat1);
    lat2 = Number(lat2);
    lon1 = Number(lon1);
    lon2 = Number(lon2);
    const φ1 = lat1 * Math.PI/180; // φ, λ in radians
    const φ2 = lat2 * Math.PI/180;
    const Δφ = (lat2-lat1) * Math.PI/180;
    const Δλ = (lon2-lon1) * Math.PI/180;

    const a = Math.sin(Δφ/2) * Math.sin(Δφ/2) +
          Math.cos(φ1) * Math.cos(φ2) *
          Math.sin(Δλ/2) * Math.sin(Δλ/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

    const d = earthR * c; // in metres
    return d;
}

// given a lat/lon location and a two-dimensional displacement vector
// in meters, compute a new lat/lon. NOTE: accurate only for small
// (less than 100km) Δy if large Δx displacement involved.
function travel(lat1, lon1 ,Δx, Δy) {
    // coerce arguments to numbers (may be strings)
    lat1 = Number(lat1);
    lon1 = Number(lon1);
    Δy = Number(Δy);
    Δx = Number(Δx);
    const pi = Math.PI;
    const cos = Math.cos;
    const mlat = (1.0 / ((2.0 * pi / 360.0) * earthR)) ;  //1 meter in one degree latitude
    const mlon = mlat/cos(lat1 * (pi / 180.0));		  //1 meter in one degree longitude
    const lat2 = lat1 + Δy * mlat;
    const lon2 = lon1 + Δx * mlon;
    return [lat2, lon2];
}

// function to compute the distance between two packed latlong
// coordinate representations. Returns distance in meters
function gpsDiff(packed1,packed2) {
    const latlon1 = decodeGPS(packed1);
    const latlon2 = decodeGPS(packed2);
    const d = haversine(latlon1[0], latlon1[1],
			latlon2[0], latlon2[1]);
    return d;
}

// test GPS coordinates for lying within three sigma (99%) of each
// other. Default σ = 1.5m, 2σ (95%) = 3m, 3σ = 4.5m

// NOTE: 3σ implies that we expect one test out of 100 to fail due to
// error even when the true location has not changed. However, GPS
// meaasurement error is highly autocorrelated for stationary
// measurements, meaning that the true error-driven failure rate
// should be significantly lower.

function sigmaTest(packed1,packed2,σ=1.5) {
    return gpsDiff(packed1,packed2) < 3*σ;
}

// Generate an offset hex grid between -lat and +lat, 0-360 long.
// boundaries are toroidal, "wrapping" at +-lat and 0/360 long.
// Grid geometry steps 3/2 unit in X and 1/2 unit in y for each cell.
//   __    __ 
//  /  \__/2 \__    dir 2, "beta" = [ 3/2 l, 1/2 l ]
//  \__/1 \_0/2 \   _
//  /0 \_0/1 \_1/   /|
//  \_0/0 \_1/1 \  /
//  /  \_1/0 \__/ %
//  \__/  \_2/0 \   %
//  /  \__/  \_3/    _%/
//  \__/  \__/       dir 1, "alpha" = [ 3/2 l, -1/2 l ]

// utility function, take two two-vectors and add them, return result

function vec2add(v1,v2) {
    return [v1[0]+v2[0], v1[1]+v2[1]];
}

// utility function, take two two-vectors and subtract them, return result
function vec2sub(v1,v2) {
    return [v1[0]-v2[0], v1[1]-v2[1]];
}

// utility function, scale a two-vector by a constant
function vec2scale(v1,a) {
    return [v1[0]*a,v1[1]*a];
}

// move rendered verticies a bit towards the geometric center of a
// polygon, as specified by parameter factor. Primarily intended for
// rendering adjacent polys in a non-overlapping way

function displaceIn(geom,factor=0.03) {
    var sum = [0,0];
    for (var i = 0; i < geom.length; i++) {
	sum = vec2add(geom[i],sum);
    }
    const center = vec2scale(sum,1.0/geom.length);
    for (var i = 0; i < geom.length; i++) {
	const inward = vec2sub(center,geom[i]);
	const diff = vec2scale(inward,factor);
	geom[i] = vec2add(geom[i],diff);
    }
    return geom;
}


// transform a latitude/longitude position into coordinates in the
// alpha/beta skew coordinate system
function latLon2ab(lat,lon,maxLat=70,step=0.01) {
    
    lat= lat > 0 ? (lat+maxLat)%(2*maxLat)-maxLat :
	(lat - maxLat)%(2*maxLat)+maxLat // torroidal latitude
    lon = lon > 0 ? (lon + 180) % 360 - 180 :
	(lon - 180) % 360 + 180;  // torroidal longitude
    const s=step/2;

    const b = (lat +lon/3)/(2*s);
    const a = lon/(3*s) - b;

    return [a,b];
}

// given a coordinate in alpha/beta space, convert to latitude and
// longitude.

function ab2latLon(a,b,maxLat=70,step=0.01) {
    const alpha = [(3/2) * step, (-1/2) * step ];
    const beta =  [(3/2) * step, ( 1/2) * step ];
    
    const x= vec2add(vec2scale(alpha,a),vec2scale(beta,b));

    return [(x[1] + maxLat) % (2 * maxLat) - maxLat,
	    (x[0] + 180) % 360 - 180,];
}

// given a grid index in i,j, return the center of that hex
// in lat/long

function grid2latLon(i,j,maxLat=70,step=0.01,offset=13034) {
    const a=i-offset;
    const b=j-offset;
    return ab2latLon(a,b,maxLat,step);
}

// given a coordinate in alpha/beta space, determine which hex index
// it falls into.  For the region of the globe from -70 to 70 latitude
// and with a step value of 0.01, the offset added to make the
// smallest index non-negative is 13034

function ab2grid(a,b,offset=13034) {
    const x = b - Math.floor(b);
    const y = a - Math.floor(a);
    var i,j;

    const AB = -0.5*x - y + 0.5;
    if (AB > 0) {
	const FA = -2*x -y + 1;
	if (FA > 0) { // REGION I
	    i=Math.floor(a);
	    j=Math.floor(b);
	}
	else { // REGION II
	    i=Math.floor(a);
	    j=Math.floor(b)+1;
	}
    }
    else {
	const AH = x-y;
	if (AH > 0) {
	    const GH = -0.5*x - y + 1;
	    if (GH > 0) { // REGION II
		i=Math.floor(a);
		j=Math.floor(b)+1;
	    }
	    else { // REGION III
		i=Math.floor(a)+1;
		j=Math.floor(b)+1;
	    }
	}
	else {
	    const HJ= -2*x - y +2;
	    if (HJ > 0) { // REGION IV
		i=Math.floor(a)+1;
		j=Math.floor(b);
	    }
	    else { // REGION III
		i=Math.floor(a)+1;
		j=Math.floor(b)+1;
	    }
	}
    }
    i+= offset;
    j+= offset;
    return [i,j];
}

// given a coordinate in lat/long space, find which hex index (i,j) it
// falls into

function latLon2grid(lat,lon,maxLat=70,step=0.01,offset=13034) {
    var grid = latLon2ab(lat,lon,maxLat,step);
    return ab2grid(grid[0],grid[1],offset);
}


// given a grid i,j index, get the six points that compose the vertices
// of the hex in right-hand order
function grid2latLonHex(i,j,offset=13034,maxLat=70,step=0.01) {
    const a=i-offset;
    const b=j-offset;
    const abHex=[ [a+1/3, b+1/3], [a-1/3, b+2/3], [a-2/3, b+1/3],
		  [a-1/3, b-1/3], [a+1/3, b-2/3], [a+2/3, b-1/3] ];
    var latLon=[];
    for (var i =0; i < abHex.length; i++) {
	latLon.push(ab2latLon(abHex[i][0],abHex[i][1],maxLat,step));
    }
    return latLon;
}


if (typeof module !== 'undefined') {
    module.exports = {
	earthR,
	haversine,
	travel,
	gpsDiff,
	sigmaTest,
	vec2add,
	vec2scale,
	latLon2ab,
	ab2latLon,
	grid2latLon,
	ab2grid,
	latLon2grid,
	grid2latLonHex
    };
}

