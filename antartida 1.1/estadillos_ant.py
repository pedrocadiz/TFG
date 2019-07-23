#!/usr/bin/python

import matplotlib.pyplot as plt
from rinex import rinex
import matplotlib.cm as cm
import numpy as np
# []=estadillos_ant(pathe,fichin,dia,year)
#
# Genera un estadillo de todas las estaciones para un día determinado,
# a partir del contenido de los archivos RINEX. Coloca un "." si los
# datos están incompletos o no hay y "o" si está todo. Los intervalos
# son de 20 minutos.
#
# pathe  = Directorio de entrada donde se encuentran los archivo RINEX. (string)
# fichin = Fichero que contiene el nombre de las estaciones, en columna. (string)
# dia    = Día GPS para el que se realiza el estadillo. (string)
# year   = Año al que corresponde el día GPS. (string)
#estadillos_ant('C:\IESID-ESTADILLOS\RINEX_24H_30seg','estaciones.dat',dia,num2str(year));

def estadillos_ant(pathIn, fileESTA, day, year):

    # Primero leemos las estaciones del estaciones.dat
    pathToESTA = pathIn + "\\" + fileESTA
    file = open(pathToESTA,"r") 
    codESTA = file.read().splitlines()
    file.close() 
    #TODO: optimizar esto
    estadilloPEND = rinex("C:\IESID-ESTADILLOS\RINEX_24H_30seg","PEND",day,year)
    estadilloBEGC = rinex("C:\IESID-ESTADILLOS\RINEX_24H_30seg","BEGC",day,year)
    estadilloFUMA = rinex("C:\IESID-ESTADILLOS\RINEX_24H_30seg","FUMA",day,year)

    estadilloPEND = np.tile(estadilloPEND, (20, 1))
    estadilloBEGC = np.tile(estadilloBEGC, (20, 1))
    estadilloFUMA = np.tile(estadilloFUMA, (20, 1))

    estadillo = np.concatenate((estadilloBEGC,estadilloFUMA,estadilloPEND))
    
    z = estadillo
    
    #TODO: buscar como cambiar los colores, tiene que ser algo con cmap
    plt.imshow(z,extent=[0,24,0,3], aspect= "auto")

    plt.title("INCLINÓMETRO ESPACIAL IESID. Datos disponibles. Día: " + day + " Año: " + year + ".")   
    plt.xlabel("hora (20min)")

    ax = plt.gca();
    ax.set_xticks(np.arange(0, 25, 1));
    ax.set_yticks([0.5,1.5,2.5]);
    ax.set_xticklabels(np.arange(0, 25, 1));
    ax.set_yticklabels(["PEND","FUMA","BEGC"]);

    plt.savefig("C:\\IESID-ESTADILLOS\\GRAFICAS\\"+ year[-2:] + day +"_estadillo.png")
    plt.draw()
    plt.close()    

#estadillos_ant("C:\IESID-ESTADILLOS\RINEX_24H_30seg","estaciones.dat","020","2017")