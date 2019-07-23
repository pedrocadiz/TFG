#!/usr/bin/python

from glob import glob
import os
import string
from datetime import date, datetime, timedelta
from pathlib import Path


#######################################################################
#
#  MBD_leer_inclinometro(pathIn,pathOut)
#
#  Lee las coordenadas ajustadas cada media hora, y las guarda
#  en un archivo llamado F1_ESTA_inisi-finsf_serie.dat
#  Los archivos de entrada se llaman: F1_yyddds.crd.
#
#  OBSERVACIONES: Los archivos tienen que empezar por F1_
#                 ESTA = Nombre de la estación.
#                 inisf = "ini" (ddd), el día GPS con tres dígitos. "si" son dos dígitos que determinan la parte centesimal del día.
#                 finsf = "fin" (ddd), el día GPS con tres dígitos. "sf" son dos dígitos que determinan la parte centesimal del día.
#
#  NOTA: Todas las variables son tipo texto y tienen que ir entre ' '.
#
#  pathIn = directorio de entrada. (string)
#  pathOut = directorio de salida. (string)
#
#  Ejemplo:
#  MBD_leer_inclinometro("C:\BERNESE\GPSDATA\INCLI_2H\STA","C:\Inclinometro")
#
#  El archivo de salida contiene la información por columnas, organizada de la
#  siguiente manera:
#
#  yyddd ss        X              Y              Z       F (1 si se ha procesado y 0 si no)
#  08201 08  5035246.5223   -767657.0488   3826194.3634  1
#  08201 16  5035246.5231   -767657.0485   3826194.3639  0
#  ..... ..  ............   ............   ............  .
#
#######################################################################

def MBD_leer_inclinometro(pathIn,pathOut):

    print(" Analizando archivos F1 year actual: \n")

    # TODO: Esto no asegura que listFiles este ordenado, asume que glob los busca alfabeticamente
    listFiles = glob(pathIn + "\F1_*.CRD") # ls F1_*.CRD
    startSession = listFiles[0][-10:-4]
    lastSession = listFiles[len(listFiles)-1][-10:-4]

    currentDate = datetime(int("20" + startSession[0:2]),1,1) + timedelta(int(startSession[2:5])-1) # Primer dia
    finalDate   = datetime(int("20" + lastSession[0:2]),1,1)  + timedelta(int(lastSession[2:5]))    # Ultimo dia dia
    hours = list(string.ascii_lowercase) # Todo el abecedario
    hours = hours[:24]                   # Hasta la "x"
    # Parte centesimal del dia correspondiente a cada sesion.
    ss = ["04","08",12,16,20,24,29,33,37,41,45,49,54,58,62,66,70,74,79,83,87,91,95,99]
    endHead = "NUM  STATION NAME           X (M)          Y (M)          Z (M)     FLAG"

    firstSessionWithSS = startSession[:-1] + str(ss[ord(startSession[-1:]) - ord('a')])
    lastSessionWithSS = lastSession[:-1] + str(ss[ord(lastSession[-1:]) - ord('a')])
    flagShowDisplay = 1
    
    pathFileBEGC = pathOut + "\\F1__BEGC_" + firstSessionWithSS + "-" + lastSessionWithSS + "_serie.dat"
    pathFilePEND = pathOut + "\\F1__PEND_" + firstSessionWithSS + "-" + lastSessionWithSS + "_serie.dat"
    pathFileFUMA = pathOut + "\\F1__FUMA_" + firstSessionWithSS + "-" + lastSessionWithSS + "_serie.dat"
    
    fileBEGC = open(pathFileBEGC, "w")
    filePEND = open(pathFilePEND, "w")
    fileFUMA = open(pathFileFUMA, "w")

    firstFlag = 1
    while currentDate < finalDate: 
        ssIndex = 0
        for hour in hours: 
            
            pathCRD = "\\F1_" + currentDate.strftime('%y') + currentDate.strftime('%j') + hour + ".CRD"
            if os.path.isfile(pathIn + pathCRD):  # Comprobamos que hay datos de la hora hour
            
                file = open(pathIn + pathCRD,"r") # Abrimos el archivo

                CRD = file.read().splitlines()     # Y lo dividimos en lineas en la RAM
                file.close() 
                
                flagHead = 0
                for line in CRD: # Leemos linea por linea el archivo .CRD

                    if flagHead == 0 and line == endHead: # Esto para saltarnos la cabecera  
                        flagHead = 1
                        continue                          # Saltamos la linea de la cabecera 
                    if len(line) > 1 and flagHead == 1:   # Saltamos lineas vacias
                    
                        lineSplit = line.split()  
                        if lineSplit[1] == "BEGC": # Comprobamos el Flag y guardamos todo en el archivo correspondiente
                            if len(lineSplit) == 7 and (lineSplit[6] == 'A' or  lineSplit[6] == 'W'): flag = '1' 
                            else: flag = '0'                       
                            fileBEGC.write(currentDate.strftime('%y') + currentDate.strftime('%j') + " " + str(ss[ssIndex]) + "  " + lineSplit[3] + "  " + lineSplit[4] + "  " + lineSplit[5] + "  " + flag + "\n")
                        if lineSplit[1] == "FUMA":
                            if len(lineSplit) == 7 and (lineSplit[6] == 'A' or  lineSplit[6] == 'W'): flag = '1' 
                            else: flag = '0'
                            fileFUMA.write(currentDate.strftime('%y') + currentDate.strftime('%j') + " " + str(ss[ssIndex]) + "  " + lineSplit[3] + "  " + lineSplit[4] + "  " + lineSplit[5] + "  " + flag + "\n")
                        if lineSplit[1] == "PEND":
                            if len(lineSplit) == 7 and (lineSplit[6] == 'A' or  lineSplit[6] == 'W'): flag = '1' 
                            else: flag = '0'
                            filePEND.write(currentDate.strftime('%y') + currentDate.strftime('%j') + " " + str(ss[ssIndex]) + "  " + lineSplit[3] + "  " + lineSplit[4] + "  " + lineSplit[5] + "  " + flag + "\n")

                ssIndex = ssIndex + 1                                      
            else:
                # Si se quiere mostrar los archivos que fallan, es bastante lento 
                #print("No se pudo abrir el archivo " + pathCRD) 
                ssIndex = ssIndex + 1  
                
        currentDate += timedelta(days=1) # Avanzamos al siguiente dia
        
        if flagShowDisplay or currentDate.strftime('%Y') != previousYear:
            flagShowDisplay = 0
            previousYear = currentDate.strftime('%Y')
            print("    " + previousYear)
        
    fileBEGC.close()
    fileFUMA.close()
    filePEND.close()

        
#MBD_leer_inclinometro("C:\\bernese\\GPSDATA\\INCLI_2H\\STA","C:\\Inclinometro\\pruebaspedro")
#probar para leer_fichero_F1
#MBD_leer_inclinometro("C:\Inclinometro\RES2008-2017\FICHEROS_FI","C:\\Inclinometro\\pruebaspedro")