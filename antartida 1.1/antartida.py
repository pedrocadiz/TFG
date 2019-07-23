#!/usr/bin/python

from subprocess import run
from shutil import copy2
from forceCopy import copyTree
from glob import glob
from datetime import date, datetime, timedelta
import os

# A partir de aqui tienen que estar en la misma carpeta que antartida.py
from lei2rnx import lei2rnx
from estadillos_ant import estadillos_ant
from procesa import procesa
from MBD_leer_inclinometro import MBD_leer_inclinometro
from series_inclinometro_dia import series_inclinometro_dia
from dibujarseries_gp import dibujarseries_gp
from kalman import kalman
import constants as cts

# Ejemplo de llamada a la función
# antartida(049,050,2016)

def antartida(firstDay, lastDay, year):

    # Por seguridad borramos todos los preexistentes STA\\F1_*.CRD
    for OldF1 in glob(cts.pathSTA + "\\F1_*.CRD"): os.remove(OldF1)
    
    for ESTA in cts.listESTA: # Creamos los Rinex a partir de los Laica
        lei2rnx(cts.pathLaicaBrutos, cts.pathRinex, ESTA, firstDay, lastDay, year, "1")
        lei2rnx(cts.pathLaicaBrutos, cts.pathRinex, ESTA, firstDay, lastDay, year, "30")
        copyTree(cts.pathRinex + "\\24H_30seg\\" + ESTA, cts.pathEstadillos30s)
         
    currentDate = datetime(int(year),1,1) + timedelta(int(firstDay)-1)    # Primer dia
    finalDate   = datetime(int(year),1,1) + timedelta(int(lastDay))       # Ultimo dia dia

    while currentDate < finalDate: 
    
        currentJulianDay = currentDate.strftime('%j')
        currentYear = currentDate.strftime('%Y')
        
        # Creamos los estadillos  
        estadillos_ant(cts.pathEstadillos30s,"estaciones.dat",currentJulianDay,currentYear)
        # Procesamos con bernese para crear los \STA\F1*
        procesa(cts.pathLaicaBrutos, cts.pathGPSDATA, currentJulianDay, currentYear, cts.campaign)
        # Preparamos los datos para dibujarlos
        MBD_leer_inclinometro(cts.pathSTA, cts.pathInclinometro)
        # Dibujamos la grafica
        series_inclinometro_dia(cts.pathInclinometro, cts.pathInclinometro)
                   
        currentDate += timedelta(days=1) # Avanzamos al siguiente dia
        
    # Pasamos los archivos F1 a \\FICHEROS_FI
    for fileF1 in glob(cts.pathSTA + "\\F1_*"): copy2(fileF1, cts.pathAllF1 + "\\" + os.path.basename(fileF1))  
    
    MBD_leer_inclinometro(cts.pathAllF1, cts.pathSeries)   # Leemos el historio de F1 de \\FICHEROS_FI
    series_inclinometro_dia(cts.pathSeries, cts.pathSeries)# Y lo dibujamos       
    kalman(cts.pathInclinometro, cts.pathKalman)           # Llamamos a kalman.py
    dibujarseries_gp(cts.pathKalman, cts.pathKalman)       # Dibujamos la grafica
      
antartida(cts.diaInicio, cts.diaFinal, cts.yearProcesado)