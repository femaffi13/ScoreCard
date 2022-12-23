import pandas as pd
import os 
#os.system('cls')
def archivo_supervisor(mes_int, mes_str, año): 
    # --------------- Milagro --------------- #
    df_argenpesos= pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/temp/Break_Argenpesos.xlsx')
    df_cordial= pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/temp/Break_Cordial.xlsx')
    df_cristal= pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/temp/Break_Cristal Cash.xlsx')
    df_mili = pd.concat([df_argenpesos, df_cordial, df_cristal])

    # --------------- Natalia --------------- #
    df_consumax= pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/temp/Break_Consumax.xlsx')
    df_crednow= pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/temp/Break_Crednow.xlsx')
    df_credicuotas= pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/temp/Break_Credicuotas.xlsx')
    df_credisol= pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/temp/Break_Credisol.xlsx')
    df_nati = pd.concat([df_consumax, df_crednow, df_credicuotas, df_credisol])

    # --------------- Anahi --------------- #
    df_edenor = pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/temp/Break_Edenor.xlsx')
    df_edersa= pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/temp/Break_Edersa.xlsx')
    df_moovitech = pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/temp/Break_Moovitech.xlsx')
    df_anahi = pd.concat([df_edenor, df_edersa, df_moovitech])

    # --------------- Sofia --------------- #
    df_edesur = pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/temp/Break_Edesur.xlsx')
    df_edemsa= pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/temp/Break_Edemsa.xlsx')
    df_sofia = pd.concat([df_edesur, df_edenor, df_edemsa, df_edersa])

    # --------------- Ana Gomez --------------- #
    df_mejorcredito= pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/temp/Break_Mejor Crédito.xlsx')
    df_qida= pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/temp/Break_Qida.xlsx')
    df_faroyfertil = pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/temp/Break_Faro y Fertil.xlsx')
    df_ana_gomez = pd.concat([df_mejorcredito, df_qida, df_faroyfertil])

    #--------------- Luna --------------- #
    df_fiat= pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/temp/Break_Fiat.xlsx')
    df_credipesos = pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/temp/Break_Credipesos.xlsx')
    df_luna = pd.concat([df_fiat, df_credipesos])

    # --------------- Mica Fernandez --------------- #
    df_antina= pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/temp/Break_Antina.xlsx')
    df_italcred = pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/temp/Break_Italcred.xlsx')
    df_mica_fernandez = pd.concat([df_antina, df_italcred])

    # --------------- Maia --------------- #
    df_maycoop= pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/temp/Break_Maycoop.xlsx')
    df_kalima = pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/temp/Break_Kalima.xlsx')
    df_maia = pd.concat([df_kalima, df_maycoop])

    # --------------- Yamila --------------- #
    df_yami = pd.concat([df_mili, df_nati, df_ana_gomez, df_luna, df_mica_fernandez, df_maia])

    # ------------------------------------------------------------------------------------#

    # --------------- Milagro --------------- #
    if os.path.exists(f'1. Break/{año}/{mes_int}. {mes_str}/Milagro - {mes_str}.xlsx'):
        a_concatenar = pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/Milagro - {mes_str}.xlsx')
        df_concat = pd.concat([a_concatenar, df_mili])
        df_concat.to_excel(f'1. Break/{año}/{mes_int}. {mes_str}/Milagro - {mes_str}.xlsx', index=False)
        print(f"Archivo 'Milagro' concatenado ✔")
    else:
        df_mili.to_excel(f'1. Break/{año}/{mes_int}. {mes_str}/Milagro - {mes_str}.xlsx', index=False)
        print("Archivo 'Milagro' creado ✔")

    # --------------- Natalia --------------- #
    if os.path.exists(f'1. Break/{año}/{mes_int}. {mes_str}/Natalia - {mes_str}.xlsx'):
        a_concatenar = pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/Natalia - {mes_str}.xlsx')
        df_concat = pd.concat([a_concatenar, df_nati])
        df_concat.to_excel(f'1. Break/{año}/{mes_int}. {mes_str}/Natalia - {mes_str}.xlsx', index=False)
        print(f"Archivo 'Natalia' concatenado ✔")
    else:
        df_nati.to_excel(f'1. Break/{año}/{mes_int}. {mes_str}/Natalia - {mes_str}.xlsx', index=False)
        print("Archivo 'Natalia' creado ✔")

    # --------------- Anahi --------------- #
    if os.path.exists(f'1. Break/{año}/{mes_int}. {mes_str}/Anahi - {mes_str}.xlsx'):
        a_concatenar = pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/Anahi - {mes_str}.xlsx')
        df_concat = pd.concat([a_concatenar, df_anahi])
        df_concat.to_excel(f'1. Break/{año}/{mes_int}. {mes_str}/Anahi - {mes_str}.xlsx', index=False)
        print(f"Archivo 'Anahi' concatenado ✔")
    else:
        df_anahi.to_excel(f'1. Break/{año}/{mes_int}. {mes_str}/Anahi - {mes_str}.xlsx', index=False)
        print("Archivo 'Anahi' creado ✔")

    # --------------- Sofia --------------- #
    if os.path.exists(f'1. Break/{año}/{mes_int}. {mes_str}/Sofia - {mes_str}.xlsx'):
        a_concatenar = pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/Sofia - {mes_str}.xlsx')
        df_concat = pd.concat([a_concatenar, df_sofia])
        df_concat.to_excel(f'1. Break/{año}/{mes_int}. {mes_str}/Sofia - {mes_str}.xlsx', index=False)
        print(f"Archivo 'Sofia' concatenado ✔")
    else:
        df_sofia.to_excel(f'1. Break/{año}/{mes_int}. {mes_str}/Sofia - {mes_str}.xlsx', index=False)
        print("Archivo 'Sofia' creado ✔")

    # --------------- Ana Gomez --------------- #
    if os.path.exists(f'1. Break/{año}/{mes_int}. {mes_str}/Ana_Gomez - {mes_str}.xlsx'):
        a_concatenar = pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/Ana_Gomez - {mes_str}.xlsx')
        df_concat = pd.concat([a_concatenar, df_ana_gomez])
        df_concat.to_excel(f'1. Break/{año}/{mes_int}. {mes_str}/Ana_Gomez - {mes_str}.xlsx', index=False)
        print(f"Archivo 'Ana_Gomez' concatenado ✔")
    else:
        df_ana_gomez.to_excel(f'1. Break/{año}/{mes_int}. {mes_str}/Ana_Gomez - {mes_str}.xlsx', index=False)
        print("Archivo 'Ana_Gomez' creado ✔")

    # --------------- Luna --------------- #
    if os.path.exists(f'1. Break/{año}/{mes_int}. {mes_str}/Luna - {mes_str}.xlsx'):
        a_concatenar = pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/Luna - {mes_str}.xlsx')
        df_concat = pd.concat([a_concatenar, df_luna])
        df_concat.to_excel(f'1. Break/{año}/{mes_int}. {mes_str}/Luna - {mes_str}.xlsx', index=False)
        print(f"Archivo 'Luna' concatenado ✔")
    else:
        df_luna.to_excel(f'1. Break/{año}/{mes_int}. {mes_str}/Luna - {mes_str}.xlsx', index=False)
        print("Archivo 'Luna' creado ✔")

    # --------------- Mica Fernandez --------------- #
    if os.path.exists(f'1. Break/{año}/{mes_int}. {mes_str}/Mica_Fernandez - {mes_str}.xlsx'):
        a_concatenar = pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/Mica_Fernandez - {mes_str}.xlsx')
        df_concat = pd.concat([a_concatenar, df_mica_fernandez])
        df_concat.to_excel(f'1. Break/{año}/{mes_int}. {mes_str}/Mica_Fernandez - {mes_str}.xlsx', index=False)
        print(f"Archivo 'Mica_Fernandez' concatenado ✔")
    else:
        df_mica_fernandez.to_excel(f'1. Break/{año}/{mes_int}. {mes_str}/Mica_Fernandez - {mes_str}.xlsx', index=False)
        print("Archivo 'Mica_Fernandez' creado ✔")

    # --------------- Yamila --------------- #
    if os.path.exists(f'1. Break/{año}/{mes_int}. {mes_str}/Yamila - {mes_str}.xlsx'):
        a_concatenar = pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/Yamila - {mes_str}.xlsx')
        df_concat = pd.concat([a_concatenar, df_yami])
        df_concat.to_excel(f'1. Break/{año}/{mes_int}. {mes_str}/Yamila - {mes_str}.xlsx', index=False)
        print(f"Archivo 'Yamila' concatenado ✔")
    else:
        df_yami.to_excel(f'1. Break/{año}/{mes_int}. {mes_str}/Yamila - {mes_str}.xlsx', index=False)
        print("Archivo 'Yamila' creado ✔")

    # --------------- Maia --------------- #
    if os.path.exists(f'1. Break/{año}/{mes_int}. {mes_str}/Maia - {mes_str}.xlsx'):
        a_concatenar = pd.read_excel(f'1. Break/{año}/{mes_int}. {mes_str}/Maia - {mes_str}.xlsx')
        df_concat = pd.concat([a_concatenar, df_maia])
        df_concat.to_excel(f'1. Break/{año}/{mes_int}. {mes_str}/Maia - {mes_str}.xlsx', index=False)
        print(f"Archivo 'Maia' concatenado ✔")
    else:
        df_maia.to_excel(f'1. Break/{año}/{mes_int}. {mes_str}/Maia - {mes_str}.xlsx', index=False)
        print("Archivo 'Maia' creado ✔")