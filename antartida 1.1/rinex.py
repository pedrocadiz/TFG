#!/usr/bin/python

from datetime import date, datetime, timedelta
import os
# Lee un archivo RINEX y devuelve una matriz rellena de 0 y 1 donde 
# cada 0 significa que no hay datos 1 si hay datos.
# Ejemplo de llamada:
# rinex('C:\IESID-ESTADILLOS\RINEX_24H_30seg','BEGC','020','2017')

def rinex(pathIn, ESTA, day, year):

    # Metemos en RAM el archivo
    fileName = ESTA + day + "0." + year[-2:] +"o"
    pathToRINEX = pathIn + "\\" + fileName
    file = open(pathToRINEX,"r")
    rinex = file.read().splitlines()
    file.close() 

    # Para localizar las horas nos fijamos en el segundo caracter de la linea
    endHead = "                                                            END OF HEADER"
    flagHead = 0  
    flagHour = 0
    estadillo = [None] * 2880 # Creamos la lista para la info del estadillo
    estadilloReducido = [None] * 144 # Creamos la lista reducida
    index = 0
    # Inicializamos un dia hora 00:00:00
    dayOnSeconds = datetime(2000,1,1)
    lineDateAnterior = [0,0,0,'0','0','0'] # Lo inicializamos a las 00:00:00 por si faltan datos al principio
    
    for line in rinex:
    
        if flagHead == 0 and line == endHead: flagHead = 1 # Esto para saltarnos la cabecera        
        if flagHead == 1 and len(line) > 2 and line[1] != ' ':
        
            lineDate = line.split()
            if len(lineDate[7]) > 2:

                if lineDate[3] == str(int(dayOnSeconds.strftime('%H'))) and lineDate[4] == str(int(dayOnSeconds.strftime('%M'))) and str(int(float(lineDate[5]))) == str(int(dayOnSeconds.strftime('%S'))):               

                    # Coincide y por tanto hay datos
                    estadillo[index] = 1 
                    dayOnSeconds += timedelta(seconds=30) 
                    index = index + 1
                    
                else: # Vamos a contar el Gap pasandolo al formato format
                
                    format = "%H:%M:%S"     
                    fecha1 = lineDateAnterior[3] + ":" + lineDateAnterior[4] + ":" + str(int(float(lineDateAnterior[5])))
                    fecha2 = lineDate[3] + ":" + lineDate[4] + ":" + str(int(float(lineDate[5])))
                    deltaGap = datetime.strptime(fecha2, format) - datetime.strptime(fecha1, format)

                    for i in range(0,int(deltaGap.total_seconds()/30)):
                        estadillo[index] = 0 # Metemos en el estadio tantos 0 como Gaps hay
                        index = index + 1
                        
                    dayOnSeconds += deltaGap
                    
                lineDateAnterior = lineDate  
                   
    while index < 2880: # Faltarian datos al final
        estadillo[index] = 0 
        index = index + 1

    # Ahora condensaremos un poco los datos para poder mostrarlos por pantalla    
    contador = 0
    estado = 1
    index = 0
    for i in estadillo:
        contador += 1
        estado = estado * i
        if (contador%20) == 0:
            estadilloReducido[index] = estado
            index = index + 1
            estado = 1

    return(estadilloReducido)