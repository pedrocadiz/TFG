#!/usr/bin/python

# Reproduccion del kalman.bat

from glob import glob
from shutil import copy2
from subprocess import run
import os


def kalman(pathDist, pathExe):
    
    fileFUMA = glob(pathDist + "\\dist_FUMA_???????????????.dat")   
    filePEND = glob(pathDist + "\\dist_PEND_???????????????.dat")
    os.chdir(pathExe) # Los exes asumen que estamos en pathExe por eso el cambio
    
    copy2(fileFUMA[0], pathExe + "\\zFUMA00.dat")
    copy2(filePEND[0], pathExe + "\\zPEND00.dat")# Pasamos los archivos a pathExe
    
    fileClist = open(pathExe + "\\clist.dat", "w")# Preparamos clist.dat para el 
    for file in glob(pathExe + "\\zFU*.dat"):     # primer xform con FUMA
        fileClist.write(os.path.basename(file))
    fileClist.close()
    
    run(pathExe + "\\xform.exe")
    
    fileClist = open(pathExe + "\\clist.dat", "w") # Para el segundo con PEND
    for file in glob(pathExe + "\\zPE*.dat"):
        fileClist.write(os.path.basename(file))
    fileClist.close()
    
    
    run(pathExe + "\\xform.exe")
    # Ejecutamos el resto de exes
    run(pathExe + "\\xstat.exe")
    run(pathExe + "\\kalman.exe")
    run(pathExe + "\\waver.exe")
    run(pathExe + "\\xdata.exe")
      
#kalman("C:\\Inclinometro","C:\\Inclinometro\\kalman")