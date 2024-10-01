from AFN_File.AFN import AFN

#Crear el AFN basico
afn = AFN.afn_basico(['a', 'z'], token="Token_Rango")

#Convertir el AFN a un AFD usando el metodo de subconjuntos
afd = afn.convertir_a_afd()

# Mostrar el AFD
for i, fila in enumerate(afd.tablaAFD):
    print(f"Estado S{i}: {fila}")

# Guardar el AFD en un archivo
afd.guardar_AFD_archivo('afd_result.csv')



"""#Crear un AFN básico para el simbolo 'a'
afn_az = AFN.afn_basico(['a','z'], token='TOKEN_AZ')
afn_az.mostrar_afn()
"""
"""
afn_az = AFN.afn_basico('a', token='TOKEN_AZ')
afn_az.mostrar_afn()

"""