from funciones.main.main_break import tiempo_break
from funciones.main.main_score_electricas import score_electricas
from funciones.main.main_score_financieras import score_financieras
#from funciones.main_baño import baño
from funciones.main.main_tabla_efectividad import tabla_efectividad
from funciones.mes_str import mesStr
from funciones.copia import copia
from datetime import datetime

# -------------------- Archivos -------------------- #
reporte_ivr = 'reporte_pausas_2022-12-22_2022-12-22'
reporte_loan = 'MonitorGestion23122022112341 '
# -------------------------------------------------- #

# ------- Fechas ------ #
#Cambiar las fechas luego de haber procesado todos los días del mes
mes = 12
año = 2022
mes_str = mesStr(mes)
# --------------------- #

# ------------------ Funciones ------------------------ #
tiempo_break(reporte_ivr, mes, mes_str, año)
score_electricas(reporte_ivr, reporte_loan, mes, mes_str, año)
score_financieras(reporte_ivr, reporte_loan, mes, mes_str, año)
#baño(reporte_ivr, mes_int)
tabla_efectividad(mes, mes_str, año)
copia(mes, mes_str, año)
# ----------------------------------------------------- #