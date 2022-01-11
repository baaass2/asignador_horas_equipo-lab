import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta

#Quitar los milisegundos
hoy = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
hoy = datetime.strptime(hoy, "%Y-%m-%d %H:%M:%S")

def open_file():
    try:
        with open('data/queue.json', 'r') as file:
            queue = json.load(file)
    except IOError:
        queue = []

    return queue

def save_file(queue):

    with open('data/queue.json', 'w') as file:
        json.dump(queue, file, indent=4, default=str)



def formulario():

    queue = open_file()

    print('Ingresar en horas! \n')
    id_pro = input('ID del proyecto: ')
    t_prep_m = input('Tiempo de preparación de las muestras: ')
    t_prep_e = input('Tiempo de preparación del equipo: ')
    cant_m = input('Cantidad de muestras: ')
    t_por_m = input('Tiempo por muestra: ')

    data = {
        'id_proyeto': id_pro,
        'tiempo_total':(int(cant_m)*int(t_por_m))+int(t_prep_e),
        't_prep_m': int(t_prep_m),
        'fecha_solicitud': hoy,
        'fecha_asignada_inicio': 'null',
        'fecha_asignada_final': 'null',
        'finalizado':0
    }
    return data

def tiempo_disponible():
    
    queue = open_file()

    #Si la queue esta vacia, no ha habido horas asignadas.
    if (len(queue) ==  0):
        t_disponible=0
    
    else:
        #Array que contendrá el diccionario de las horas de tiempos vacios y la fecha inicial entre horas asignadas.
        t_disponible = []

        #Diccionario para guardar la información de
        data = {
            'fecha_inicial': 0,
            'horas_del_bloque': 0
        }
        t_operacion = hoy
        for i in range(0,len(queue)):
            #Delta entre tiempos iniciales y finales de bloques asiganados
            t_delta = datetime.strptime(queue[i]['fecha_asignada_inicio'], "%Y-%m-%d %H:%M:%S") - t_operacion 
            #Transformar bloques vacios entre el hoy y las fechas asignadas a horas
            t_delta_horas = t_delta.total_seconds()/3600
            data['fecha_inicial'] = t_operacion
            data['horas_del_bloque'] = t_delta_horas
            print(data)
            t_disponible.append(data)
            t_operacion = datetime.strptime(queue[i]['fecha_asignada_final'], "%Y-%m-%d %H:%M:%S")
    
    return t_disponible

def tiempo_ventana(data, t_disponible):
    t_inicial = data['t_prep_m'] + data['tiempo_total']
    #Como t_disponible es vacio, se asigna la hora para el primero en llegar.
    if t_disponible==0:
        asignar_hora(hoy, data, 0)    
    #De lo contrario, se revisa si el input cae en la ventana entre horas asignadas.
    else:
        for i in range(0,len(t_disponible)):
            #Si existe una ventana de duración mayor a la suma de la preparación de las muestras más tiempo total, se asigna la primera fecha de match.
            if t_disponible[i]['horas_del_bloque'] >= t_inicial:
                print("Se ha encontrado una ventana")
                asignar_hora(t_disponible[i]['fecha_inicial'], data, i)
                break

    return 0

def asignar_hora(fecha_inicial, data, posicion):

    queue=open_file()
    t_inicial = data['t_prep_m'] + data['tiempo_total']
    data['fecha_asignada_inicio'] = fecha_inicial + timedelta(hours=t_inicial)
    #Falta agregar el tiempo entre usos de equipo
    data['fecha_asignada_final'] = data['fecha_asignada_inicio'] + timedelta(hours=data['tiempo_total']) 

    queue.insert(posicion,data)
    save_file(queue)
    return 0
def main():

    # Calculo: ¿Tengo tiempo libre entre horas asignadas?
    t_disponible=tiempo_disponible()
    #Pedir Input
    data=formulario()
    # Calculo: Si existe una ventana de tiempo entre horas asignadas.
    tiempo_ventana(data, t_disponible)
    
        
    return 0

main()





