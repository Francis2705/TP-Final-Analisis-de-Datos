from tasas.analisis_tasa_actividad import mostrar_tasa_actividad
from tasas.analisis_tasa_desocupacion import mostrar_tasa_desocupacion
from tasas.analisis_tasa_empleo import mostrar_tasa_empleo
from tasas.analisis_tasas_comparacion import mostrar_ingresos_poblacion
from tasas.analisis_ingresos import ver_evolucion_del_ingreso_promedio

from ejercicio1.analisis_medidas_tendencia import ver_evolucion_medidas_tendecia_central
from ejercicio1.analisis_medidas_posicion import ver_evolucion_medidas_posicion

from ejercicio2.analisi_multivariado import realizar_analisis_multivariado
from ejercicio4.modelo_entrenamiento import realizar_prediccion

from ejercicio5.grafico_con_variable import realizar_grafico_con_variable
from ejercicio5.grafico_sin_variable import realizar_grafico_sin_variable

print("\n ----------------- Bienvenido a nuestro menu ------------------------------\n")


def pedir_numero()-> int:
    numero = int(input("Ingrese un numero: "))
    return numero


def mostrar_menu():
    
    print("""Elige el numero:
            
            \n ----------------- VER TASAS ------------------------------\n
            
            1. para ver tasa de actividad
            2. para ver tasa de desocupacion
            3. para ver tasa de empleo
            4  para ver la evolucion del Ingreso Promedio Individual en el AMBA (2016-2024)
            5. para ver todas las tasas 
            
            \n ----------------- VER LA EVOLUCION DE MEDIDAS DE TENDENCIA CENTRAL Y MEDIDAS DE POSICION ------------------\n
            
            6. para ver la evolucion de las medidas de tendencia central
            7. para ver la evolucion de las medidas de posicion
            
            \n ----------------- VER ANALISIS MULTIVARIADO ------------------\n
            
            8. para ver analisis multivariado
            9. para ver predicciones de ingresos
            
            \n ----------------- VISUALIZACIONES DE DATOS GEORREFERENCIADOS. ------------------\n
            
            10. para ver la cantidad de gente que hay en GBA
            11. para ver el promedio de ingresos de la gente en GBA
            
            \n ----------------- SALIR DEL MENU. ------------------\n
            12. para salir del menu y dejar de ejecutar el programa
        """)
        
def elegir_menu():
    
    mostrar_menu()
    seguir = True
    
    while(seguir):
        numero_elegido = pedir_numero()
        
        if(numero_elegido == 1):
            mostrar_tasa_actividad()
        
        elif(numero_elegido == 2):
            mostrar_tasa_desocupacion()
        
        elif(numero_elegido == 3):
            mostrar_tasa_empleo()
        
        elif(numero_elegido == 4):
            ver_evolucion_del_ingreso_promedio()
        
        elif(numero_elegido == 5):
            mostrar_ingresos_poblacion()
        
        elif(numero_elegido == 6):
            ver_evolucion_medidas_tendecia_central()
        
        elif(numero_elegido == 7):
            ver_evolucion_medidas_posicion()
        
        elif(numero_elegido == 8):
            realizar_analisis_multivariado()
        
        elif(numero_elegido == 9):
            realizar_prediccion()
            
        elif(numero_elegido == 10):
            realizar_grafico_sin_variable()
        
        elif(numero_elegido == 11):
            realizar_grafico_con_variable()
        
        elif(numero_elegido == 12):
            seguir = False
        
        if(numero_elegido != 13):mostrar_menu()

elegir_menu()
