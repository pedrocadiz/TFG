#!/usr/bin/python

from datetime import date, datetime, timedelta
import os
from subprocess import run
from glob import glob
import constants as cts

def lei2rnx( pathIn, pathOut, ESTA, firstDay, lastDay, year, frec):

    #  Genera archivos RINEX de 24 horas a la frecuencia especificada para los
    #  dias indicados, a partir de archivos brutos de Leica.
    
    #  pathIn   = Directorio donde se encuentran los archivos brutos de Leica (ej. C:\Descaga_WIFI).
    #  pathOut  = Directorio de salida en el que se guardarán 
    #  ESTA     = Codigo de la estacion de 4 caracteres
    #  firstDay = Dia de inicio con 3 dígitos
    #  lastDay  = Dia de fin con 3 dígitos
    #  year     = year
    #  frec     = frecuencia de los datos en los archivos de 24 horas (los de 3
    #             horas siempre son a 1 seg)
    
    # Ejemplo de llamada:
    # lei2rnx("C:\\Descarga_WIFI","C:\\Users\\astronomia\\Desktop\\pruebasMAT","BEGC","020","020","2017","1")
    
    currentDate = datetime(int(year),1,1) + timedelta(int(firstDay)-1)  # Primer dia
    finalDate = datetime(int(year),1,1) + timedelta(int(lastDay))       # Ultimo dia dia
    pathOut = pathOut + "\\24H_" + frec + "seg\\" + ESTA                # Directorio de salida 

    while currentDate < finalDate:

        if not os.path.exists(pathOut): # Creamos el directorio sino existe
            os.makedirs(pathOut)
        listFiles = glob(pathIn + "\\" + ESTA + "\\" + ESTA + currentDate.strftime('%j') + "?.m??") # ls ?.m??
        stringOfFiles = ' '.join(listFiles)              # Pasa la lista anterior a un solo sting
        nameFile = ESTA + currentDate.strftime('%j') + "0." + currentDate.strftime('%y')
        
        teqc = cts.pathTEQC + " -O.mo \"" + ESTA + "\" -O.ag \"LAGC\" -O.o \"LAGC\" -O.obs \"C1L1P2L2\" -O.dec " + frec + " +nav " + pathOut + "\\" + nameFile + "n +obs " + pathOut + "\\" + nameFile + "o " + stringOfFiles
        run(teqc)
    
        currentDate += timedelta(days=1) # Avanzamos al siguiente dia
    os.chdir(pathOut)  # Nos posicionamos en la carpeta destino 