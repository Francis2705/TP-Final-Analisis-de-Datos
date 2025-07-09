#Consolar
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
#Tasas
from tasas.analisis_tasa_actividad import mostrar_tasa_actividad
from tasas.analisis_tasa_desocupacion import mostrar_tasa_desocupacion
from tasas.analisis_tasa_empleo import mostrar_tasa_empleo
from tasas.analisis_tasas_comparacion import mostrar_ingresos_poblacion
from tasas.analisis_ingresos import ver_evolucion_del_ingreso_promedio
#Medidas de tendencia y posicion
from ejercicio1.analisis_medidas_tendencia import ver_evolucion_medidas_tendecia_central
from ejercicio1.analisis_medidas_posicion import ver_evolucion_medidas_posicion
#Analisis multivariado y predicciones
from ejercicio2.analisi_multivariado import realizar_analisis_multivariado
from ejercicio4.modelo_entrenamiento import realizar_prediccion
#Datos georreferenciados
from ejercicio5.grafico_con_variable import realizar_grafico_con_variable
from ejercicio5.grafico_sin_variable import realizar_grafico_sin_variable

console = Console()

def mostrar_bienvenida():
    console.print(Panel.fit("🌟 [bold cyan]Bienvenido/a al menú de análisis de datos del AMBA[/bold cyan] 🌟", padding=2))

def mostrar_menu():
    table = Table(title="📊 Menú Principal", show_lines=True)

    table.add_column("Opción", justify="center", style="cyan", no_wrap=True)
    table.add_column("Descripción", style="white")

    opciones = [
        ("1", "Ver tasa de actividad"),
        ("2", "Ver tasa de desocupación"),
        ("3", "Ver tasa de empleo"),
        ("4", "Ver evolución del ingreso promedio en AMBA"),
        ("5", "Ver todas las tasas"),
        ("6", "Ver evolución de medidas de tendencia central"),
        ("7", "Ver evolución de medidas de posición"),
        ("8", "Ver análisis multivariado"),
        ("9", "Ver predicciones de ingresos"),
        ("10", "Visualización: cantidad de gente en AMBA"),
        ("11", "Visualización: ingresos promedio en AMBA"),
        ("12", "Salir del programa")
    ]

    for codigo, descripcion in opciones:
        table.add_row(codigo, descripcion)

    console.print(table)

def pedir_numero() -> int:
    while True:
        entrada = Prompt.ask("👉 Ingresá una opción [1-12]")
        if entrada.isdigit():
            numero = int(entrada)
            if 1 <= numero <= 12:
                return numero
            else:
                console.print("[red]❌ Número fuera de rango. Elegí entre 1 y 12.[/red]")
        else:
            console.print("[red]❌ Entrada inválida. Solo se permiten números.[/red]")

def ejecutar_opcion(opcion: int):
    acciones = {
        1: mostrar_tasa_actividad,
        2: mostrar_tasa_desocupacion,
        3: mostrar_tasa_empleo,
        4: ver_evolucion_del_ingreso_promedio,
        5: mostrar_ingresos_poblacion,
        6: ver_evolucion_medidas_tendecia_central,
        7: ver_evolucion_medidas_posicion,
        8: realizar_analisis_multivariado,
        9: realizar_prediccion,
        10: realizar_grafico_sin_variable,
        11: realizar_grafico_con_variable
    }

    if opcion == 12:
        console.print("\n👋 [bold green]¡Gracias por usar el sistema! [/bold green]")
        return False

    accion = acciones.get(opcion)
    if accion:
        console.rule(f"[bold blue]Ejecutando opción {opcion}...[/bold blue]")
        accion()
    else:
        console.print("[red]❌ Opción no válida.[/red]")

    return True

def main():
    mostrar_bienvenida()
    seguir = True
    while seguir:
        mostrar_menu()
        opcion = pedir_numero()
        seguir = ejecutar_opcion(opcion)

if __name__ == "__main__":
    main()