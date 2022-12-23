import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
from funciones.funcion_baño import formacion_baño
from operadores.edersa import usuarios_edersa
from operadores.edemsa import usuarios_edemsa
from operadores.edenor import usuarios_edenor
from operadores.edesur import usuarios_edesur
import os 

#-------------------- Archivo --------------------#
# reporte = 'reporte_pausas_2022-11-24_2022-11-24'
# mes = 'Noviembre'
#-------------------------------------------------#

def baño(reporte, mes):
    #------------------- USUARIOS --------------------#
    usuarios = [
                usuarios_edersa(), 
                usuarios_edemsa(), 
                usuarios_edenor(), 
                usuarios_edesur()
                ]
                
    empresas = [
                'EDERSA', 
                'EDEMSA', 
                'EDENOR', 
                'EDESUR'
                ]
    #-------------------------------------------------#

    os.system('cls')
    for i in range(len(usuarios)):
        usuarios_var = usuarios[i]
        empresa = empresas[i]
        formacion_baño(reporte, usuarios_var, empresa, mes)