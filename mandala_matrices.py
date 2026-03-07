import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection

def generar_mandala_matricial(tamaño=500, capas=8):
    """
    Genera un mandala usando operaciones matriciales.
    
    Args:
        tamaño: dimensión de la matriz (tamaño x tamaño)
        capas: número de capas del mandala
    
    Returns:
        matriz: matriz 2D que representa el mandala
    """
    # Crear una matriz de coordenadas
    x = np.linspace(-1, 1, tamaño)
    y = np.linspace(-1, 1, tamaño)
    X, Y = np.meshgrid(x, y)
    
    # Calcular la distancia desde el centro
    distancia = np.sqrt(X**2 + Y**2)
    
    # Calcular el ángulo desde el centro
    angulo = np.arctan2(Y, X)
    
    # Crear el patrón del mandala combinando distancia y ángulo
    mandala = np.zeros((tamaño, tamaño))
    
    for i in range(capas):
        # Crear ondas circulares con modulación angular
        frecuencia_radial = 5 * (i + 1)
        frecuencia_angular = (i + 1) * 6
        
        # Aplicar operaciones matriciales para crear el patrón
        patron = np.sin(frecuencia_radial * distancia) * np.cos(frecuencia_angular * angulo)
        
        # Ponderar cada capa
        peso = (capas - i) / capas
        mandala += peso * patron
    
    # Normalizar la matriz al rango [0, 1]
    mandala = (mandala - mandala.min()) / (mandala.max() - mandala.min())
    
    return mandala, distancia, angulo

def transformar_rotacion(matriz, angulo_grados):
    """
    Rota una matriz por un ángulo especificado.
    
    Args:
        matriz: matriz 2D a rotar
        angulo_grados: ángulo de rotación en grados
    
    Returns:
        matriz rotada
    """
    from scipy import ndimage
    return ndimage.rotate(matriz, angulo_grados, reshape=False, order=1)

def crear_simetria_axial(matriz, eje='ambos'):
    """
    Crea simetría en la matriz para efectos tipo mandala.
    
    Args:
        matriz: matriz original
        eje: 'horizontal', 'vertical' o 'ambos'
    
    Returns:
        matriz con simetría aplicada
    """
    resultado = matriz.copy()
    
    if eje in ['horizontal', 'ambos']:
        # Reflejo horizontal
        resultado = (resultado + np.fliplr(resultado)) / 2
    
    if eje in ['vertical', 'ambos']:
        # Reflejo vertical
        resultado = (resultado + np.flipud(resultado)) / 2
    
    return resultado

def visualizar_mandala(mandala, titulo="Mandala Matricial"):
    """
    Visualiza el mandala con colores especiales.
    """
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    
    # Usar un colormap especial
    im = ax.imshow(mandala, cmap='twilight', interpolation='bilinear')
    ax.set_title(titulo, fontsize=16, fontweight='bold', pad=20)
    ax.axis('off')
    
    plt.colorbar(im, ax=ax, label='Intensidad')
    plt.tight_layout()
    return fig

# ============= EJECUCIÓN PRINCIPAL =============

if __name__ == "__main__":
    print("🎨 Generando Mandala Matricial...")
    
    # Generar mandala básico
    mandala_base, distancia, angulo = generar_mandala_matricial(tamaño=600, capas=10)
    
    # Aplicar simetría
    mandala_simetrico = crear_simetria_axial(mandala_base, eje='ambos')
    
    # Visualizar resultados
    fig1 = visualizar_mandala(mandala_base, "Mandala Matricial - Patrón Base")
    fig1.savefig('mandala_base.png', dpi=150, bbox_inches='tight')
    print("✓ Mandala base guardado como 'mandala_base.png'")
    
    fig2 = visualizar_mandala(mandala_simetrico, "Mandala Matricial - Con Simetría")
    fig2.savefig('mandala_simetrico.png', dpi=150, bbox_inches='tight')
    print("✓ Mandala simétrico guardado como 'mandala_simetrico.png'")
    
    # Crear una composición con múltiples rotaciones
    fig3, axes = plt.subplots(2, 2, figsize=(12, 12))
    angulos = [0, 45, 90, 135]
    
    for idx, angulo_rot in enumerate(angulos):
        ax = axes[idx // 2, idx % 2]
        mandala_rotado = transformar_rotacion(mandala_simetrico, angulo_rot)
        im = ax.imshow(mandala_rotado, cmap='hsv', interpolation='bilinear')
        ax.set_title(f'Rotación: {angulo_rot}°', fontweight='bold')
        ax.axis('off')
    
    plt.suptitle('Mandala Matricial - Rotaciones', fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    fig3.savefig('mandala_rotaciones.png', dpi=150, bbox_inches='tight')
    print("✓ Composición de rotaciones guardada como 'mandala_rotaciones.png'")
    
    # Estadísticas de las matrices
    print("\n📊 Estadísticas de las matrices generadas:")
    print(f"  Forma: {mandala_base.shape}")
    print(f"  Valor mínimo: {mandala_base.min():.4f}")
    print(f"  Valor máximo: {mandala_base.max():.4f}")
    print(f"  Valor promedio: {mandala_base.mean():.4f}")
    print(f"  Desviación estándar: {mandala_base.std():.4f}")
    
    print("\n✨ ¡Mandala generado exitosamente!")
    plt.show()