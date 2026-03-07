"""
╔══════════════════════════════════════════════════════╗
║        🌌  VIDA CUÁNTICA  -  Autómata Celular 3D      ║
║   Simulación de vida artificial usando matrices 3D    ║
╚══════════════════════════════════════════════════════╝

Reglas del universo:
  - Una célula VIVA sobrevive si tiene entre 4 y 6 vecinos vivos
  - Una célula MUERTA nace si tiene exactamente 5 vecinos vivos
  - El espacio es un cubo 3D toroidal (los bordes se conectan)
"""

import numpy as np
import time
import os
import sys
import random


# ═══════════════════════════════════════════════
#   PALETA DE COLORES (ANSI escape codes)
# ═══════════════════════════════════════════════
class Color:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"

    # Células por densidad de vecinos (gradiente de color)
    NIVELES = [
        "\033[38;5;17m",   # 0 vecinos → azul muy oscuro
        "\033[38;5;21m",   # 1 vecino  → azul
        "\033[38;5;39m",   # 2 vecinos → azul claro
        "\033[38;5;51m",   # 3 vecinos → cian
        "\033[38;5;82m",   # 4 vecinos → verde neón
        "\033[38;5;226m",  # 5 vecinos → amarillo
        "\033[38;5;208m",  # 6 vecinos → naranja
        "\033[38;5;196m",  # 7+ vecinos → rojo intenso
    ]

    TITULO   = "\033[38;5;201m"   # magenta brillante
    INFO     = "\033[38;5;250m"   # gris claro
    ACENTO   = "\033[38;5;45m"    # cian brillante
    MUERTO   = "\033[38;5;238m"   # gris oscuro (célula muerta)


# ═══════════════════════════════════════════════
#   SÍMBOLOS VISUALES
# ═══════════════════════════════════════════════
CELULA_VIVA  = ["▓", "█", "◉", "⬡", "✦", "★"]
CELULA_MUERTA = "·"

# Capas del cubo 3D que se muestran (proyección 2D de cada capa Z)
SEPARADOR = "  "


# ═══════════════════════════════════════════════
#   NÚCLEO: MATRICES Y SIMULACIÓN
# ═══════════════════════════════════════════════

def crear_universo(filas: int, cols: int, capas: int, densidad: float = 0.35) -> np.ndarray:
    """Crea una matriz 3D de células vivas/muertas de forma aleatoria."""
    return (np.random.rand(capas, filas, cols) < densidad).astype(np.int8)


def contar_vecinos_3d(universo: np.ndarray) -> np.ndarray:
    """
    Cuenta los vecinos vivos de cada célula en las 26 direcciones
    posibles del espacio 3D usando convolución manual con matrices.
    Los bordes son toroidales (universo que se enrolla sobre sí mismo).
    """
    capas, filas, cols = universo.shape
    vecinos = np.zeros_like(universo, dtype=np.int8)

    for dz in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dz == 0 and dy == 0 and dx == 0:
                    continue  # No contarse a sí mismo
                # np.roll simula el toroide (bordes que se conectan)
                vecinos += np.roll(
                    np.roll(
                        np.roll(universo, dz, axis=0),
                        dy, axis=1
                    ),
                    dx, axis=2
                )
    return vecinos


def evolucionar(universo: np.ndarray, nacer: set, sobrevivir: set) -> np.ndarray:
    """
    Aplica las reglas de vida/muerte usando operaciones matriciales.
    Reglas configurables para experimentar con distintos 'universos'.
    """
    vecinos = contar_vecinos_3d(universo)

    # Máscaras booleanas (operaciones matriciales puras)
    vivo   = universo == 1
    muerto = universo == 0

    # Crear arrays de máscaras para las reglas
    sobrevive_mask = np.zeros_like(universo, dtype=bool)
    nace_mask      = np.zeros_like(universo, dtype=bool)

    for n in sobrevivir:
        sobrevive_mask |= (vivo & (vecinos == n))
    for n in nacer:
        nace_mask |= (muerto & (vecinos == n))

    nuevo_universo = np.zeros_like(universo)
    nuevo_universo[sobrevive_mask] = 1
    nuevo_universo[nace_mask]      = 1

    return nuevo_universo


# ═══════════════════════════════════════════════
#   VISUALIZACIÓN: PROYECCIÓN 2D DEL CUBO
# ═══════════════════════════════════════════════

def renderizar(universo: np.ndarray, generacion: int, densidad_total: float,
               reglas_nombre: str, simbolo_idx: int):
    """Dibuja el universo 3D como capas 2D lado a lado en la terminal."""

    capas, filas, cols = universo.shape
    vecinos = contar_vecinos_3d(universo)
    simbolo = CELULA_VIVA[simbolo_idx % len(CELULA_VIVA)]

    # Limpiar pantalla
    print("\033[H\033[J", end="")

    # ─── Título ───
    ancho_total = capas * (cols * 2 + 3)
    print(Color.TITULO + Color.BOLD)
    print("  ╔" + "═" * (ancho_total + 2) + "╗")
    print(f"  ║  🌌  VIDA CUÁNTICA 3D  ·  {reglas_nombre:<30}║")
    print("  ╚" + "═" * (ancho_total + 2) + "╝" + Color.RESET)

    # ─── Etiquetas de capa ───
    linea_capas = "  "
    for z in range(capas):
        etiq = f" Capa Z={z} "
        linea_capas += Color.ACENTO + etiq.center(cols * 2 + 2) + Color.RESET + SEPARADOR
    print(linea_capas)
    print()

    # ─── Grilla de cada capa ───
    for y in range(filas):
        fila_str = "  "
        for z in range(capas):
            for x in range(cols):
                estado  = universo[z, y, x]
                n_vivos = vecinos[z, y, x]

                if estado == 1:
                    nivel = min(n_vivos, len(Color.NIVELES) - 1)
                    fila_str += Color.NIVELES[nivel] + simbolo + " " + Color.RESET
                else:
                    fila_str += Color.MUERTO + CELULA_MUERTA + " " + Color.RESET
            fila_str += SEPARADOR
        print(fila_str)

    # ─── Estadísticas ───
    vivas = int(universo.sum())
    total = universo.size

    print()
    print(Color.INFO + "  " + "─" * (ancho_total + 2) + Color.RESET)
    print(
        f"  {Color.ACENTO}Gen {generacion:>4}{Color.RESET}  │  "
        f"{Color.NIVELES[4]}Vivas: {vivas:>4}{Color.RESET}  │  "
        f"{Color.MUERTO}Muertas: {total - vivas:>4}{Color.RESET}  │  "
        f"Densidad: {vivas/total*100:5.1f}%  │  "
        f"Inercia inicial: {densidad_total*100:.0f}%"
    )
    print()
    print(Color.INFO + "  Leyenda: ", end="")
    for i, lv in enumerate(Color.NIVELES):
        print(lv + f"[{i}vec] " + Color.RESET, end="")
    print()
    print(Color.INFO + "  Presiona Ctrl+C para salir" + Color.RESET)


# ═══════════════════════════════════════════════
#   PRESETS DE UNIVERSOS (distintas reglas)
# ═══════════════════════════════════════════════

UNIVERSOS = [
    {
        "nombre":    "Cuántico Clásico      ",
        "nacer":     {5},
        "sobrevivir": {4, 5, 6},
        "densidad":  0.35,
    },
    {
        "nombre":    "Expansión Caótica     ",
        "nacer":     {4, 5},
        "sobrevivir": {3, 4, 5, 6},
        "densidad":  0.25,
    },
    {
        "nombre":    "Cristal de Hielo      ",
        "nacer":     {6},
        "sobrevivir": {5, 6, 7},
        "densidad":  0.45,
    },
    {
        "nombre":    "Plasma Inestable      ",
        "nacer":     {3, 4, 5, 6},
        "sobrevivir": {2, 3},
        "densidad":  0.20,
    },
]


# ═══════════════════════════════════════════════
#   MENÚ INTERACTIVO
# ═══════════════════════════════════════════════

def mostrar_menu():
    print("\033[H\033[J")
    print(Color.TITULO + Color.BOLD)
    print("  ╔══════════════════════════════════════╗")
    print("  ║   🌌  VIDA CUÁNTICA  -  Menú         ║")
    print("  ╚══════════════════════════════════════╝")
    print(Color.RESET)

    for i, u in enumerate(UNIVERSOS):
        print(f"  {Color.ACENTO}[{i+1}]{Color.RESET} {u['nombre']}  "
              f"Nacer:{sorted(u['nacer'])}  "
              f"Sobrevivir:{sorted(u['sobrevivir'])}  "
              f"Densidad:{u['densidad']*100:.0f}%")

    print(f"\n  {Color.ACENTO}[0]{Color.RESET} Universo aleatorio")
    print(f"\n  {Color.INFO}Elige un universo (0-{len(UNIVERSOS)}): {Color.RESET}", end="")


# ═══════════════════════════════════════════════
#   MAIN
# ═══════════════════════════════════════════════

def main():
    # Parámetros del cubo 3D
    FILAS  = 16
    COLS   = 20
    CAPAS  = 3
    FPS    = 8   # fotogramas por segundo

    mostrar_menu()

    try:
        eleccion = int(input())
    except (ValueError, EOFError):
        eleccion = 1

    if eleccion == 0:
        # Universo completamente aleatorio
        config = {
            "nombre":    "Universo Aleatorio    ",
            "nacer":     set(random.sample(range(1, 14), random.randint(1, 4))),
            "sobrevivir": set(random.sample(range(1, 14), random.randint(2, 5))),
            "densidad":  random.uniform(0.2, 0.5),
        }
    else:
        config = UNIVERSOS[max(0, min(eleccion - 1, len(UNIVERSOS) - 1))]

    universo  = crear_universo(FILAS, COLS, CAPAS, config["densidad"])
    simbolo_i = 0
    gen       = 0
    anterior  = None

    print("\033[H\033[J")
    print(Color.ACENTO + "\n  Iniciando simulación..." + Color.RESET)
    time.sleep(1)

    try:
        while True:
            renderizar(
                universo, gen, config["densidad"],
                config["nombre"], simbolo_i
            )

            # Detección de estado estático (universo congelado)
            if anterior is not None and np.array_equal(universo, anterior):
                print(Color.TITULO + "\n  ⚡ Universo estabilizado — reiniciando con nueva semilla..." + Color.RESET)
                time.sleep(2)
                universo  = crear_universo(FILAS, COLS, CAPAS, config["densidad"])
                gen       = 0
                anterior  = None
                simbolo_i += 1
                continue

            anterior = universo.copy()
            universo = evolucionar(universo, config["nacer"], config["sobrevivir"])
            gen     += 1

            time.sleep(1 / FPS)

    except KeyboardInterrupt:
        print("\n\n" + Color.TITULO + "  Universo disuelto. ¡Hasta la próxima simulación! 🌌" + Color.RESET + "\n")


if __name__ == "__main__":
    main()
