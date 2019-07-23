#!/usr/bin/python

# Crea la grafica dis_ESTA a partir de los datos en los archivos \oESTA00

from glob import glob
import os
from math import floor
import matplotlib.pyplot as plt

def dibujarseries_gp(pathIn, pathOut):
   
    listFiles = [os.path.basename(x) for x in glob(pathIn + "\\o*00.dat")] # ls \o*00.dat
    
    for filename in listFiles:
        
        ESTA = filename[1:5]
        file = open(pathIn + "\\" + filename, "r")
        oFile = file.read().splitlines()     # Metemos en RAM el archivo
        file.close()
        
        epoca = [None] * len(oFile) # Reservamos memoria    
        DLGT  = [None] * len(oFile) 
        index = 0 
        flagFirst = 1
         
        for line in oFile:
            lineSplit = line.split()  
            
            if flagFirst: # Calculamos ini con epoca[0]
                ina = float(lineSplit[2])
                ine = (ina - 10) / 10 + 0.5
                ini = floor(ine)*10
                flagFirst = 0    
            
            epoca[index] = float(lineSplit[2]) - ini # Rellenamos las matrices
            DLGT[index]  = float(lineSplit[6]) * 100
            index = index +1
            
        # Creamos la figura
        fig, ax = plt.subplots() 
        ax.plot(epoca, DLGT, 'k.', markersize = 2, label = "Variación en distancia")
        ax.legend(loc = "upper center")
        ax.set_xlim(0,120)            
        ax.set_ylim(-8, 8)
        ax.set_title("INCLINÓMETRO ESPACIAL IESID.  (BEGC - " + ESTA + ")" )
        ax.grid(True, axis='y',linestyle='-')
        ax.set_facecolor("lightgreen") # Color del background de la grafica
        ax.set_xlabel('Tiempo (years)') 
        ax.set_ylabel('Distancia (cm)')
        
        # Borramos si hubiera una imagen con el mismo nombre y guardamos la nueva
        imageName = pathOut + "\\dist_" + ESTA + ".png"
        if os.path.isfile(imageName):
            os.remove(imageName)
        plt.savefig(imageName)        
        plt.show()

#dibujarseries_gp("C:\Inclinometro\kalman","C:\Inclinometro\pruebaspedro")