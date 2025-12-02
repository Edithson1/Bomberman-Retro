from entities.player import Player
from entities.enemy import Enemy
from entities.blocks import DestructibleBlock, IndestructibleBlock
from entities.portal import Portal
import random

# ----------------------------------------------------------
# Tipos posibles de ítems que pueden aparecer dentro de un bloque destructible
# ----------------------------------------------------------
POWERUP_TYPES = ["FIRE", "BOMB", "SPEED", "PASS_WALL", "PASS_BOMB", "SHIELD", "KEY", "SLOW"]

# Probabilidad global de que un bloque contenga un ítem (15%)
DROP_RATE = 0.15


# ==========================================================
# generate_entities(game, matrix)
# ----------------------------------------------------------
# Lee la matriz del nivel (mapa) y crea las entidades:
#   - S → Bloque indestructible
#   - B → Bloque destruible (posible ítem oculto)
#   - P → Jugador
#   - E → Enemigo
#   - O → Portal (la puerta de salida)
#
# Además:
#   • Asigna ítems aleatorios dentro de bloques destruibles.
#   • Garantiza que *siempre* exista exactamente 1 llave por nivel.
#
# Parámetros:
#   game    → instancia de GamePlayScreen que almacenará las entidades
#   matrix  → mapa del nivel como matriz de caracteres
# ==========================================================
def generate_entities(game, matrix):
    # Lista para rastrear todos los bloques destruibles,
    # útil para asignar la llave si no aparece aleatoriamente.
    destructible_blocks = []

    # Marca si ya se generó una llave en forma aleatoria
    key_generated = False

    # ------------------------------------------------------
    # Recorrer toda la matriz del nivel
    # ------------------------------------------------------
    for y, row in enumerate(matrix):
        for x, char in enumerate(row):

            # ----------------------------------------------
            # 'S' → bloque sólido indestructible
            # ----------------------------------------------
            if char == "S":
                game.blocks.append(IndestructibleBlock(x, y))

            # ----------------------------------------------
            # 'B' → bloque destructible (puede tener ítem oculto)
            # ----------------------------------------------
            elif char == "B":
                hidden_item = None

                # Intento aleatorio de generar un ítem
                if random.random() < DROP_RATE:
                    hidden_item = random.choice(POWERUP_TYPES)

                    # Si salió una llave → marcar que ya existe
                    if hidden_item == "KEY":
                        key_generated = True
                        # Remover KEY para evitar más llaves aleatorias
                        POWERUP_TYPES.remove("KEY")

                # Crear el bloque destruible, asignando ítem o None
                block = DestructibleBlock(x, y, item_hidden=hidden_item)
                game.blocks.append(block)

                # Registrar este bloque para usarlo después si falta la llave
                destructible_blocks.append(block)

            # ----------------------------------------------
            # 'P' → jugador inicial
            # ----------------------------------------------
            elif char == "P":
                game.player = Player(x, y)

            # ----------------------------------------------
            # 'E' → enemigo
            # ----------------------------------------------
            elif char == "E":
                en = Enemy(x, y, name="Ballom")

                # Aplicar modificaciones por dificultad:
                en.move_duration *= game.enemy_speed_mod
                en.ai_type = game.enemy_ai_type

                game.enemies.append(en)

            # ----------------------------------------------
            # 'O' → portal (la puerta)
            # ----------------------------------------------
            elif char == "O":
                game.portal = Portal(x, y)

    # ======================================================
    # GARANTIZAR QUE SIEMPRE EXISTA UNA LLAVE
    # ------------------------------------------------------
    # Si NO se generó llave en ningún bloque aleatoriamente,
    # se elige uno al azar para asignarla manualmente.
    # ======================================================
    if not key_generated:
        # Bloques que no contienen ítem
        no_item_blocks = [b for b in destructible_blocks if b.item_hidden is None]

        # Si hay bloques vacíos → elegir uno de ellos
        if no_item_blocks:
            chosen_block = random.choice(no_item_blocks)
        else:
            # Si todos tienen ítem, se reemplaza uno cualquiera
            chosen_block = random.choice(destructible_blocks)

        # Asignar llave obligatoria
        chosen_block.item_hidden = "KEY"
        key_generated = True
