import pygame
from config import FONT_PATH

# ==========================================================
#  load_font(size)
# ----------------------------------------------------------
#  Carga una fuente personalizada para el juego.
#  Si falla (por ejemplo, archivo faltante), usa Arial.
# ==========================================================
def load_font(size):
    try:
        # Intenta cargar la fuente desde el archivo configurado
        return pygame.font.Font(FONT_PATH, size)
    except:
        # Si falla, se usa una fuente estándar del sistema
        return pygame.font.SysFont("arial", size)

# ==========================================================
#  play_music(path, current_music)
# ----------------------------------------------------------
#  Reproduce música de fondo si:
#    - El mixer está inicializado
#    - El archivo pedido no es el mismo que ya suena
#
#  Devuelve:
#    - El path de la música actual si se reproduce correctamente
#    - None si hubo error
#
#  current_music: path actualmente sonando → evita recargar
# ==========================================================
def play_music(path, current_music):
    # Si el mixer no fue inicializado, no intentamos reproducir
    if not pygame.mixer.get_init():
        return path

    # Si la música ya está sonando, no se recarga
    if current_music == path:
        return path

    try:
        # Cargar y reproducir en loop infinito
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)
        print(path)
        return path

    except pygame.error as e:
        # Si ocurre un error con el archivo o mixer
        print(f"Error al reproducir música: {e}")
        return None
