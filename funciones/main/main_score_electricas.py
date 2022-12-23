import pandas as pd
from funciones.graficos import graficos
pd.options.mode.chained_assignment = None  # default='warn'
from funciones.formacion_score import formacion_score
from funciones.operadores.edersa import usuarios_edersa
from funciones.operadores.edemsa import usuarios_edemsa
from funciones.operadores.edenor import usuarios_edenor
from funciones.operadores.edesur import usuarios_edesur
import os

def score_electricas(reporte_ivr, reporte_loan, mes_int, mes_str, año):
    #------------------- USUARIOS --------------------#
    usuarios = [
                usuarios_edersa(), 
                usuarios_edemsa(), 
                usuarios_edenor(), 
                usuarios_edesur(),
                ]

    empresas = [
                'EDERSA',
                'EDEMSA',
                'EDENOR',
                'EDESUR',
                ]
    #--------------------------------------------------#
    #os.system('cls')
    print('\n--------------- ScoreCard Electricas ---------------')
    for i in range(len(usuarios)):
        usuarios_var = usuarios[i]
        empresa = empresas[i]
        formacion_score(reporte_ivr, reporte_loan, usuarios_var, empresa, mes_int, mes_str, año)

    #graficos()