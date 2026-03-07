# Sistema de Recomendación de Canciones
#
# CARACTERÍSTICAS PRINCIPALES:
# 1. **Vectores de Canciones**: Cada canción se representa como un vector con atributos numéricos
#    (Energía, Bailabilidad, Emotividad, Tempo). Esto permite comparar canciones matemáticamente.
# 
# 2. **Similitud Coseno**: Calcula qué tan parecidas son dos canciones usando el producto punto
#    de sus vectores. Valores cercanos a 1 = canciones muy similares, cercanos a 0 = diferentes.
#
# 3. **Recomendaciones Personalizadas**: Busca las canciones más similares a la que el usuario
#    está escuchando y las sugiere como recomendaciones.
#
# 4. **Análisis de Playlist**: Calcula el estado emocional promedio de una lista de reproducción
#    basándose en los valores de emotividad de cada canción.
#
# 5. **Visualización de Datos**: Genera gráficos para ver patrones entre géneros y características.

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

# BASE DE DATOS VECTORIAL DE CANCIONES
# Cada canción tiene 4 características: [energía, bailabilidad, emotividad, tempo_normalizado]
canciones = {
    "Bohemian Rhapsody": {"artista": "Queen", "genero": "Rock", "vector": [0.7, 0.4, 0.9, 0.6]},
    "Blinding Lights": {"artista": "The Weeknd", "genero": "Pop", "vector": [0.9, 0.8, 0.7, 0.8]},
    "Levitating": {"artista": "Dua Lipa", "genero": "Pop", "vector": [0.8, 0.9, 0.8, 0.7]},
    "Lose Yourself": {"artista": "Eminem", "genero": "Hip-Hop", "vector": [0.9, 0.7, 0.5, 0.9]},
    "Uptown Funk": {"artista": "Mark Ronson", "genero": "Funk", "vector": [0.85, 0.95, 0.6, 0.75]},
    "Midnight City": {"artista": "M83", "genero": "Electrónica", "vector": [0.7, 0.6, 0.8, 0.65]},
    "Shape of You": {"artista": "Ed Sheeran", "genero": "Pop", "vector": [0.7, 0.8, 0.6, 0.7]},
    "Starboy": {"artista": "The Weeknd", "genero": "Electrónica", "vector": [0.8, 0.7, 0.7, 0.75]},
}

# FUNCIÓN 1: Calcular similitud coseno entre dos vectores
def calcular_similitud(vector1, vector2):
    """
    Calcula la similitud coseno entre dos vectores de canciones.
    Rango: 0 (completamente diferentes) a 1 (idénticas)
    """
    similitud = cosine_similarity([vector1], [vector2])[0][0]
    return similitud

# FUNCIÓN 2: Recomendar canciones similares
def recomendar_canciones(nombre_cancion, top_n=5):
    """
    Encuentra las canciones más similares a la canción dada.
    Usa la similitud coseno para comparar vectores.
    """
    if nombre_cancion not in canciones:
        return f"❌ Canción '{nombre_cancion}' no encontrada en la base de datos."
    
    vector_referencia = np.array(canciones[nombre_cancion]["vector"])
    similitudes = []
    
    for nombre, datos in canciones.items():
        if nombre != nombre_cancion:
            vector_candidato = np.array(datos["vector"])
            similitud = calcular_similitud(vector_referencia, vector_candidato)
            similitudes.append((nombre, similitud, datos["artista"], datos["genero"]))
    
    # Ordenar por similitud descendente
    similitudes.sort(key=lambda x: x[1], reverse=True)
    return similitudes[:top_n]

# FUNCIÓN 3: Analizar el estado emocional de una playlist
def analizar_playlist(nombres_canciones):
    """
    Calcula el promedio de emotividad de una lista de reproducción.
    Emotividad: índice 2 del vector (rango 0-1)
    """
    emotividades = []
    for nombre in nombres_canciones:
        if nombre in canciones:
            emotividades.append(canciones[nombre]["vector"][2])
    
    if not emotividades:
        return 0
    
    promedio = np.mean(emotividades)
    return promedio

# FUNCIÓN 4: Visualizar canciones por género
def visualizar_por_genero():
    """
    Crea gráficos para visualizar la relación entre energía y bailabilidad por género.
    """
    generos = {}
    
    # Agrupar canciones por género
    for nombre, datos in canciones.items():
        genero = datos["genero"]
        if genero not in generos:
            generos[genero] = {"energias": [], "bailabilidades": []}
        
        vector = datos["vector"]
        generos[genero]["energias"].append(vector[0])
        generos[genero]["bailabilidades"].append(vector[1])
    
    # Crear gráfico
    plt.figure(figsize=(12, 6))
    
    colores = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
    for idx, (genero, datos) in enumerate(generos.items()):
        plt.scatter(datos["energias"], datos["bailabilidades"], 
                   label=genero, s=100, alpha=0.7, color=colores[idx % len(colores)])
    
    plt.xlabel("Energía", fontsize=12)
    plt.ylabel("Bailabilidad", fontsize=12)
    plt.title("Características de Canciones por Género", fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('analisis_canciones.png', dpi=150)
    print("✓ Gráfico guardado como 'analisis_canciones.png'")
    plt.show()

# FUNCIÓN 5: Mostrar estadísticas de una canción
def estadisticas_cancion(nombre_cancion):
    """
    Muestra las características vectoriales de una canción.
    """
    if nombre_cancion not in canciones:
        return f"❌ Canción no encontrada."
    
    datos = canciones[nombre_cancion]
    vector = datos["vector"]
    
    print(f"\n📊 Estadísticas de '{nombre_cancion}':")
    print(f"   Artista: {datos['artista']}")
    print(f"   Género: {datos['genero']}")
    print(f"   Energía: {vector[0]:.2f}/1.0")
    print(f"   Bailabilidad: {vector[1]:.2f}/1.0")
    print(f"   Emotividad: {vector[2]:.2f}/1.0")
    print(f"   Tempo (normalizado): {vector[3]:.2f}/1.0")

# ============= EJECUCIÓN PRINCIPAL =============

if __name__ == "__main__":
    print("🎵 SISTEMA DE RECOMENDACIÓN DE CANCIONES 🎵\n")
    
    # Ejemplo 1: Recomendar canciones similares
    print("=" * 60)
    print("1️⃣  RECOMENDACIONES SIMILARES A 'Blinding Lights'")
    print("=" * 60)
    recomendaciones = recomendar_canciones("Blinding Lights", top_n=3)
    for idx, (nombre, similitud, artista, genero) in enumerate(recomendaciones, 1):
        print(f"{idx}. {nombre} - {artista} ({genero})")
        print(f"   Similitud: {similitud:.2%}\n")
    
    # Ejemplo 2: Analizar estado emocional de una playlist
    print("=" * 60)
    print("2️⃣  ANÁLISIS EMOCIONAL DE PLAYLIST")
    print("=" * 60)
    mi_playlist = ["Blinding Lights", "Levitating", "Uptown Funk"]
    emocion_promedio = analizar_playlist(mi_playlist)
    print(f"Canciones en la playlist: {', '.join(mi_playlist)}")
    print(f"Emotividad promedio: {emocion_promedio:.2f}/1.0")
    
    if emocion_promedio > 0.7:
        print("🎉 ¡Playlist muy emotiva!")
    elif emocion_promedio > 0.4:
        print("😊 Playlist con emociones moderadas")
    else:
        print("😎 Playlist más relajada")
    
    # Ejemplo 3: Mostrar estadísticas
    print("\n" + "=" * 60)
    print("3️⃣  ESTADÍSTICAS DE CANCIÓN")
    print("=" * 60)
    estadisticas_cancion("Shape of You")
    
    # Ejemplo 4: Visualizar datos
    print("\n" + "=" * 60)
    print("4️⃣  VISUALIZANDO DATOS...")
    print("=" * 60)
    visualizar_por_genero()
    
    print("\n✨ ¡Análisis completado! ✨"