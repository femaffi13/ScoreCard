import pandas as pd
import os
from funciones.mes_str import mesStr
import shutil

def copia(mes_int, mes_str, año):
    print('\n--------------- Copia a Administración ---------------')
    
    # -------------------- Break -------------------- #
    origen = f'1. Break/{año}/{mes_int}. {mes_str}/'
    destino = f'M:/FEDERICO/__data/__Scorecard/1. Break/{año}/{mes_int}. {mes_str}/'

    archivos = os.listdir(origen)
    archivos = [i for i in archivos if '.xlsx' in i]

    for archivo in archivos:
        shutil.copy(origen+archivo, destino+archivo)
    print("Archivos de Break copiados ✔")

    # -------------------- ScoreCard Electricas -------------------- #
    origen = f'2. ScoreCard/{año}/Electricas/{mes_int}. {mes_str}/'
    destino = f'M:/FEDERICO/__data/__Scorecard/2. ScoreCard/{año}/Electricas/{mes_int}. {mes_str}/'

    archivos = os.listdir(origen)
    for archivo in archivos:
        shutil.copy(origen+archivo, destino+archivo)
    print("Archivos de ScoreCard Electricas copiados ✔")

    # -------------------- ScoreCard Financieras -------------------- #
    origen = f'2. ScoreCard/{año}/Financieras/{mes_int}. {mes_str}/'
    destino = f'M:/FEDERICO/__data/__Scorecard/2. ScoreCard/{año}/Financieras/{mes_int}. {mes_str}/'

    archivos = os.listdir(origen)
    for archivo in archivos:
        shutil.copy(origen+archivo, destino+archivo)
    print("Archivos de ScoreCard Financieras copiados ✔")

    # -------------------- Efectividad -------------------- #
    origen = f'3. Efectividad/{año}/{mes_int}. {mes_str}/'
    destino = f'M:/FEDERICO/__data/__Scorecard/3. Efectividad/{año}/{mes_int}. {mes_str}/'

    archivos = os.listdir(origen)
    for archivo in archivos:
        shutil.copy(origen+archivo, destino+archivo)
    print("Archivos de Efectividad copiados ✔")