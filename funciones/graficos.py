import pandas as pd 
import numpy as np
import os 
import matplotlib.pyplot as plt
import dataframe_image as dfi
#-------------------------------------#
import datetime
current_datetime = datetime.datetime.now()
current_datetime = current_datetime.strftime('%d/%m/%Y')
current_datetime = str(current_datetime)
dia = current_datetime[:2]
mes = current_datetime[3:5]
año = current_datetime[6:10]
#-------------------------------------#
valores_edersa = [12, 5]
valores_edemsa = [30, 18]
valores_edenor = [30, 18]
valores_edesur = [30, 18]

def graficos():
    lista = os.listdir('C:/Users/fmaffi/Desktop/7. Break_ScoreCard/Score_Empresas/Noviembre - Electricas')
    lista_2 = [i for i in lista if 'Score' in i] #Lista de archivos Score

    #-------------------- Tablas --------------------#
    lista_dfs = []
    #En cada iteración se genera un df de cada empresa
    for i in lista_2:
        df = pd.read_excel(f'C:/Users/fmaffi/Desktop/7. Break_ScoreCard/Score_Empresas/Noviembre - Electricas/{i}')
        empresa = i[6:12]

        df = df[['Fecha', 'Operador', 'Break', 'p_Break', 'Contactos_Efectivos', 'p_CE', 'Promesas', 'p_Promesas',
                 'Score', '$']].replace(0, np.nan)
            
        df.dropna(subset=['Contactos_Efectivos', 'p_CE',
                          'Promesas', 'p_Promesas', 'Score', '$'], inplace=True)

        df = df.groupby('Operador').agg({'Score': 'sum', 
                                         '$': 'sum', 
                                         'Fecha': 'count', 
                                         'Promesas': 'sum',
                                         'Contactos_Efectivos': 'sum'}).reset_index()
                                        
        df['Empresa'] = empresa 
        df['Efectividad'] = round((df['Promesas'] / df['Contactos_Efectivos'] * 100), 2)
        lista_dfs.append(df)

    df_final = pd.concat([i for i in lista_dfs])
    df_final.rename({'Fecha': 'n_Dias'}, axis=1, inplace=True)
    df_final.sort_values(['Efectividad', 'Score'], ascending=False, inplace=True)
    df_final = df_final[['Operador', 'Empresa', 'n_Dias', 'Contactos_Efectivos',
                         'Promesas', 'Score', '$', 'Efectividad']]
    df_final.reset_index(drop=True, inplace=True)
    #Indice iniciando el 1
    df_final.index = np.arange(1, len(df_final) + 1)

    #Genero la imagen del df ordenado por Efectividad
    dfi.export(df_final, f'Score_Empresas/imagenes/efectividad_{dia}{mes}{año}.jpg')
    print('Tabla de Efectividad creado correctamente ✔')

    #Genero la imagen del df ordenado por Puntaje
    df_final.sort_values('Score', ascending=False, inplace=True)
    dfi.export(df_final, f'Score_Empresas/imagenes/puntajes_{dia}{mes}{año}.jpg')
    print('Tabla de Puntajes creado correctamente ✔')
    #-------------------------------------------------------#

    #-------------------- Comparativos ---------------------#
    lista_dfs = []
    for i in lista_2:
        df = pd.read_excel(f'C:/Users/fmaffi/Desktop/7. Break_ScoreCard/Score_Empresas/Noviembre - Electricas/{i}')
        empresa = i[6:12]
        df = df.groupby(['Fecha']).agg({'Score': 'sum',
                                        'Promesas': 'sum',
                                        'Contactos_Efectivos': 'sum'}).reset_index()

        df['Fecha'] = df['Fecha'].apply(lambda x : x[:5])
        df.rename({'Score': f'{empresa}'}, axis=1, inplace=True)
        lista_dfs.append(df)

    df_final = lista_dfs[0].merge(lista_dfs[1], on='Fecha', suffixes=('_0', '_1')).merge(lista_dfs[2], on='Fecha', suffixes=('_1', '_2')).merge(lista_dfs[3], on='Fecha', suffixes=('_2', '_3'))

    df_final['Edemsa - %'] = round(df_final['Promesas_0'] / df_final['Contactos_Efectivos_0'] * 100, 2)
    df_final['Edenor - %'] = round(df_final['Promesas_1'] / df_final['Contactos_Efectivos_1'] * 100, 2)
    df_final['Edersa - %'] = round(df_final['Promesas_2'] / df_final['Contactos_Efectivos_2'] * 100, 2)
    df_final['Edesur - %'] = round(df_final['Promesas_3'] / df_final['Contactos_Efectivos_3'] * 100, 2)
    
    #Gráfico
    fig, axes = plt.subplots(nrows=2, ncols=1)
    #---------------------------------------------------------------------------#
    axes[0].plot(df_final['Fecha'], df_final['Edenor - %'], color = 'tab:purple', marker = 'o', label = 'Edenor') #linestyle = 'dotted',
    axes[0].plot(df_final['Fecha'], df_final['Edesur - %'], color = 'tab:green', marker = 'o', label = 'Edesur') #linestyle = 'dotted',
    axes[0].plot(df_final['Fecha'], df_final['Edemsa - %'], color = 'tab:orange', marker = 'o', label = 'Edemsa') #linestyle = 'dotted',
    axes[0].plot(df_final['Fecha'], df_final['Edersa - %'], color = 'tab:blue', marker = 'o', label = 'Edersa') #linestyle = 'dotted',
    #Título del gráfico
    axes[0].set_title('Promesas/Contactos Efectivos por día', loc = "center", fontdict = {'fontsize':17, 'fontweight':'bold', 'color':'k'})
    #Títulos de los ejes
    axes[0].set_ylabel("%", fontdict = {'fontsize': 13, 'fontweight': 'bold', 'color': 'k'})
    #Info label
    axes[0].legend(loc = 'best', prop={'size': 13}) #upper right
    #Rejilla
    axes[0].grid(axis = 'y', color = 'gray', linestyle = 'dashed')
    #---------------------------------------------------------------------------#
    axes[1].plot(df_final['Fecha'], df_final['EDENOR'], color = 'tab:purple', marker = 'o', label = 'Edenor') #linestyle = 'dotted',
    axes[1].plot(df_final['Fecha'], df_final['EDESUR'], color = 'tab:green', marker = 'o', label = 'Edesur') #linestyle = 'dotted',
    axes[1].plot(df_final['Fecha'], df_final['EDEMSA'], color = 'tab:orange', marker = 'o', label = 'Edemsa') #linestyle = 'dotted',
    axes[1].plot(df_final['Fecha'], df_final['EDERSA'], color = 'tab:blue', marker = 'o', label = 'Edersa') #linestyle = 'dotted',
    #Título del gráfico
    axes[1].set_title('Sumatoria de puntos por día', loc = "center", fontdict = {'fontsize':17, 'fontweight':'bold', 'color':'k'})
    #Títulos de los ejes
    axes[1].set_ylabel("Score", fontdict = {'fontsize': 13, 'fontweight': 'bold', 'color': 'k'})
    #Info label
    axes[1].legend(loc = 'best', prop={'size': 13}) #upper right
    #Rejilla
    axes[1].grid(axis = 'y', color = 'gray', linestyle = 'dashed')
    #---------------------------------------------------------------------------#
    #Sólo los valores pasados al eje x
    plt.xticks(df_final['Fecha'])
    #Tamaño de gráfico
    plt.gcf().set_size_inches(15, 13)
    #Guardar imagen
    plt.savefig(f'Score_Empresas/imagenes/rendimiento_{dia}{mes}{año}.jpg')
    print('Gráfico de Rendimiento creado correctamente ✔')
    #-------------------------------------------------------#
    
    #-------------------- Comparación con objetivo ---------------------#
    lista_dfs = []
    lista_empresas = []
    #En cada iteración se genera un df de cada empresa
    for i in lista_2:
        df = pd.read_excel(f'C:/Users/fmaffi/Desktop/7. Break_ScoreCard/Score_Empresas/Noviembre - Electricas/{i}')
        empresa = i[6:12]
        lista_empresas.append(empresa)
        df = df[['Fecha', 'Operador', 'Break', 'p_Break', 'Contactos_Efectivos', 'p_CE', 'Promesas', 'p_Promesas',
                'Score', '$']].replace(0, np.nan)

        df.dropna(thresh=3, inplace=True)

        df = df.groupby(['Fecha']).agg({'Contactos_Efectivos': 'sum', 
                                            'Promesas': 'sum', 
                                            'Operador': 'count'}).reset_index()

        df['Fecha'] = df['Fecha'].apply(lambda x : x[:5])

        if empresa == 'EDERSA':
            df['ideal_CE'] = df['Operador'].apply(lambda x : x * valores_edersa[0])
            df['ideal_P'] = df['Operador'].apply(lambda x : x * valores_edersa[1])
        elif empresa == 'EDEMSA':
            df['ideal_CE'] = df['Operador'].apply(lambda x : x * valores_edemsa[0])
            df['ideal_P'] = df['Operador'].apply(lambda x : x * valores_edemsa[1])
        elif empresa == 'EDENOR':
            df['ideal_CE'] = df['Operador'].apply(lambda x : x * valores_edenor[0])
            df['ideal_P'] = df['Operador'].apply(lambda x : x * valores_edenor[1])
        elif empresa == 'EDESUR':
            df['ideal_CE'] = df['Operador'].apply(lambda x : x * valores_edesur[0])
            df['ideal_P'] = df['Operador'].apply(lambda x : x * valores_edesur[1])

        df['%_CE'] = round(df['Contactos_Efectivos'] / df['ideal_CE'] * 100, 2)
        df['%_P'] = round(df['Promesas'] / df['ideal_P'] * 100, 2)
        df.rename({'Operador': 'n_Operadores'}, axis=1, inplace=True)

        df = df[['Fecha', 'n_Operadores', 'ideal_CE',
                'Contactos_Efectivos', 'ideal_P', 'Promesas', '%_CE', '%_P']]

        lista_dfs.append(df)

    #Gráfico
    fig, axes = plt.subplots(nrows=4, ncols=1)
    for index, i in enumerate(lista_dfs):
        axes[index].plot(i['Fecha'], i['%_CE'], color='tab:blue', marker='o', label='% Contactos Efectivos') #linestyle = 'dotted',
        axes[index].plot(i['Fecha'], i['%_P'], color='tab:green', marker='o', label='% Promesas') #linestyle = 'dotted',
        axes[index].axhline(y=100, color='tab:red', linestyle='-')
        #Título del gráfico
        axes[index].set_title(f'{lista_empresas[index]}', loc="center", fontdict={'fontsize':17, 'fontweight':'bold', 'color':'k'})
        #Títulos de los ejes
        axes[index].set_ylabel("%", fontdict={'fontsize': 13, 'fontweight': 'bold', 'color': 'k'})
        #Info label
        axes[index].legend(loc='best', prop={'size': 14}) #upper right
        #Rejilla
        axes[index].grid(axis='y', color='gray', linestyle='dashed', linewidth=1.5)

    #Sólo los valores pasados al eje x
    plt.xticks(df_final['Fecha'])
    #Tamaño de gráfico
    plt.gcf().set_size_inches(15, 25)
    #Guardar imagen
    plt.savefig(f'Score_Empresas/imagenes/objetivo por empresa_{dia}{mes}{año}.jpg') #png}
    print('Gráfico de Comparación por objetivo creado correctamente ✔')
    #-------------------------------------------------------------------#

#graficos()