#!/usr/bin/python
#---------------- Variables manuales------------------------------

#---------- Fechas para llamar a antartida() -------------
diaInicio     = 1       # dia juliano inicial
diaFinal      = 2       # dia juliano final
yearProcesado = 2017    # year del procesamiento
#---------------------------------------------------------

campaign = 'INCLI_2H'                # Nombre de la campana 
listESTA = [ "BEGC", "FUMA", "PEND"] # lista de codigos de 4 simbolos de las estaciones

#------------ Fin de las variables manuales -----------------------
    
# path necesarios, en principio no tocar
    
pathLaicaBrutos   = "C:\\Descarga_WIFI" 
pathRinex         = "C:\\Descarga_WIFI\\RINEX"  

pathGPSDATA       = "C:\\bernese\\GPSDATA"
pathSTA           = "C:\\bernese\\GPSDATA\\INCLI_2H\\STA"

pathEstadillos30s = "C:\\IESID-ESTADILLOS\\RINEX_24H_30seg"

pathInclinometro  = "C:\\Inclinometro"
pathAllF1         = "C:\\Inclinometro\\RES2008-2017\\FICHEROS_FI"
pathSeries        = "C:\\Inclinometro\\RES2008-2017\\series"
pathKalman        = "C:\\Inclinometro\\kalman"

pathTEQC          = "C:\\MATLAB2008\\work\\teqc"  
pathPL            = "C:\\MATLAB2008\\WORK\\PROCESAR\\INC_AUT.pl"