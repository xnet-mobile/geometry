__all__ = ['geom']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['ab2latLon', 'vec2scale', 'travel', 'ab2grid', 'latLon2ab', 'grid2latLonHex', 'sigmaTest', 'grid2latLon', 'vec2add', 'latLon2grid', 'gpsDiff', 'earthR', 'haversine'])
@Js
def PyJsHoisted_haversine_(lat1, lon1, lat2, lon2, this, arguments, var=var):
    var = Scope({'lat1':lat1, 'lon1':lon1, 'lat2':lat2, 'lon2':lon2, 'this':this, 'arguments':arguments}, var)
    var.registers(['φ2', 'lat1', 'a', 'd', 'lon1', 'lon2', 'c', 'φ1', 'lat2', 'Δφ', 'Δλ'])
    var.put('lat1', var.get('Number')(var.get('lat1')))
    var.put('lat2', var.get('Number')(var.get('lat2')))
    var.put('lon1', var.get('Number')(var.get('lon1')))
    var.put('lon2', var.get('Number')(var.get('lon2')))
    var.put('φ1', ((var.get('lat1')*var.get('Math').get('PI'))/Js(180.0)))
    var.put('φ2', ((var.get('lat2')*var.get('Math').get('PI'))/Js(180.0)))
    var.put('Δφ', (((var.get('lat2')-var.get('lat1'))*var.get('Math').get('PI'))/Js(180.0)))
    var.put('Δλ', (((var.get('lon2')-var.get('lon1'))*var.get('Math').get('PI'))/Js(180.0)))
    var.put('a', ((var.get('Math').callprop('sin', (var.get('Δφ')/Js(2.0)))*var.get('Math').callprop('sin', (var.get('Δφ')/Js(2.0))))+(((var.get('Math').callprop('cos', var.get('φ1'))*var.get('Math').callprop('cos', var.get('φ2')))*var.get('Math').callprop('sin', (var.get('Δλ')/Js(2.0))))*var.get('Math').callprop('sin', (var.get('Δλ')/Js(2.0))))))
    var.put('c', (Js(2.0)*var.get('Math').callprop('atan2', var.get('Math').callprop('sqrt', var.get('a')), var.get('Math').callprop('sqrt', (Js(1.0)-var.get('a'))))))
    var.put('d', (var.get('earthR')*var.get('c')))
    return var.get('d')
PyJsHoisted_haversine_.func_name = 'haversine'
var.put('haversine', PyJsHoisted_haversine_)
@Js
def PyJsHoisted_travel_(lat1, lon1, Δx, Δy, this, arguments, var=var):
    var = Scope({'lat1':lat1, 'lon1':lon1, 'Δx':Δx, 'Δy':Δy, 'this':this, 'arguments':arguments}, var)
    var.registers(['lat1', 'Δy', 'pi', 'Δx', 'cos', 'lon2', 'lon1', 'mlat', 'lat2', 'mlon'])
    var.put('lat1', var.get('Number')(var.get('lat1')))
    var.put('lon1', var.get('Number')(var.get('lon1')))
    var.put('Δy', var.get('Number')(var.get('Δy')))
    var.put('Δx', var.get('Number')(var.get('Δx')))
    var.put('pi', var.get('Math').get('PI'))
    var.put('cos', var.get('Math').get('cos'))
    var.put('mlat', (Js(1.0)/(((Js(2.0)*var.get('pi'))/Js(360.0))*var.get('earthR'))))
    var.put('mlon', (var.get('mlat')/var.get('cos')((var.get('lat1')*(var.get('pi')/Js(180.0))))))
    var.put('lat2', (var.get('lat1')+(var.get('Δy')*var.get('mlat'))))
    var.put('lon2', (var.get('lon1')+(var.get('Δx')*var.get('mlon'))))
    return Js([var.get('lat2'), var.get('lon2')])
PyJsHoisted_travel_.func_name = 'travel'
var.put('travel', PyJsHoisted_travel_)
@Js
def PyJsHoisted_gpsDiff_(packed1, packed2, this, arguments, var=var):
    var = Scope({'packed1':packed1, 'packed2':packed2, 'this':this, 'arguments':arguments}, var)
    var.registers(['latlon2', 'd', 'packed2', 'packed1', 'latlon1'])
    var.put('latlon1', var.get('decodeGPS')(var.get('packed1')))
    var.put('latlon2', var.get('decodeGPS')(var.get('packed2')))
    var.put('d', var.get('haversine')(var.get('latlon1').get('0'), var.get('latlon1').get('1'), var.get('latlon2').get('0'), var.get('latlon2').get('1')))
    return var.get('d')
PyJsHoisted_gpsDiff_.func_name = 'gpsDiff'
var.put('gpsDiff', PyJsHoisted_gpsDiff_)
@Js
def PyJsHoisted_sigmaTest_(packed1, packed2, σ, this, arguments, var=var):
    var = Scope({'packed1':packed1, 'packed2':packed2, 'σ':σ, 'this':this, 'arguments':arguments}, var)
    var.registers(['packed2', 'σ', 'packed1'])
    var.put('σ', (Js(1.5) if (var.get('σ')==var.get('undefined')) else var.get('σ')))
    return (var.get('gpsDiff')(var.get('packed1'), var.get('packed2'))<(Js(3.0)*var.get('σ')))
PyJsHoisted_sigmaTest_.func_name = 'sigmaTest'
var.put('sigmaTest', PyJsHoisted_sigmaTest_)
@Js
def PyJsHoisted_vec2add_(v1, v2, this, arguments, var=var):
    var = Scope({'v1':v1, 'v2':v2, 'this':this, 'arguments':arguments}, var)
    var.registers(['v2', 'v1'])
    return Js([(var.get('v1').get('0')+var.get('v2').get('0')), (var.get('v1').get('1')+var.get('v2').get('1'))])
PyJsHoisted_vec2add_.func_name = 'vec2add'
var.put('vec2add', PyJsHoisted_vec2add_)
@Js
def PyJsHoisted_vec2scale_(v1, a, this, arguments, var=var):
    var = Scope({'v1':v1, 'a':a, 'this':this, 'arguments':arguments}, var)
    var.registers(['a', 'v1'])
    return Js([(var.get('v1').get('0')*var.get('a')), (var.get('v1').get('1')*var.get('a'))])
PyJsHoisted_vec2scale_.func_name = 'vec2scale'
var.put('vec2scale', PyJsHoisted_vec2scale_)
@Js
def PyJsHoisted_latLon2ab_(lat, lon, maxLat, step, this, arguments, var=var):
    var = Scope({'lat':lat, 'lon':lon, 'maxLat':maxLat, 'step':step, 'this':this, 'arguments':arguments}, var)
    var.registers(['lon', 'a', 'maxLat', 's', 'b', 'step', 'lat'])
    var.put('maxLat', (Js(70.0) if (var.get('maxLat')==var.get('undefined')) else var.get('maxLat')))
    var.put('step', (Js(0.01) if (var.get('step')==var.get('undefined')) else var.get('step')))
    var.put('lat', ((((var.get('lat')+var.get('maxLat'))%(Js(2.0)*var.get('maxLat')))-var.get('maxLat')) if (var.get('lat')>Js(0.0)) else (((var.get('lat')-var.get('maxLat'))%(Js(2.0)*var.get('maxLat')))+var.get('maxLat'))))
    var.put('lon', ((((var.get('lon')+Js(180.0))%Js(360.0))-Js(180.0)) if (var.get('lon')>Js(0.0)) else (((var.get('lon')-Js(180.0))%Js(360.0))+Js(180.0))))
    var.put('s', (var.get('step')/Js(2.0)))
    var.put('b', ((var.get('lat')+(var.get('lon')/Js(3.0)))/(Js(2.0)*var.get('s'))))
    var.put('a', ((var.get('lon')/(Js(3.0)*var.get('s')))-var.get('b')))
    return Js([var.get('a'), var.get('b')])
PyJsHoisted_latLon2ab_.func_name = 'latLon2ab'
var.put('latLon2ab', PyJsHoisted_latLon2ab_)
@Js
def PyJsHoisted_ab2latLon_(a, b, maxLat, step, this, arguments, var=var):
    var = Scope({'a':a, 'b':b, 'maxLat':maxLat, 'step':step, 'this':this, 'arguments':arguments}, var)
    var.registers(['a', 'maxLat', 'b', 'alpha', 'beta', 'step', 'x'])
    var.put('maxLat', (Js(70.0) if (var.get('maxLat')==var.get('undefined')) else var.get('maxLat')))
    var.put('step', (Js(0.01) if (var.get('step')==var.get('undefined')) else var.get('step')))
    var.put('alpha', Js([((Js(3.0)/Js(2.0))*var.get('step')), (((-Js(1.0))/Js(2.0))*var.get('step'))]))
    var.put('beta', Js([((Js(3.0)/Js(2.0))*var.get('step')), ((Js(1.0)/Js(2.0))*var.get('step'))]))
    var.put('x', var.get('vec2add')(var.get('vec2scale')(var.get('alpha'), var.get('a')), var.get('vec2scale')(var.get('beta'), var.get('b'))))
    return Js([(((var.get('x').get('1')+var.get('maxLat'))%(Js(2.0)*var.get('maxLat')))-var.get('maxLat')), (((var.get('x').get('0')+Js(180.0))%Js(360.0))-Js(180.0))])
PyJsHoisted_ab2latLon_.func_name = 'ab2latLon'
var.put('ab2latLon', PyJsHoisted_ab2latLon_)
@Js
def PyJsHoisted_grid2latLon_(i, j, maxLat, step, offset, this, arguments, var=var):
    var = Scope({'i':i, 'j':j, 'maxLat':maxLat, 'step':step, 'offset':offset, 'this':this, 'arguments':arguments}, var)
    var.registers(['offset', 'a', 'maxLat', 'b', 'j', 'i', 'step'])
    var.put('maxLat', (Js(70.0) if (var.get('maxLat')==var.get('undefined')) else var.get('maxLat')))
    var.put('step', (Js(0.01) if (var.get('step')==var.get('undefined')) else var.get('step')))
    var.put('offset', (Js(13034.0) if (var.get('offset')==var.get('undefined')) else var.get('offset')))
    var.put('a', (var.get('i')-var.get('offset')))
    var.put('b', (var.get('j')-var.get('offset')))
    return var.get('ab2latLon')(var.get('a'), var.get('b'), var.get('maxLat'), var.get('step'))
PyJsHoisted_grid2latLon_.func_name = 'grid2latLon'
var.put('grid2latLon', PyJsHoisted_grid2latLon_)
@Js
def PyJsHoisted_ab2grid_(a, b, offset, this, arguments, var=var):
    var = Scope({'a':a, 'b':b, 'offset':offset, 'this':this, 'arguments':arguments}, var)
    var.registers(['offset', 'a', 'x', 'b', 'GH', 'j', 'i', 'y', 'AH', 'FA', 'AB', 'HJ'])
    var.put('offset', (Js(13034.0) if (var.get('offset')==var.get('undefined')) else var.get('offset')))
    var.put('x', (var.get('b')-var.get('Math').callprop('floor', var.get('b'))))
    var.put('y', (var.get('a')-var.get('Math').callprop('floor', var.get('a'))))
    pass
    var.put('AB', ((((-Js(0.5))*var.get('x'))-var.get('y'))+Js(0.5)))
    if (var.get('AB')>Js(0.0)):
        var.put('FA', ((((-Js(2.0))*var.get('x'))-var.get('y'))+Js(1.0)))
        if (var.get('FA')>Js(0.0)):
            var.put('i', var.get('Math').callprop('floor', var.get('a')))
            var.put('j', var.get('Math').callprop('floor', var.get('b')))
        else:
            var.put('i', var.get('Math').callprop('floor', var.get('a')))
            var.put('j', (var.get('Math').callprop('floor', var.get('b'))+Js(1.0)))
    else:
        var.put('AH', (var.get('x')-var.get('y')))
        if (var.get('AH')>Js(0.0)):
            var.put('GH', ((((-Js(0.5))*var.get('x'))-var.get('y'))+Js(1.0)))
            if (var.get('GH')>Js(0.0)):
                var.put('i', var.get('Math').callprop('floor', var.get('a')))
                var.put('j', (var.get('Math').callprop('floor', var.get('b'))+Js(1.0)))
            else:
                var.put('i', (var.get('Math').callprop('floor', var.get('a'))+Js(1.0)))
                var.put('j', (var.get('Math').callprop('floor', var.get('b'))+Js(1.0)))
        else:
            var.put('HJ', ((((-Js(2.0))*var.get('x'))-var.get('y'))+Js(2.0)))
            if (var.get('HJ')>Js(0.0)):
                var.put('i', (var.get('Math').callprop('floor', var.get('a'))+Js(1.0)))
                var.put('j', var.get('Math').callprop('floor', var.get('b')))
            else:
                var.put('i', (var.get('Math').callprop('floor', var.get('a'))+Js(1.0)))
                var.put('j', (var.get('Math').callprop('floor', var.get('b'))+Js(1.0)))
    var.put('i', var.get('offset'), '+')
    var.put('j', var.get('offset'), '+')
    return Js([var.get('i'), var.get('j')])
PyJsHoisted_ab2grid_.func_name = 'ab2grid'
var.put('ab2grid', PyJsHoisted_ab2grid_)
@Js
def PyJsHoisted_latLon2grid_(lat, lon, maxLat, step, offset, this, arguments, var=var):
    var = Scope({'lat':lat, 'lon':lon, 'maxLat':maxLat, 'step':step, 'offset':offset, 'this':this, 'arguments':arguments}, var)
    var.registers(['offset', 'lon', 'maxLat', 'grid', 'step', 'lat'])
    var.put('maxLat', (Js(70.0) if (var.get('maxLat')==var.get('undefined')) else var.get('maxLat')))
    var.put('step', (Js(0.01) if (var.get('step')==var.get('undefined')) else var.get('step')))
    var.put('offset', (Js(13034.0) if (var.get('offset')==var.get('undefined')) else var.get('offset')))
    var.put('grid', var.get('latLon2ab')(var.get('lat'), var.get('lon'), var.get('maxLat'), var.get('step')))
    return var.get('ab2grid')(var.get('grid').get('0'), var.get('grid').get('1'), var.get('offset'))
PyJsHoisted_latLon2grid_.func_name = 'latLon2grid'
var.put('latLon2grid', PyJsHoisted_latLon2grid_)
@Js
def PyJsHoisted_grid2latLonHex_(i, j, offset, maxLat, step, this, arguments, var=var):
    var = Scope({'i':i, 'j':j, 'offset':offset, 'maxLat':maxLat, 'step':step, 'this':this, 'arguments':arguments}, var)
    var.registers(['offset', 'latLon', 'a', 'abHex', 'maxLat', 'b', 'j', 'i', 'step'])
    var.put('maxLat', (Js(70.0) if (var.get('maxLat')==var.get('undefined')) else var.get('maxLat')))
    var.put('step', (Js(0.01) if (var.get('step')==var.get('undefined')) else var.get('step')))
    var.put('offset', (Js(13034.0) if (var.get('offset')==var.get('undefined')) else var.get('offset')))
    var.put('a', (var.get('i')-var.get('offset')))
    var.put('b', (var.get('j')-var.get('offset')))
    var.put('abHex', Js([Js([(var.get('a')+(Js(1.0)/Js(3.0))), (var.get('b')+(Js(1.0)/Js(3.0)))]), Js([(var.get('a')-(Js(1.0)/Js(3.0))), (var.get('b')+(Js(2.0)/Js(3.0)))]), Js([(var.get('a')-(Js(2.0)/Js(3.0))), (var.get('b')+(Js(1.0)/Js(3.0)))]), Js([(var.get('a')-(Js(1.0)/Js(3.0))), (var.get('b')-(Js(1.0)/Js(3.0)))]), Js([(var.get('a')+(Js(1.0)/Js(3.0))), (var.get('b')-(Js(2.0)/Js(3.0)))]), Js([(var.get('a')+(Js(2.0)/Js(3.0))), (var.get('b')-(Js(1.0)/Js(3.0)))])]))
    var.put('latLon', Js([]))
    #for JS loop
    var.put('i', Js(0.0))
    while (var.get('i')<var.get('abHex').get('length')):
        var.get('latLon').callprop('push', var.get('ab2latLon')(var.get('abHex').get(var.get('i')).get('0'), var.get('abHex').get(var.get('i')).get('1'), var.get('maxLat'), var.get('step')))
        # update
        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    return var.get('latLon')
PyJsHoisted_grid2latLonHex_.func_name = 'grid2latLonHex'
var.put('grid2latLonHex', PyJsHoisted_grid2latLonHex_)
var.put('earthR', Js(6371000.0))
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass
pass


# Add lib to the module scope
geom = var.to_python()