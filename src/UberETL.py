from pymongo import MongoClient

client = MongoClient()
db = client['UberDataset']
print("Conexión exitosa")
def ValidarDatos(datos):
    if 'fare_amount' not in datos or 'pickup_datetime' not in datos or 'pickup_longitude' not in datos or 'pickup_latitude' not in datos or 'dropoff_longitude' not in datos or 'dropoff_latitude' not in datos or 'passenger_count' not in datos:
        return False
    else:
        return True


while True:
    collection = db['UberRide']
    print("1.- Mostrar todos los viajes")
    print("2.- Salir")
    switch = int(input("Opción: "))
    if switch == 1:
        datos=collection.find()
        for ride in datos:
            if ValidarDatos(ride):
                print("\nTarifa: "+str(ride['fare_amount'])+"\nFecha: "+str(ride['pickup_datetime'])+"\nLongitud inicial: "+str(ride['pickup_longitude'])+"\nLatitud inicial: "+str(ride['pickup_latitude'])+"\nLongitud final: "+str(ride['dropoff_longitude'])+"\nLatitud final: "+str(ride['dropoff_latitude'])+"\nCantidad pasajeros: "+str(ride['passenger_count']))
    elif switch == 2:
        break
