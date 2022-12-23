import pandas as pd 
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np 

#Agregar una columna con la empresa
def formacion_archivo(reporte, usuarios, empresa, mes_int, mes_str, año):
    df_reporte = pd.read_csv(f'reportes/{reporte}.csv', sep=';', encoding = "ISO-8859-1")
    df_reporte_descanso = df_reporte[df_reporte['Tipo Pausa'].str.contains('descanso')] #Filtro por descanso

    dia = reporte[-2:]
    mes = reporte[-5:-3]
    año = reporte[-10:-6]
    fecha = f'{dia}/{mes}/{año}' #La fecha depende de que el nombre del archivo de reporte_ivr la tenga
    
    df_reporte_descanso['Fecha_fin'] = pd.to_datetime(df_reporte_descanso['Fecha_fin'])
    df_reporte_descanso['Fecha inicio'] = pd.to_datetime(df_reporte_descanso['Fecha inicio'])

    df_reporte_descanso['Break'] = df_reporte_descanso['Fecha_fin'] - df_reporte_descanso['Fecha inicio'] #Diferencia
    df_reporte_descanso['Break'] = df_reporte_descanso['Break'].astype(str).str[10:] #Me quedo con los minutos y segundos

    df_reporte_descanso.Operador = df_reporte_descanso.Operador.str.upper() #Convierto a mayúsculas la columna de OPERADOR

    apellido_nombre = []
    usuarios_ivr = []
    
    for k, item in usuarios.items():
        apellido_nombre.append(item[0])
    for k, item in usuarios.items():
        usuarios_ivr.append(item[1])
    #-----------------------------------N
    def asigna_id_ivr(i):
        for key, item in usuarios.items():
            if item[1] == i:
                return key
    df_reporte_descanso['ID'] = df_reporte_descanso['Operador'].apply(asigna_id_ivr)

    #Filtros por operador
    operadores_ivr = pd.DataFrame({'Operador': []})
    operadores_ivr['Operador'] = apellido_nombre

    def asigna_id_ivr2(i):
        for key, item in usuarios.items():
            if item[0] == i:
                return key
    operadores_ivr['ID'] = operadores_ivr['Operador'].apply(asigna_id_ivr2)
    
    try:
        df_merge = operadores_ivr.merge(df_reporte_descanso, on='ID', how='left')
    except:
        operadores_ivr['Operador_x'] = np.nan
        operadores_ivr['Fecha inicio'] = np.nan
        operadores_ivr['Fecha_fin'] = np.nan
        operadores_ivr['Break'] = np.nan
        df_merge = operadores_ivr
    #-----------------------------------#

    operadores_ivr = df_merge[['ID', 'Operador_x', 'Fecha inicio', 'Fecha_fin', 'Break']]
    operadores_ivr.rename({'Operador_x': 'Operador'}, axis=1, inplace=True)

    #Pasar a segundos
    def segundos(i):
        try: 
            min = int(i[:2])
            min = min*60
            seg = int(i[3:])
            resultado = min+seg
            return resultado    
        except:
            return 0            

    operadores_ivr['segundos'] = operadores_ivr['Break'].apply(segundos)

    operadores_ivr.sort_values('ID', inplace=True)

    def asigna_nombre(i):
        for key, item in usuarios.items():
            if key == i:
                return item[0]
    operadores_ivr['Operador'] = operadores_ivr['ID'].apply(asigna_nombre)

    def cumplimiento(i):
        try: 
            i = int(i[:2])
            if i < 2:
                return 'Inválido'
            elif i >= 2 and i < 16:
                return 'Cumple'
            else:
                return 'No Cumple'
        except:
            return 'Sin Registro'
    operadores_ivr['Resultado'] = operadores_ivr['Break'].apply(cumplimiento)
    
    operadores_ivr.reset_index(drop=True)

    operadores_ivr['Empresa'] = empresa
    operadores_ivr['Fecha'] = fecha 

    def horario(i):
        return i[10:]

    operadores_ivr['Fecha inicio'] = operadores_ivr['Fecha inicio'].apply(str)
    operadores_ivr['Fecha_fin'] = operadores_ivr['Fecha_fin'].apply(str)
    operadores_ivr['Fecha inicio'] = operadores_ivr['Fecha inicio'].apply(horario)
    operadores_ivr['Fecha_fin'] = operadores_ivr['Fecha_fin'].apply(horario)

    operadores_ivr = operadores_ivr[['Fecha', 'Operador', 'Fecha inicio', 'Fecha_fin', 'Break', 'Resultado', 'Empresa']]
    operadores_ivr.rename({'Fecha inicio': 'Hora inicio',
                           'Fecha_fin': 'Hora fin',
                           'Break': 'Break Total'}, axis=1, inplace=True)

    operadores_ivr.to_excel(f'1. Break/{año}/{mes_int}. {mes_str}/temp/Break_{empresa}.xlsx', index=False)