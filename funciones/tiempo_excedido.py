import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
from datetime import date
from datetime import datetime
import dataframe_image as dfi
import os 

#------------------------------#
inicio = '25/11/2022'
#------------------------------#

dia_inicio = inicio[:2]
dia_fin = str(date.today())[-2:]

os.system('cls')
mes = 'Noviembre'
ruta = 'C:/Users/fmaffi/Desktop/7. Break_ScoreCard/Score_Empresas/Noviembre - Electricas'
lista = os.listdir(f'{ruta}')
lista = [x for x in lista if '~$' not in x and 'Baño' not in x and 'Tiempo excedente' not in x and 'Noviembre' not in x]

def tiempo_total(i):
    """ Retorna el tiempo excedente pasados los 15 minutos """
    if pd.notna(i):
        hora2 = "15:00"
        formato = "%M:%S"
        
        h1 = datetime.strptime(i, formato)
        h2 = datetime.strptime(hora2, formato)
        
        resultado = h1 - h2
        if resultado.total_seconds() > 0:
            return resultado
        else:
            return np.nan 
    else:
        return np.nan

df_base = pd.DataFrame({})

for archivo in lista:
    #Lectura del archivo
    df = pd.read_excel(f'{ruta}/{archivo}')
    empresa = archivo[6:12]

    df = df[['Fecha', 'Operador', 'Break', 'p_Break', 'Contactos_Efectivos', 'p_CE', 'Promesas', 'p_Promesas',
            'Score', '$']].replace(0, np.nan)
         
    df.dropna(thresh=3, inplace=True)

    df = df[df['Fecha'] >= f'{inicio}']
    print(df['Fecha'].value_counts())

    #Lista de operadores a iterar
    operadores = list(df['Operador'].unique())

    for i in operadores:
        df_2 = df[df['Operador'].str.contains(f'{i}')]
        df_2['x'] = df_2['Break'].apply(tiempo_total)
        tiempo = str(df_2['x'].sum())
        tiempo = tiempo[-9:]
        df_excedido = pd.DataFrame({
            'Operador': [i],
            'Tiempo': [tiempo],
            'Empresa': [empresa]
        })

        df_base = pd.concat([df_base, df_excedido])

    print(f'{empresa} concatenado correctamente ✔')

df_base.replace('0.0', np.nan, inplace=True)
df_base = df_base[['Empresa', 'Operador', 'Tiempo']]
df_base.sort_values('Tiempo', ascending=False, inplace=True)
df_base.reset_index(drop=True, inplace=True)
df_base.dropna(inplace=True)

dfi.export(df_base, f'{ruta}/Tiempo excedente/{dia_inicio} al {dia_fin} de {mes}.jpg')
print('.jpg creada correctamente ✔')
df_base.to_excel(f'{ruta}/Tiempo excedente/{dia_inicio} al {dia_fin} de {mes}.xlsx', index=False)
print('Excel creado correctamente ✔')