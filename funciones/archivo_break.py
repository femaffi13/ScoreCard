import pandas as pd
import os
#----------------------- LECTURA DE ARCHIVOS --------------------------------------------------#
# df_argenpesos= pd.read_excel('')
df_consumax= pd.read_excel('Control_Break/EMPRESAS/Consumax/Break_Consumax.xlsx')
df_corcial= pd.read_excel('Control_Break/EMPRESAS/Cordial/Break_Cordial.xlsx')
df_credicuotas= pd.read_excel('Control_Break/EMPRESAS/Credicuotas/Break_Credicuotas.xlsx')
df_credisol= pd.read_excel('Control_Break/EMPRESAS/Credisol/Break_Credisol.xlsx')
df_crednow= pd.read_excel('Control_Break/EMPRESAS/Crednow/Break_Crednow.xlsx')
# df_cristal= pd.read_excel('')
df_edemsa= pd.read_excel('Control_Break/EMPRESAS/Edemsa/Break_Edemsa.xlsx')
df_edersa= pd.read_excel('Control_Break/EMPRESAS/Edersa/Break_Edersa.xlsx')
df_mejorcredito= pd.read_excel('Control_Break/EMPRESAS/Mejor Crédito/Break_Mejor Crédito.xlsx')
df_qida= pd.read_excel('Control_Break/EMPRESAS/Qida/Break_Qida.xlsx')

#------------------------------------------------------------------------------------------------#

writer = pd.ExcelWriter('archivo1.xlsx')
# df_argenpesos.to_excel(writer, sheet_name="argenpesos", index=False)
df_consumax.to_excel(writer, sheet_name="consumax", index=False)
df_corcial.to_excel(writer, sheet_name="cordial", index=False)
df_credicuotas.to_excel(writer, sheet_name="credicuotas", index=False)
df_credisol.to_excel(writer, sheet_name="credisol", index=False)
df_crednow.to_excel(writer, sheet_name="crednow", index=False)
# df_cristal.to_excel(writer, sheet_name="cristal", index=False)
df_edemsa.to_excel(writer, sheet_name="edemsa", index=False)
df_edersa.to_excel(writer, sheet_name="edersa", index=False)
df_mejorcredito.to_excel(writer, sheet_name="mejorcredito", index=False)
df_qida.to_excel(writer, sheet_name="qida", index=False)

writer.save()
writer.close()

__import__('archivo_unico.py')

print('Archivo creado correctamente')