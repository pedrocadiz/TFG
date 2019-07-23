#!/usr/bin/python
import string
from genrnx import genrnx
from subprocess import call
from glob import glob
import os
import constants as cts
#######################################################################
#
#  function [] = procesa(pathe,paths,dini,yyyy,campaing)
#
#  Lanza los procesados para un día y sesiones de 1 horas. En total,
#  procesará 24 sesiones. Al final de cada procesado, renombra la salida
#  para que no se pise con el siguiente procesado.
#
#  NOTA: Todas las variables son tipo texto y tienen que ir entre ' '.
#
#  pathe = Directorio donde se encuentran los archivos brutos de Leica (ej. C:\Descaga_WIFI).
#  paths = Directorio de salida en el que se guardarán (ej. C:\RINEX\RINEX').
#  dini  = Día de inicio con 3 dígitos
#  yyyy  = Año con 4 digitos
#  campaing = Camapaña (ej. INCLI_1H)
#
#  Esta función llama a genrnx(), MBD_leer_inclinometro() y MBD_series_inclinometro().
#
#  Ejemplo:
#  
#  procesa('C:\Descarga_WIFI','C:\BERNESE\GPSDATA','008','2009','INCLI_2H')
#  
# 
#   Orden para compilarlo:
#  mcc -m procesa.m genrnx.m leer_inclinometro.m series_inclinometro.m -d procesa
#
###########################################################################

def procesa(pathIn, pathOut, day, year, campaing):


    hours = list(string.ascii_lowercase) # Todo el abecedario
    hours = hours[:24] # Hasta la "x"
    shortYear = year[-2:]

    for hour in hours:

        print(" Generando RINEX a 1s")
        for ESTA in cts.listESTA:    # Rinex a 1s de las 3 estaciones de la hora hour    
            genrnx(pathIn, pathOut, ESTA, day, year, hour, campaing) 
            
        # Llamamos a bernese
        print("\n Sesion actual: " + day + hour)   
        call(["perl", cts.pathPL, year, day + "0 ", campaing])
        
        # Renombramos los archivos (son 8 renombramientos)
        print(" Renombrando archivos")
        tempPath = pathOut + "\\" + campaing
        
        # Renombramos los \STA\F1_yyddd0.CRD a \STA\F1_yyddds.CRD
        if os.path.isfile(tempPath + "\STA\F1_" + shortYear + day + hour + ".CRD"):
            os.remove(tempPath + "\STA\F1_" + shortYear + day + hour + ".CRD")
        if os.path.isfile(tempPath + "\STA\F1_" + shortYear + day + "0.CRD"):
            os.rename(tempPath + "\STA\F1_" + shortYear + day + "0.CRD",tempPath + "\STA\F1_" + shortYear + day + hour + ".CRD")
        
        # Renombramos los \STA\P1_yyddd0.CRD a \STA\P1_yyddds.CRD
        if os.path.isfile(tempPath + "\STA\P1_" + shortYear + day + hour + ".CRD"):
            os.remove(tempPath + "\STA\P1_" + shortYear + day + hour + ".CRD")
        if os.path.isfile(tempPath + "\STA\P1_" + shortYear + day + "0.CRD"):
            os.rename(tempPath + "\STA\P1_" + shortYear + day + "0.CRD", tempPath + "\STA\P1_" + shortYear + day + hour + ".CRD")
        
        # Renombramos los \STA\AM_yyddd0.CRD a \STA\AM_yyddds.CRD
        if os.path.isfile(tempPath + "\STA\AM_" + shortYear + day + hour + ".CRD"):
            os.remove(tempPath + "\STA\AM_" + shortYear + day + hour + ".CRD")        
        if os.path.isfile(tempPath + "\STA\AM_" + shortYear + day + "0.CRD"):
            os.rename(tempPath + "\STA\AM_" + shortYear + day + "0.CRD", tempPath + "\STA\AM_" + shortYear + day + hour + ".CRD")
            
        # Renombramos los \OUT\QIFyyddd0.OUT a \OUT\QIFyyddds.OUT
        if os.path.isfile(tempPath + "\OUT\QIF" + shortYear + day + hour + ".OUT"):
            os.remove(tempPath + "\OUT\QIF" + shortYear + day + hour + ".OUT")
        if os.path.isfile(tempPath + "\OUT\QIF" + shortYear + day + "0.OUT"):
            os.rename(tempPath + "\OUT\QIF" + shortYear + day + "0.OUT", tempPath + "\OUT\QIF" + shortYear + day + hour + ".OUT")        
        
        # Renombramos los \OUT\F1_yyddd0.OUT a \OUT\F1_yyddds.OUT
        if os.path.isfile(tempPath + "\OUT\F1_" + shortYear + day + hour + ".OUT"):
            os.remove(tempPath + "\OUT\F1_" + shortYear + day + hour + ".OUT")
        if os.path.isfile(tempPath + "\OUT\F1_" + shortYear + day + "0.OUT"):
            os.rename(tempPath + "\OUT\F1_" + shortYear + day + "0.OUT", tempPath + "\OUT\F1_" + shortYear + day + hour + ".OUT")
        
        # Renombramos los \SOL\EDTddd0001.NQ0 a \SOL\EDTddds001.NQ0
        if os.path.isfile(tempPath + "\SOL\EDT" + day + hour + "001.NQ0"):
            os.remove(tempPath + "\SOL\EDT" + day + hour + "001.NQ0")
        if os.path.isfile(tempPath + "\SOL\EDT" + day + "0001.NQ0"):
            os.rename(tempPath + "\SOL\EDT" + day + "0001.NQ0", tempPath + "\SOL\EDT" + day + hour + "001.NQ0")
        
        # Renombramos los \SOL\F1_yyddd0.NQ0 a \SOL\F1_yyddds.NQ0
        if os.path.isfile(tempPath + "\SOL\F1_" + shortYear + day + hour + ".NQ0"):
            os.remove(tempPath + "\SOL\F1_" + shortYear + day + hour + ".NQ0")
        if os.path.isfile(tempPath + "\SOL\F1_" + shortYear + day + "0.NQ0"):
            os.rename(tempPath + "\SOL\F1_" + shortYear + day + "0.NQ0", tempPath + "\SOL\F1_" + shortYear + day + hour + ".NQ0")
        
        # Renombramos los \SOL\P1_yyddd0.NQ0 a \SOL\P1_yyddds.NQ0
        if os.path.isfile(tempPath + "\SOL\P1_" + shortYear + day + hour + ".NQ0"):
            os.remove(tempPath + "\SOL\P1_" + shortYear + day + hour + ".NQ0")
        if os.path.isfile(tempPath + "\SOL\P1_" + shortYear + day + "0.NQ0"):   
            os.rename(tempPath + "\SOL\P1_" + shortYear + day + "0.NQ0", tempPath + "\SOL\P1_" + shortYear + day + hour + ".NQ0")

#procesa("C:\Descarga_WIFI","C:\BERNESE\GPSDATA","020","2017","INCLI_2H")


