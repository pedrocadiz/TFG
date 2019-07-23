#!/usr/bin/python
# TODO: que el nombre de la imagen al guardarlo ponga la fecha de inicio y final
from glob import glob
import calendar
import os
from math import sqrt
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import datetime


def series_inclinometro_dia(pathIn, pathOut):
    listFiles = [os.path.basename(x) for x in glob(pathIn + "\F1_*.dat")] # ls F1_*.dat
    startDay = listFiles[0][-25:-18]
    lastDay = listFiles[0][-17:-10]

    for filename in listFiles:
    
        ESTA = filename[4:8]
        if ESTA != "BEGC":
            flagFirstSession = 1
            file = open(pathIn + "\\" + filename, "r")
            F1dat = file.read().splitlines()     # Metemos en RAM el archivo
            file.close()
            epoca = [None] * len(F1dat) # Reservamos memoria para las epocas 
            dist  = [None] * len(F1dat) # (puede que reservemos de mas)
            distm = [None] * len(F1dat)
            index = 0
            
            for line in F1dat:
                lineSplit = line.split()  

                if lineSplit[5] == "1": #Comprobamos que el flag es 1

                    # Primero tomamos las coordenadas restandoles a 
                    # cada una la coordenada de BEGC y calculamos la distancia euclidea
                    dist[index] = sqrt((float(lineSplit[2]) - 1423027.7842)**2 + (float(lineSplit[3]) + 2533144.0078)**2 + (float(lineSplit[4]) + 5658977.7603)**2)
                    # Ahora le restamos la distancia de FUMA o PEND para ver la diferencia
                    if ESTA == "FUMA": distm[index] = (dist[index] - 2888.060)*100
                    else:              distm[index] = (dist[index] - 6305.805)*100
                    # Guardamos la primera y la ultima sesion para el nombre del archivo
                    if flagFirstSession:
                        firstSession = lineSplit[0][:2] + lineSplit[0][2:] + lineSplit[1]
                        flagFirstSession = 0
                    lastSession = lineSplit[0][:2] + lineSplit[0][2:] + lineSplit[1]
                    # Pasamos a calcular epoca = parte decimal del ano AVISAR DEL FALLO EN EL MATLAB
                    year = int(2000 + int(lineSplit[0][:2]))
                    if calendar.isleap(year): # Comprobamos si el ano es bisiesto                  
                        oneDayOnDecimalPartYear   = 2.73224043712617e-003 # 1/366
                    else: oneDayOnDecimalPartYear = 2.73972602739726e-003 # 1/365                   
                    #              year +  julianDay - 1                                    + parte decimal del dia
                    epoca[index] = year + (int(lineSplit[0][2:])-1)*oneDayOnDecimalPartYear + int(lineSplit[1])*oneDayOnDecimalPartYear/100
                    index = index + 1
                    
            # Guardamos datos en  "dist_PEND_1702004-1702095.dat"
            file = open(pathOut + "\\dist_" + ESTA + "_" + firstSession + "-" + lastSession + ".dat", "w")
            indexWrite = 0
            for epocaWrite in epoca: 
                if(epocaWrite): # no es if(not epocaWrite): por ser tipo none (creo)
                    file.write("   " + str('{:.7e}'.format(epocaWrite)) + "   " + str('{:.7e}'.format(dist[indexWrite])) + "\n")
                indexWrite = indexWrite + 1
            file.close()

            # Creamos la figura
            # Esta parte para poder poner en la grafica el dia/mes en vez del ano en parte decimal
            def update_ticksX(x, pos):
                julianDay = int((x-int(x))/oneDayOnDecimalPartYear) + 1 # +1 para contrarestar el -1 del "julianDay - 1"
                julianDay = str(year) + str(julianDay)
                month = str(datetime.datetime.strptime(julianDay, '%Y%j').month)
                day = str(datetime.datetime.strptime(julianDay, '%Y%j').day)
                return(day + "/" + month)

            fig, ax = plt.subplots()  
            
            ax.plot(epoca, distm, 'k.', markersize = 2, label = "Variación en distancia")
            ax.legend(loc = "upper center")
            
            if index > 8000 : # Para el archivo con miles de F1
                ax.xaxis.set_ticks(range(int(epoca[0]),int(epoca[index - 1] + 1),1))
                ax.set_xlabel('Tiempo (years)') 
                
            else: # Para el de unos dias
                ax.xaxis.set_major_formatter(mticker.FuncFormatter(update_ticksX)) # Cambiar el formato del eje x sin cambiar los datos
                ax.set_xlabel('Tiempo (dias)') 

            ax.grid(True, axis='y',linestyle='-')
            ax.set_facecolor("lightgreen") # Color del background de la grafica
            ax.set_xlim(epoca[0],epoca[index - 1])            
            ax.set_ylim(-10, 10)
            ax.yaxis.set_ticks(range(-10, 11, 2))
            ax.set_ylabel('Distancia (cm)')        
            ax.set_title("INCLINÓMETRO ESPACIAL IESID.  (BEGCᵣₑ," + ESTA + ")" )
            
            # Borramos si hubiera una imagen con el mismo nombre y guardamos la nueva
            imageName = pathOut + "\\dist_" + ESTA + "_" + firstSession + "-" + lastSession +".png"
            if os.path.isfile(imageName):
                os.remove(imageName)
            plt.savefig(imageName)
            plt.draw()
            plt.close()
            
#series_inclinometro_dia("C:\Inclinometro","C:\Inclinometro\pruebaspedro")
#probar con dibujarseries
#series_inclinometro_dia("C:\Inclinometro\RES2008-2017\series","C:\Inclinometro\pruebaspedro")