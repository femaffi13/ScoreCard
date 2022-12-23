import pandas as pd
import numpy as np

contador = 0
def tabla_efectividad(mes_int, mes_str, año):
    global contador 
    if contador == 0:
        print('\n--------------- Efectividad ---------------')
    contador += 1

    #------------------------------#
    valores_edersa = [15, 7]
    valores_edemsa = [23, 14]
    valores_edenor = [33, 18]
    valores_edesur = [35, 18]
    #------------------------------#

    empresas = ['EDEMSA', 'EDENOR', 'EDERSA', 'EDESUR']

    for i in empresas:
        archivo = f'2. ScoreCard/{año}/Electricas/{mes_int}. {mes_str}/Score_{i}_{mes_str}.xlsx'
        df = pd.read_excel(archivo)
        empresa = archivo[-21:-15]

        df = df[['Fecha', 'Operador', 'Break', 'p_Break', 'Contactos_Efectivos', 'p_CE', 'Promesas', 'p_Promesas',
                 'Score', '$']].replace(0, np.nan)

        df.dropna(thresh=3, inplace=True)

        df = df.groupby(['Operador']).agg({'Contactos_Efectivos': 'sum', 
                                           'Promesas': 'sum', 
                                           'Fecha': 'count',
                                           'Score': 'sum',
                                           '$': 'sum'}).reset_index()

        df['Contactos_Efectivos'] = df['Contactos_Efectivos'].apply(int)
        df['Promesas'] = df['Promesas'].apply(int)

        if i == 'EDEMSA':
            df['ideal_ContEfect'] = df['Fecha'].apply(lambda x : x * valores_edemsa[0])
            df['ideal_Promesas'] = df['Fecha'].apply(lambda x : x * valores_edemsa[1])
        elif i == 'EDENOR':
            df['ideal_ContEfect'] = df['Fecha'].apply(lambda x : x * valores_edenor[0])
            df['ideal_Promesas'] = df['Fecha'].apply(lambda x : x * valores_edenor[1])
        elif i == 'EDERSA':
            df['ideal_ContEfect'] = df['Fecha'].apply(lambda x : x * valores_edersa[0])
            df['ideal_Promesas'] = df['Fecha'].apply(lambda x : x * valores_edersa[1])
        elif i == 'EDESUR':
            df['ideal_ContEfect'] = df['Fecha'].apply(lambda x : x * valores_edesur[0])
            df['ideal_Promesas'] = df['Fecha'].apply(lambda x : x * valores_edesur[1])

        df['p_ContEfect'] = round(df['Contactos_Efectivos'] / df['ideal_ContEfect'] * 100, 2)
        df['p_Promesas'] = round(df['Promesas'] / df['ideal_Promesas'] * 100, 2)
        df['Efectividad'] = round((df['Promesas'] / df['Contactos_Efectivos'] * 100), 2)
        df.rename({'Fecha': 'Dias'}, axis=1, inplace=True)

        df = df[['Operador', 'Dias', 'Contactos_Efectivos', 'ideal_ContEfect',
                 'Promesas', 'ideal_Promesas', 'p_ContEfect', 'p_Promesas', 'Efectividad', 'Score', '$']]

        df.insert(0, "Empresa", empresa)
        df.sort_values('Efectividad', ascending=False, inplace=True)
        df.reset_index(drop=True, inplace=True)

        #Comisiona / No Comisiona
        def comision(x,y,z):
            if x >= 50 and y >= 50 and z >= 40:
                return 'SI'
            else:
                return 'NO'

        df['COMISIONA'] = df.apply(lambda x: comision(x.p_ContEfect, x.p_Promesas, x.Efectividad), axis=1)

        df.to_excel(f'./3. Efectividad/{año}/{mes_int}. {mes_str}/Efectividad_{i}_{mes_str}.xlsx', index=False)
        print(f"Archivo 'Efectividad_{i}_{mes_str}' ✔")