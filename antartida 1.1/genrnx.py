#!/usr/bin/python

from glob import glob
from datetime import date, datetime, timedelta
from subprocess import run
import constants as cts
########################################################################
#  Genera 1 archivo de 1 estacion de 1 hora a 1 segundo a partir de los archivos brutos
#  de Leica (puede haber mas de uno m00 m01...). Los RINEX resultantes los guarda en el 
#  directorio RAW de la campaña INCLI_2H del Bernese.
#
#  pathIn = Directorio donde se encuentran los archivos brutos de Leica (ej. C:\Descaga_WIFI).
#  pathOut = Directorio de salida en el que se guardarán (ej. C:\RINEX\RINEX').
#  ESTA  = Nombre de la estación
#  julianDay  = Día de inicio con 3 dígitos
#  year  = Año.
#  hour = 2 letras correspondientes a las horas que quiero concatenar.
#  campaing = nombre de la campana
# 
#  Ejemplo llamada: 
#  genrnx("C:\Descarga_WIFI","C:\BERNESE\GPSDATA","PEND","020","2017","a","INCLI_2H")
#
########################################################################

def genrnx(pathIn, pathOut, ESTA, julianDay, year, hour, campaing):
 
    listFiles = glob(pathIn + "\\" + ESTA + "\\" + ESTA + julianDay + hour + ".m??") # Equivalente a "ls ESTA*.m??"

    if listFiles: # Comprobamos que no este vacia la lista
    
        # Calculamos gpsWeek del julianDay  
        epoch = datetime.strptime("1980-01-07 00:00:00","%Y-%m-%d %H:%M:%S") 
        date = datetime(int(year),1,1) + timedelta(int(julianDay)-1) 
        currentTime = year + "-" + date.strftime('%m') + "-" + date.strftime('%d') + " 00:00:00"
        utc = datetime.strptime(currentTime,"%Y-%m-%d %H:%M:%S")
        diff = utc - epoch
        gpsWeek = int(diff.days/7)
        
        # Pasamos a llamar al teqc para crear el archivo de 1 hora a 1 segundo
        teqc = cts.pathTEQC + " -week \"" + str(gpsWeek) + "\" -O.mo \"" + ESTA + "\" -O.ag \"LAGC\" -O.o \"LAGC\" -O.obs \"C1L1P2L2\" -O.dec 1 +nav " +  pathOut + "\\" + campaing + "\ORX\AUTO" + julianDay + "0." + year[-2:] + "n +obs " + pathOut + "\\" + campaing + "\RAW\\" + ESTA + julianDay + "0." + year[-2:] + "o " + ' '.join(listFiles)
        run(teqc)