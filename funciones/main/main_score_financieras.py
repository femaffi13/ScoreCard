import pandas as pd
from funciones.graficos import graficos
from funciones.operadores.consumax import usuarios_consumax
pd.options.mode.chained_assignment = None  # default='warn'
from funciones.formacion_score_financieras import formacion_score_financieras

def score_financieras(reporte_ivr, reporte_loan, mes_int, mes_str, año):
    #------------------- USUARIOS --------------------#
    usuarios = [
                usuarios_consumax(),
                ]

    empresas = [
                'CONSUMAX',
                ]
    #--------------------------------------------------#
    print('\n--------------- ScoreCard Financieras ---------------')

    for i in range(len(usuarios)):
        usuarios_var = usuarios[i]
        empresa = empresas[i]
        formacion_score_financieras(reporte_ivr, reporte_loan, usuarios_var, empresa, mes_int, mes_str, año)

    #graficos()