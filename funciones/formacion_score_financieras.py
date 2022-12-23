import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import os 
import numpy as np
import math 
#Contactos Efectivos, Promesas
consumax = [14, 6]

def formacion_score_financieras(reporte_ivr, reporte_loan, usuarios, empresa, mes_int, mes_str, año):
    df_reporte = pd.read_csv(f'reportes/{reporte_ivr}.csv', sep=';', encoding = "ISO-8859-1")
    #df_monitor = pd.read_excel(f'reportes/{reporte_loan}.xlsx', usecols=['Operador', 'Cont.tit.', 'Terceros', 'Promesas'])

    df_monitor = pd.read_html(f'reportes/{reporte_loan}.xls', encoding='utf-8')
    #Devuelve una lista con un único elemento que es el DataFrame
    df_monitor = df_monitor[0]
    new_header = df_monitor.iloc[0] #grab the first row for the header
    df_monitor = df_monitor[1:] #take the data less the header row
    df_monitor.columns = new_header #set the header row as the df_monitor header

    df_reporte_descanso = df_reporte[df_reporte['Tipo Pausa'].str.contains('descanso')] #Filtro por descanso
    df_reporte_descanso['Fecha_fin'] = pd.to_datetime(df_reporte_descanso['Fecha_fin']) #Convierto a datetime
    df_reporte_descanso['Fecha inicio'] = pd.to_datetime(df_reporte_descanso['Fecha inicio']) #Convierto a datetime
    df_reporte_descanso['Break'] = df_reporte_descanso['Fecha_fin'] - df_reporte_descanso['Fecha inicio'] #Diferencia entre fechas
    df_reporte_descanso['Break'] = df_reporte_descanso['Break'].astype(str).str[10:] #Me quedo con los minutos y segundos

    df_reporte_descanso.Operador = df_reporte_descanso.Operador.str.upper() #Convierto a mayúsculas la columna de OPERADOR

    apellido_nombre = []
    usuarios_ivr = []
    usuarios_loan = []
    mora = []

    for key, item in usuarios.items():
        apellido_nombre.append(item[0])
    for key, item in usuarios.items():
        usuarios_ivr.append(item[1])
    for key, item in usuarios.items():
        usuarios_loan.append(item[2])
    for key, item in usuarios.items():
        mora.append(item[3])

    #Filtros por operador
    operadores_loan = df_monitor[df_monitor.Operador.isin(usuarios_loan)]
    operadores_loan.reset_index(drop =True, inplace =True)
    operadores_ivr = df_reporte_descanso[df_reporte_descanso.Operador.isin(usuarios_ivr)]
    operadores_ivr.reset_index(drop =True, inplace =True)

    #-------------------- Operadores LOAN --------------------#
    #Convertir a int si es posible
    def conversion_int(i):
        try:
            return int(i)
        except:
            return np.NaN

    operadores_loan['Cont.tit.'] = operadores_loan['Cont.tit.'].apply(conversion_int)
    operadores_loan['Terceros'] = operadores_loan['Terceros'].apply(conversion_int)
    operadores_loan['Promesas'] = operadores_loan['Promesas'].apply(conversion_int)

    operadores_loan['Contactos_Efectivos'] = operadores_loan[['Cont.tit.','Terceros']].sum(axis= 1) #Contactos Efectivos
    def asigna_id_loan(i):
        for key, item in usuarios.items():
            if item[2] == i:
                return key
    operadores_loan['ID'] = operadores_loan['Operador'].apply(asigna_id_loan) #Agrego ID

    #operadores_loan['Fecha'] = pd.to_datetime(operadores_loan['Fecha'], errors='coerce')
    #operadores_loan['Fecha'] = operadores_loan['Fecha'].dt.strftime('%d/%m/%Y')
    operadores_loan = operadores_loan[['ID', 'Operador', 'Contactos_Efectivos', 'Promesas']]
    #-----------------------------------------------------------#

    #--------------------- Operadores IVR ----------------------#
    def asigna_id_ivr(i):
        for key, item in usuarios.items():
            if item[1] == i:
                return key
    operadores_ivr['ID'] = operadores_ivr['Operador'].apply(asigna_id_ivr)

    operadores_ivr = operadores_ivr[['ID', 'Operador', 'Break']]
    #-----------------------------------------------------------#
    
    #--------------------- Operadores IVR ----------------------#
    def asigna_mora(i):
        for key, item in usuarios.items():
            if item[1] == i:
                return item[3]
    
    #print('OPERADORES_IVR')
    #print(operadores_ivr)
    try:
        operadores_ivr['MORA'] = operadores_ivr['Operador'].apply(asigna_mora)
    except:
        pass 

    operadores_mora = operadores_ivr[['ID', 'Operador', 'MORA']]

    #print(operadores_mora)
    #-----------------------------------------------------------#

    #--------------------- Base ----------------------#
    base = pd.DataFrame({'Operador': []})
    base['Operador'] = apellido_nombre

    def asigna_id_ivr2(i):
        for key, item in usuarios.items():
            if item[0] == i:
                return key
    base['ID'] = base['Operador'].apply(asigna_id_ivr2)
     #Tomo la fecha del reporte de ivr
    dia = reporte_ivr[-2:]
    mes_num = reporte_ivr[-5:-3]
    año = reporte_ivr[-10:-6]
    fecha = f'{dia}/{mes_num}/{año}'

    base['Fecha'] = fecha 
    #-------------------------------------------------#

    #--------------------------- Merge -------------------------#
    df_merge = base.merge(operadores_loan, on='ID', how='left')
    df_merge.drop('Operador_y', axis=1, inplace=True)
    df_merge.rename({'Operador_x': 'Operador'}, axis=1, inplace=True)
    df_merge = df_merge.merge(operadores_ivr, on='ID', how='left')
    df_merge.drop('Operador_y', axis=1, inplace=True)
    df_merge.rename({'Operador_x': 'Operador'}, axis=1, inplace=True)
    df_merge = df_merge.merge(operadores_mora, on='ID', how='left')
    df_merge.drop('Operador_y', axis=1, inplace=True)
    df_merge.rename({'Operador_x': 'Operador'}, axis=1, inplace=True)
    
    df_merge.sort_values(by=['ID'], inplace=True)
    def cumplimiento(i):
        try: 
            i = int(i[:2])
            if i < 2:
                return 'Inválido'
            elif i >= 2 and i < 16:
                return 'Cumple'
            else:
                return 'No cumple'
        except:
            return 'Sin Registro'

    df_merge['Resultado'] = df_merge['Break'].apply(cumplimiento)

    df_merge = df_merge[['Fecha', 'Operador', 'Break', 'Resultado', 'Contactos_Efectivos', 'Promesas', 'MORA_x']]
         
    #-----------------------------------------------------------#
    #Dropeo los inválidos
    df = df_merge.drop(df_merge[df_merge['Resultado'].str.contains('Inválido')].index)
       
    if empresa == 'CONSUMAX':
       contactos_efectivos = [consumax[0], 30]
       promesas = [consumax[1], 40]
       breaks = [30]
       
    #Ponderados
    def ponderado_ce(i):
        if math.isnan(i): 
            return 0
        else:
            resultado = (i * contactos_efectivos[1]) / contactos_efectivos[0]
            return round(resultado, 2)
        
    df['p_CE'] = df['Contactos_Efectivos'].apply(ponderado_ce)

    def ponderado_promesas(i):
        try:
            i = int(i)
        except:
            i = np.NaN
        
        if math.isnan(i): 
            return 0
        else:
            resultado = (i * promesas[1]) / promesas[0]
            return round(resultado, 2)
    
    df['p_Promesas'] = df['Promesas'].apply(ponderado_promesas)
    
    def ponderado_break(i):
        if i == 'Cumple':
            return breaks[0]
        else: 
            return 0
    
    df['p_Break'] = df['Resultado'].apply(ponderado_break)

    #Si hay 0 puntos en el break, son 0 puntos.
    def score_break(i):
        if pd.isna(i):
            return 0 
        else:
            return '-'

    df['Score'] = df['Break'].apply(score_break)

    def score_suma(a,x,y,z):
        if a == 0:
            return a 
        elif a == '-':
            return round(x + y + z)

    df.sort_values('Break', ascending=False, inplace=True)
    df.drop_duplicates('Operador', keep='first', inplace=True)

    df['Score'] = df.apply(lambda x: score_suma(x.Score, x.p_CE, x.p_Promesas, x.p_Break), axis=1)

    #df['Score'] = round(df['p_CE'] + df['p_Promesas'] + df['p_Break'])
    df['Score'] = df['Score'].astype(int)


    score_tardia = list(range(40, 159))
    monto_tardia = list(range(0, 830, 7))

    score_temprana = list(range(40, 159))
    monto_temprana = list(range(0, 595, 5))

    #Tomar en cuenta los de Mora Temprana/Tardía/Refis
    df.rename({'MORA_x': 'MORA'}, axis=1, inplace=True)

    #print('df')
    #print(df)

    lista_mora = list(df['MORA'].unique())

    #print(lista_mora)

    df_base = pd.DataFrame({})    

    for i in lista_mora:
        if i == 'TARDIA':
            score = list(range(40, 159))
            monto = list(range(0, 830, 7))
        elif i == 'TEMPRANA':
            score = list(range(40, 159))
            monto = list(range(0, 595, 5))
        elif i == 'REFIS':
            score = list(range(40, 159))
            monto = list(range(0, 356, 3))

        df_3 = pd.DataFrame(df[df['MORA'].str.contains(f'{i}', na=False)])

        df_pago = pd.DataFrame({
            'Score': score,
            '$': monto,
        })
    
        df_3 = df_3.merge(df_pago, on='Score', how='left')
        df_base = pd.concat([df_base, df_3])

    df_base.rename({'$': 'pesos'}, axis=1, inplace=True)

    def pesos_cero2(i, j):
        if i >= 158:
            return monto_tardia[-1] 

        if math.isnan(j):
            return 0
        else:
            return j

    df_base['pesos'] = df_base.apply(lambda x: pesos_cero2(x.Score, x.pesos), axis=1)

    df_base.rename({'pesos': '$'}, axis=1, inplace=True)
    
    df = df_base[['Fecha', 'MORA', 'Operador', 'Break', 'p_Break', 'Contactos_Efectivos', 'p_CE', 
    'Promesas', 'p_Promesas', 'Score', '$']]

    df.sort_values('Operador', inplace=True)

    electricas = ['EDENOR', 'EDESUR', 'EDEMSA', 'EDERSA']
    if empresa in electricas:
        if os.path.exists(f'./2. ScoreCard/{año}/Electricas/{mes_int}. {mes_str}/Score_{empresa}_{mes_str}.xlsx'):
            a_concatenar = pd.read_excel(f'./2. ScoreCard/{año}/Electricas/{mes_int}. {mes_str}/Score_{empresa}_{mes_str}.xlsx')
            df_concat = pd.concat([a_concatenar, df])
            df_concat.to_excel(f'./2. ScoreCard/{año}/Electricas/{mes_int}. {mes_str}/Score_{empresa}_{mes_str}.xlsx', index=False)
            print(f"Archivo 'Score_{empresa}_{mes_str}' concatenado ✔")
        else:
            df.to_excel(f'./2. ScoreCard/{año}/Electricas/{mes_int}. {mes_str}/Score_{empresa}_{mes_str}.xlsx', index=False)
            print(f"Archivo 'Score_{empresa}_{mes_str}' creado ✔")
        
    else:
        if os.path.exists(f'./2. ScoreCard/{año}/Financieras/{mes_int}. {mes_str}/Score_{empresa}_{mes_str}.xlsx'):
            a_concatenar = pd.read_excel(f'./2. ScoreCard/{año}/Financieras/{mes_int}. {mes_str}/Score_{empresa}_{mes_str}.xlsx')
            df_concat = pd.concat([a_concatenar, df])
            df_concat.to_excel(f'./2. ScoreCard/{año}/Financieras/{mes_int}. {mes_str}/Score_{empresa}_{mes_str}.xlsx', index=False)
            print(f"Archivo 'Score_{empresa}_{mes_str}' concatenado ✔")
        else:
            df.to_excel(f'./2. ScoreCard/{año}/Financieras/{mes_int}. {mes_str}/Score_{empresa}_{mes_str}.xlsx', index=False)
            print(f"Archivo 'Score_{empresa}_{mes_str}' creado ✔")
