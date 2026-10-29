from collections import defaultdict
import csv
import matplotlib.pyplot as plt

def leer_tiempos(nombre_archivo):
    mediciones = defaultdict(list)

    try:
        with open(nombre_archivo, newline="", encoding="utf-8") as archivo:
            # Detección automática de delimitador (',' o ';')
            muestra = archivo.read(2048)
            archivo.seek(0)
            delimitador = ';' if ';' in muestra and ',' not in muestra else ','

            lector = csv.reader(archivo, delimiter=delimitador)

            for fila in lector:
                if len(fila) < 2:
                    continue

                try:
                    # Se convierte a float primero para aceptar valores como "12.0"
                    n = int(float(fila[0].strip()))
                    tiempo_str = fila[1].strip().replace(',', '.')
                    tiempo = float(tiempo_str)
                except ValueError:
                    if fila and fila[0].strip().lower() in {"n", "tamano", "tamaño"}:
                        continue
                    continue

                mediciones[n].append(tiempo)

    except FileNotFoundError:
        print(f"[AVISO] No se encontró el archivo '{nombre_archivo}'. Asegúrate de que esté en la misma carpeta.")

    return dict(mediciones)


def calcular_estadisticas(mediciones):
    estadisticas = {}

    for n, tiempos in mediciones.items():
        if not tiempos:
            continue

        media = sum(tiempos) / len(tiempos)
        # Se calcula un único valor de error promedio (desviación media absoluta) para este n
        error_promedio = sum(abs(t - media) for t in tiempos) / len(tiempos) if tiempos else 0

        estadisticas[n] = {
            "media": media,
            "error_promedio": error_promedio
        }

    return estadisticas

def error_abs(mediciones, estadisticas):
    errores_abs = {}

    for n, tiempos in mediciones.items():
        if not tiempos or n not in estadisticas:
            continue

        media = estadisticas[n]["media"]
        errores_abs[n] = [
            abs(tiempo - media)
            for tiempo in tiempos
        ]

    return errores_abs

def graficar(estadisticas_it, estadisticas_rec):
    if not estadisticas_it and not estadisticas_rec:
        print("[ERROR] No hay datos para graficar.")
        return

    fig, ax = plt.subplots(figsize=(9, 5))

    if estadisticas_it:
        n_it = sorted(estadisticas_it)
        tiempos_it = [estadisticas_it[n]["media"] for n in n_it]
        ax.plot(n_it, tiempos_it, "o-", color="blue", label="Iterativo")

    if estadisticas_rec:
        n_rec = sorted(estadisticas_rec)
        tiempos_rec = [estadisticas_rec[n]["media"] for n in n_rec]
        ax.plot(n_rec, tiempos_rec, "o-", color="green", label="Recursivo")

    ax.set_title("Tiempo promedio por tamaño de entrada n")
    ax.set_xlabel("n")
    ax.set_ylabel("Tiempo promedio")
    ax.grid(True, which="both", linestyle="--", linewidth=0.5)

    # Escala logarítmica para visualizar correctamente ambos algoritmos
    ax.set_yscale('log')

    ax.legend()
    plt.tight_layout()
    plt.savefig("grafico.png", dpi=150, bbox_inches="tight")
    plt.close()


def mostrar_tabla(estadisticas_it, estadisticas_rec):
    n_values = sorted(set(estadisticas_it) | set(estadisticas_rec))

    if not n_values:
        print("[ERROR] No hay datos para mostrar en la tabla.")
        return

    filas = []
    for n in n_values:
        datos_it = estadisticas_it.get(n)
        datos_rec = estadisticas_rec.get(n)

        if datos_it is not None:
            media_it = f"{datos_it['media']:.5f}" if datos_it['media'] < 1 else f"{datos_it['media']:.2f}"
            error_it = f"{datos_it['error_promedio']:.5f}"
        else:
            media_it, error_it = "-", "-"

        if datos_rec is not None:
            media_rec = f"{datos_rec['media']:.5f}" if datos_rec['media'] < 1 else f"{datos_rec['media']:.2f}"
            error_rec = f"{datos_rec['error_promedio']:.5f}"
        else:
            media_rec, error_rec = "-", "-"

        filas.append([
            n,
            media_it,
            error_it,
            media_rec,
            error_rec
        ])

    fig, ax = plt.subplots(figsize=(10, max(4, len(filas) * 0.35)))
    ax.axis("off")

    columnas = [
        "n",
        "Media It.",
        "Error It.",
        "Media Rec.",
        "Error Rec."
    ]

    tabla = ax.table(
        cellText=filas,
        colLabels=columnas,
        loc="center",
        cellLoc="center"
    )

    tabla.auto_set_font_size(False)
    tabla.set_fontsize(9)
    tabla.scale(1, 1.4)

    plt.title("Resumen de Tiempos y Errores por n", pad=20, fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig("tabla_tiempos.png", dpi=150, bbox_inches="tight")
    plt.close()

def mostrar_tabla_errabs(errores_abs, tipo):
    n_values = sorted(errores_abs)

    if not n_values:
        print(f"[ERROR] No hay datos para {tipo}.")
        return

    cantidad_ejecuciones = max(
        len(errores_abs[n])
        for n in n_values
    )

    filas = []

    for n in n_values:
        fila = [n]

        for error in errores_abs[n]:
            fila.append(
                f"{error:.5f}" if error < 1 else f"{error:.2f}"
            )

        fila.extend(
            ["-"] * (cantidad_ejecuciones - len(errores_abs[n]))
        )

        filas.append(fila)

    columnas = ["n"] + [
        f"Ejecución {numero}"
        for numero in range(1, cantidad_ejecuciones + 1)
    ]

    fig, ax = plt.subplots(
        figsize=(
            max(8, cantidad_ejecuciones * 1.5),
            max(4, len(filas) * 0.35)
        )
    )

    ax.axis("off")

    tabla = ax.table(
        cellText=filas,
        colLabels=columnas,
        loc="center",
        cellLoc="center"
    )

    tabla.auto_set_font_size(False)
    tabla.set_fontsize(9)
    tabla.scale(1, 1.4)

    plt.title(
        f"Error absoluto por ejecución - {tipo}",
        pad=20,
        fontsize=12,
        fontweight="bold"
    )

    plt.tight_layout()
    plt.savefig(f"tabla_error_absoluto_{tipo.lower()}.png",
            dpi=150,
            bbox_inches="tight")
    plt.close()

# ---- Uso principal ----
if __name__ == "__main__":
    mediciones_it = leer_tiempos("tiempoFibIterativo.csv")
    mediciones_rec = leer_tiempos("tiempoFibRecursivo.csv")

    estadisticas_it = calcular_estadisticas(mediciones_it)
    estadisticas_rec = calcular_estadisticas(mediciones_rec)
    errores_abs_it = error_abs(mediciones_it,estadisticas_it)
    errores_abs_rec = error_abs(mediciones_rec, estadisticas_rec)
    
    graficar(estadisticas_it, estadisticas_rec)
    mostrar_tabla(estadisticas_it, estadisticas_rec)
    mostrar_tabla_errabs(errores_abs_it,"Iterativo")
    mostrar_tabla_errabs(errores_abs_rec,"Recursivo")
