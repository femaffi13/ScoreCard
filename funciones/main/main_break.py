import pandas as pd
from funciones.operadores.faroyfertil import usuarios_faroyfertil
from funciones.operadores.kalima import usuarios_kalima
from funciones.operadores.maycoop import usuarios_maycoop
from funciones.operadores.fiat import usuarios_fiat
from funciones.operadores.moovitech import usuarios_moovitech
pd.options.mode.chained_assignment = None  # default='warn'
from funciones.archivo_supervisor import archivo_supervisor
from funciones.operadores.antina import usuarios_antina
from funciones.operadores.edenor import usuarios_edenor
from funciones.operadores.edesur import usuarios_edesur
from funciones.operadores.argenpesos import usuarios_argenpesos
from funciones.operadores.consumax import usuarios_consumax
from funciones.operadores.credicuotas import usuarios_credicuotas
from funciones.operadores.credisol import usuarios_credisol
from funciones.operadores.crednow import usuarios_crednow
from funciones.operadores.cristalcash import usuarios_cristalcash
from funciones.formacion_archivo import formacion_archivo
from funciones.operadores.qida import usuarios_qida
from funciones.operadores.mejor_credito import usuarios_mejor_credito
from funciones.operadores.cordial import usuarios_cordial
from funciones.operadores.edersa import usuarios_edersa
from funciones.operadores.edemsa import usuarios_edemsa
from funciones.operadores.credipesos import usuarios_credipesos
from funciones.operadores.italcred import usuarios_italcred
import os

def tiempo_break(reporte, mes_int, mes_str, año):
    #------------------- Usuarios y Empresas --------------------#
    usuarios = [
                usuarios_qida(), 
                usuarios_mejor_credito(), 
                usuarios_cordial(),
                usuarios_consumax(),
                usuarios_credisol(),
                usuarios_crednow(),
                usuarios_credicuotas(),
                usuarios_edersa(),
                usuarios_edemsa(),
                usuarios_argenpesos(),
                usuarios_cristalcash(),
                usuarios_edenor(),
                usuarios_edesur(),
                usuarios_antina(),
                usuarios_fiat(),
                usuarios_maycoop(),
                usuarios_moovitech(),
                usuarios_faroyfertil(),
                usuarios_kalima(),
                usuarios_credipesos(),
                usuarios_italcred(),
                ]

    empresas = [
                'Qida', 
                'Mejor Crédito', 
                'Cordial', 
                'Consumax',
                'Credisol', 
                'Crednow', 
                'Credicuotas', 
                'Edersa', 
                'Edemsa', 
                'Argenpesos', 
                'Cristal Cash',
                'Edenor',
                'Edesur',
                'Antina',
                'Fiat',
                'Maycoop',
                'Moovitech',
                'Faro y Fertil',
                'Kalima',
                'Credipesos',
                'Italcred'
                ]
    #------------------------------------------------------------#
    os.system('cls')

    for i in range(len(usuarios)):
        usuarios_var = usuarios[i]
        empresa = empresas[i]
        formacion_archivo(reporte, usuarios_var, empresa, mes_int, mes_str, año)
    print('\n-------------------- Break ----------------------')
    archivo_supervisor(mes_int, mes_str, año)