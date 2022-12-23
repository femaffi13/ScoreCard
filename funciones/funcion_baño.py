import pandas as pd
import os 

def formacion_baño(reporte, usuarios, empresa, mes):
    df_reporte = pd.read_csv(f'reportes/{reporte}.csv', sep=';', encoding = "ISO-8859-1")
    
    df_reporte_baño = df_reporte[df_reporte['Tipo Pausa'].str.contains('baño')] #Filtro por descanso
    df_reporte_baño['Fecha_fin'] = pd.to_datetime(df_reporte_baño['Fecha_fin']) #Convierto a datetime
    df_reporte_baño['Fecha inicio'] = pd.to_datetime(df_reporte_baño['Fecha inicio']) #Convierto a datetime
    df_reporte_baño['Baño'] = df_reporte_baño['Fecha_fin'] - df_reporte_baño['Fecha inicio'] #Diferencia entre fechas
    df_reporte_baño['Baño'] = df_reporte_baño['Baño'].astype(str).str[10:] #Me quedo con los minutos y segundos

    df_reporte_baño.Operador = df_reporte_baño.Operador.str.upper() #Convierto a mayúsculas la columna de OPERADOR

    apellido_nombre = []
    usuarios_ivr = []

    for key, item in usuarios.items():
        apellido_nombre.append(item[0])
    for key, item in usuarios.items():
        usuarios_ivr.append(item[1])

    operadores_ivr = df_reporte_baño[df_reporte_baño.Operador.isin(usuarios_ivr)]
    operadores_ivr.reset_index(drop =True, inplace =True)

    def asigna_id_ivr(i):
        for key, item in usuarios.items():
            if item[1] == i:
                return key
    operadores_ivr['ID'] = operadores_ivr['Operador'].apply(asigna_id_ivr)

    operadores_ivr = operadores_ivr[['ID', 'Operador', 'Fecha inicio', 'Fecha_fin', 'Baño']]
    
    #--------------------- Base ----------------------#
    base = pd.DataFrame({'Operador': []})
    base['Operador'] = apellido_nombre

    def asigna_id_ivr2(i):
        for key, item in usuarios.items():
            if item[0] == i:
                return key
    base['ID'] = base['Operador'].apply(asigna_id_ivr2)
        #Tomo la fecha del reporte de ivr
    dia = reporte[-2:]
    mes_num = reporte[-5:-3]
    año = reporte[-10:-6]
    fecha = f'{dia}/{mes_num}/{año}'

    base['Fecha'] = fecha 

    #--------------------------- Merge -------------------------#
    df_merge = base.merge(operadores_ivr, on='ID', how='left')
    df_merge.sort_values(by=['ID'], inplace=True)

    df_merge = df_merge[['Fecha', 'Operador_x', 'Fecha inicio', 'Fecha_fin', 'Baño']]

    df_merge.rename({'Operador_x': 'Operador',
                     'Fecha_fin': 'Fecha fin'}, axis=1, inplace=True)

    if os.path.exists(f'./Score_Empresas/Noviembre - Electricas/Baño/Baño_{empresa}_{mes}.xlsx'):
        a_concatenar = pd.read_excel(f'./Score_Empresas/Noviembre - Electricas/Baño/Baño_{empresa}_{mes}.xlsx')
        df_concat = pd.concat([a_concatenar, df_merge])
        df_concat.to_excel(f'./Score_Empresas/Noviembre - Electricas/Baño/Baño_{empresa}_{mes}.xlsx', index=False)
        print(f"Archivo 'Baño_{empresa}_{mes}' concatenado correctamente")
    else:
        df_merge.to_excel(f'./Score_Empresas/Noviembre - Electricas/Baño/Baño_{empresa}_{mes}.xlsx', index=False)
        print(f"Archivo 'Baño_{empresa}_{mes}' creado correctamente")