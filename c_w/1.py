import math
from operator import itemgetter

def distancia(coord1, coord2):
    lat1 = coord1[0]
    lon1 = coord1[1]
    lat2 = coord2[0]
    lon2 = coord2[1]
    return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

def en_ruta(rutas, c):
    ruta = None
    for r in rutas:
        if c in r:
            ruta = r
    return ruta

def peso_ruta(ruta):
    total = 0
    for c in ruta:
        total = total + pedidos[c]
    return total

def obtener_datos_ciudad():
    ciudad = input("Ingrese el nombre de la ciudad (o presione Enter para finalizar): ")
    if not ciudad:
        return None, None, None
    latitud = float(input("Ingrese la latitud de la ciudad: "))
    longitud = float(input("Ingrese la longitud de la ciudad: "))
    paquetes = int(input("Ingrese la cantidad de paquetes en la ciudad: "))
    return ciudad, (latitud, longitud), paquetes

def vrp_voraz(coord, pedidos, max_carga):
    # Calcular los ahorros
    s = {}
    for c1 in coord:
        for c2 in coord:
            if c1 != c2:
                if not (c2, c1) in s:
                    d_c1_c2 = distancia(coord[c1], coord[c2])
                    d_c1_almacen = distancia(coord[c1], almacen)
                    d_c2_almacen = distancia(coord[c2], almacen)
                    s[c1, c2] = d_c1_almacen + d_c2_almacen - d_c1_c2

    # Ordenar Ahorros
    s = sorted(s.items(), key=itemgetter(1), reverse=True)

    # Construir rutas
    rutas = []
    for k, v in s:
        rc1 = en_ruta(rutas, k[0])
        rc2 = en_ruta(rutas, k[1])
        if rc1 == None and rc2 == None:
            # No están en ninguna ruta. Crear la ruta.
            if peso_ruta([k[0], k[1]]) <= max_carga:
                rutas.append([k[0], k[1]])
        elif rc1 != None and rc2 == None:
            # Ciudad 1 ya está en ruta. Agregar la ciudad 2
            if rc1[0] == k[0]:
                if peso_ruta(rc1) + peso_ruta([k[1]]) <= max_carga:
                    rutas[rutas.index(rc1)].insert(0, k[1])
            elif rc1[len(rc1) - 1] == k[0]:
                if peso_ruta(rc1) + peso_ruta([k[1]]) <= max_carga:
                    rutas[rutas.index(rc1)].append(k[1])
        elif rc1 == None and rc2 != None:
            # Ciudad 2 ya está en ruta. Agregar la ciudad 1
            if rc2[0] == k[1]:
                if peso_ruta(rc2) + peso_ruta([k[0]]) <= max_carga:
                    rutas[rutas.index(rc2)].insert(0, k[0])
            elif rc2[len(rc2) - 1] == k[1]:
                if peso_ruta(rc2) + peso_ruta([k[0]]) <= max_carga:
                    rutas[rutas.index(rc2)].append(k[0])
        elif rc1 != None and rc2 != None and rc1 != rc2:
            # Ciudad 1 y 2 ya están en una ruta.
            if rc1[0] == k[0] and rc2[len(rc2) - 1] == k[1]:
                if peso_ruta(rc1) + peso_ruta(rc2) <= max_carga:
                    rutas[rutas.index(rc2)].extend(rc1)
                    rutas.remove(rc1)
            elif rc1[len(rc1) - 1] == k[0] and rc2[0] == k[1]:
                if peso_ruta(rc1) + peso_ruta(rc2) <= max_carga:
                    rutas[rutas.index(rc1)].extend(rc2)
                    rutas.remove(rc2)
    return rutas

if __name__ == "__main__":
    coord = {}
    pedidos = {}
    almacen = (40.23, -3.40)
    max_carga = 40
    
    while True:
        ciudad, ciudad_coord, ciudad_paquetes = obtener_datos_ciudad()
        if ciudad is None:
            break
        coord[ciudad] = ciudad_coord
        pedidos[ciudad] = ciudad_paquetes

    rutas = vrp_voraz(coord, pedidos, max_carga)
    for ruta in rutas:
        print(ruta)
