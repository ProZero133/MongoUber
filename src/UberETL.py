from pymongo import MongoClient
from collections import defaultdict
import math

client = MongoClient()
db = client['UberDataset']
collection = db['UberRide']

def ValidarDatos(datos):
    required_fields = ['fare_amount', 'pickup_datetime', 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude', 'passenger_count']
    return all(field in datos for field in required_fields)

def redondear_coordenadas(coordenadas, decimales=2):
    return tuple(round(coord, decimales) for coord in coordenadas)

def haversine(lon1, lat1, lon2, lat2):
    R = 6371  # Radio de la Tierra en kilómetros
    dlon = math.radians(lon2 - lon1)
    dlat = math.radians(lat2 - lat1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def obtener_tarifa_promedio_por_pasajero():
    datos = collection.find()
    tarifas_por_pasajero = defaultdict(list)
    
    for ride in datos:
        if ValidarDatos(ride):
            distancia = haversine(
                ride['pickup_longitude'], ride['pickup_latitude'],
                ride['dropoff_longitude'], ride['dropoff_latitude']
            )
            tarifa = ride['fare_amount']
            pasajeros = ride['passenger_count']
            tarifas_por_pasajero[pasajeros].append((tarifa, distancia))
    
    for pasajeros, tarifas_distancias in tarifas_por_pasajero.items():
        total_tarifa = sum(tarifa for tarifa, _ in tarifas_distancias)
        total_distancia = sum(distancia for _, distancia in tarifas_distancias)
        promedio_tarifa = total_tarifa / len(tarifas_distancias)
        promedio_distancia = total_distancia / len(tarifas_distancias)
        print(f"Pasajeros: {pasajeros} - Tarifa Promedio: {promedio_tarifa:.2f} - Distancia Promedio: {promedio_distancia:.2f} km")

while True:
    print("1.- Mostrar todos los viajes")
    print("2.- Obtener promedio de la hora más repetida")
    print("3.- Obtener rango de las rutas más visitadas")
    print("4.- Obtener tarifa promedio por cantidad de pasajeros y distancia")
    print("5.- Salir")
    switch = int(input("Opción: "))
    
    if switch == 1:
        datos = collection.find()
        for ride in datos:
            if ValidarDatos(ride):
                print("\nTarifa: " + str(ride['fare_amount']) +
                      "\nFecha: " + str(ride['pickup_datetime']))
    elif switch == 3:
        decimales = int(input("Ingrese el número de decimales para redondear las coordenadas: "))
        obtener_rutas_mas_visitadas(decimales)
    elif switch == 4:
        obtener_tarifa_promedio_por_pasajero()
    elif switch == 5:
        break