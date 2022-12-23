import pandas as pd
import os 
import numpy as np
import math 
def formacion_score(reporte_ivr, reporte_loan, usuarios, empresa, mes_int, mes_str, año):
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
    for key, item in usuarios.items():
        apellido_nombre.append(item[0])
    for key, item in usuarios.items():
        usuarios_ivr.append(item[1])
    for key, item in usuarios.items():
        usuarios_loan.append(item[2])

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
    df_merge = df_merge.merge(operadores_ivr, on='ID', how='left')
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

    df_merge = df_merge[['Fecha', 'Operador_x', 'Break', 'Resultado', 'Contactos_Efectivos', 'Promesas']]
    #-----------------------------------------------------------#

    #Dropeo los inválidos
    df = df_merge.drop(df_merge[df_merge['Resultado'].str.contains('Inválido')].index)

    #df2 = df.groupby(['ID', 'Operador_x']).agg({'Break': 'max'}).reset_index()
    #--------#
    #df_operadores2_unicos = df_merge.groupby(['ID', 'Operador_x']).agg({'Break': 'max'}).reset_index()
    
    #SCORE
    #EDEMSA/EDENOR/EDESUR:
    # Promesas: 18, 50
    # C.E.: 30, 30
    # Break: 20

    #EDERSA
    # Promesas: 5, 50
    # C.E.: 12, 30
    # Break: 20

    if empresa == 'EDEMSA':
        #[cantidad, puntaje]
        contactos_efectivos = [23, 30]
        promesas = [14, 40]
        breaks = [30]
        #pagos = [7, 10]
    elif empresa == 'EDENOR':
        contactos_efectivos = [33, 30]
        promesas = [18, 40]
        breaks = [30]
    elif empresa == 'EDERSA':
        contactos_efectivos = [15, 30]
        promesas = [7, 40]
        breaks = [30]
    elif empresa == 'EDESUR':
        contactos_efectivos = [35, 30]
        promesas = [18, 40]
        breaks = [30]
    elif empresa == 'CONSUMAX':
        contactos_efectivos = [14, 30]
        promesas = [6, 40]
        breaks = [30]
       
    #Ponderados
    def ponderado_ce(i):
        if math.isnan(i): 
            return 0
        else:
            resultado = (i * contactos_efectivos[1]) / contactos_efectivos[0]
            return round(resultado, 2)
        # if resultado >= contactos_efectivos[1]:
        #     return contactos_efectivos[1]
        # else:
        #     return round(resultado, 2)
    #df_merge['%_ce'] = df_merge['Contactos_Efectivos'].apply(ponderado_ce)
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
        # if resultado >= promesas[1]:
        #     return promesas[1]
        # else:
        #     return round(resultado, 2)
    #df_merge['%_promesas'] = df_merge['Promesas'].apply(ponderado_promesas)
    df['p_Promesas'] = df['Promesas'].apply(ponderado_promesas)
    
    def ponderado_break(i):
        if i == 'Cumple':
            return breaks[0]
        else: 
            return 0
    #df_merge['%_break'] = df_merge['Resultado'].apply(ponderado_break)
    df['p_Break'] = df['Resultado'].apply(ponderado_break)

    # df_merge['Score'] = round(df_merge['%_ce'] + df_merge['%_promesas'] + df_merge['%_break'])
    # df_merge['Score'] = df_merge['Score'].astype(int)

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

    df['Score'] = df.apply(lambda x: score_suma(x.Score, x.p_CE, x.p_Promesas, x.p_Break), axis=1)

    #df['Score'] = round(df['p_CE'] + df['p_Promesas'] + df['p_Break'])
    df['Score'] = df['Score'].astype(int)

    #Suma para cerrar números
    # df_merge['Score2'] = df_merge['Score']+70
    #df['Score2'] = df['Score']+70

    # score = list(range(22, 101))
    # monto = list(range(100, 495, 5))
    # score = list(range(40, 140))
    # monto = list(range(0, 500, 5))
    score = list(range(40, 159))
    monto = list(range(0, 475, 4))

    df_pago = pd.DataFrame({
        'Score': score,
        '$': monto
    })

    df_inner = df.merge(df_pago, on='Score', how='left')

    
    df_inner.rename({'$': 'pesos'}, axis=1, inplace=True)

    def pesos_cero2(i, j):
        if i >= 158:
            return monto[-1] 

        if math.isnan(j):
            return 0
        else:
            return j

    df_inner['pesos'] = df_inner.apply(lambda x: pesos_cero2(x.Score, x.pesos), axis=1)

    df_inner.rename({'pesos': '$'}, axis=1, inplace=True)

    # def pesos_cero(i):
    #     if math.isnan(i):
    #         return 0
    #     else:
    #         return i
    # df_inner['$'] = df_inner['$'].apply(pesos_cero)
    
    # df_inner['Pagos'] = np.nan
    # df_inner['%_pagos'] = np.nan
    # df_inner['Recupero'] = np.nan
    # df_inner['%_recupero'] = np.nan

    # df = df_inner[['ID', 'Fecha', 'Break', '%_break', 'Contactos_Efectivos', '%_ce', 'Promesas', '%_promesas',
    # 'Pagos', '%_pagos', 'Recupero', '%_recupero', 'Score', 'Paga']]
    df = df_inner[['Fecha', 'Operador_x', 'Break', 'p_Break', 'Contactos_Efectivos', 'p_CE', 
    'Promesas', 'p_Promesas', 'Score', '$']]

    df.rename({'Operador_x': 'Operador'}, axis=1, inplace=True)

    # df = df[['Fecha', 'Nombre', 'Break', '%_break', 'Contactos_Efectivos', '%_ce', 'Promesas', '%_promesas',
    # 'Pagos', '%_pagos', 'Recupero', '%_recupero', 'Score', 'Paga']]
    
    electricas = ['EDENOR', 'EDESUR', 'EDEMSA', 'EDERSA']
    if empresa in electricas:
        # try:
        if os.path.exists(f'./2. ScoreCard/{año}/Electricas/{mes_int}. {mes_str}/Score_{empresa}_{mes_str}.xlsx'):
        #if os.path.exists(f'./Score_Empresas/Noviembre - Electricas/Score_{empresa}_{mes_str}.xlsx'):
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