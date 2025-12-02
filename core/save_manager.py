import json
import os
from config import SAVE_FILE, DIFFICULTIES, LEVELS_PER_DIFFICULTY

# ======================================================
# DEFAULT_DATA
# ------------------------------------------------------
# Estructura base de los datos de guardado.
# Contiene:
#   - Qué niveles están desbloqueados por dificultad
#   - Última dificultad seleccionada
#   - Último nivel seleccionado
#
# Inicialmente, solo el nivel 1 de Fácil está desbloqueado.
# ======================================================
DEFAULT_DATA = {
    "levels_unlocked": {
        d: [False] * LEVELS_PER_DIFFICULTY for d in DIFFICULTIES
    },
    "selected_difficulty": "Fácil",
    "selected_level": 0
}

# Nivel 1 de Fácil desbloqueado desde el inicio
DEFAULT_DATA["levels_unlocked"]["Fácil"][0] = True


class SaveManager:

    # ======================================================
    # load()
    # ------------------------------------------------------
    # Carga el archivo SAVE_FILE.
    # Si no existe o está dañado, se crea uno nuevo usando DEFAULT_DATA.
    #
    # return: diccionario con la información guardada.
    # ======================================================
    @staticmethod
    def load():
        # Si el archivo no existe → crearlo con datos por defecto
        if not os.path.exists(SAVE_FILE):
            SaveManager.save(DEFAULT_DATA)
            return DEFAULT_DATA

        try:
            # Intentar cargar archivo JSON
            with open(SAVE_FILE, "r") as f:
                return json.load(f)
        except:
            # Si hay error en lectura o formato inválido → reset
            SaveManager.save(DEFAULT_DATA)
            return DEFAULT_DATA

    # ======================================================
    # save(data)
    # ------------------------------------------------------
    # Guarda el diccionario "data" dentro del archivo SAVE_FILE.
    # Este archivo almacena el progreso del jugador.
    # ======================================================
    @staticmethod
    def save(data):
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f, indent=4)

    # ======================================================
    # unlock_next(data, difficulty, index)
    # ------------------------------------------------------
    # Se llama cuando el jugador gana un nivel.
    #
    # Su propósito:
    #   1. Desbloquear el siguiente nivel dentro de la misma dificultad.
    #   2. Si ya no quedan niveles, desbloquear el primer nivel
    #      de la siguiente dificultad.
    #
    # return:
    #   data (modificado)
    #   next_difficulty  -> dificultad recién desbloqueada o la misma
    #   next_index       -> índice del nivel desbloqueado
    #
    # Si no hay más niveles ni dificultades → (data, None, None)
    # ======================================================
    @staticmethod
    def unlock_next(data, difficulty, index):
        diffs = DIFFICULTIES
        diff_i = diffs.index(difficulty)

        # ---------------------------------------
        # 1. Buscar siguiente nivel en la MISMA dificultad
        # ---------------------------------------
        for i in range(index + 1, LEVELS_PER_DIFFICULTY):

            # Si ya está desbloqueado → simplemente ir allí
            if data["levels_unlocked"][difficulty][i] == True:
                return data, difficulty, i

            # Si está bloqueado → desbloquear este nivel
            if not data["levels_unlocked"][difficulty][i]:
                data["levels_unlocked"][difficulty][i] = True
                return data, difficulty, i

        # ---------------------------------------
        # 2. Si se terminó la dificultad actual → pasar a la siguiente
        # ---------------------------------------
        for d in diffs[diff_i + 1:]:
            for i in range(LEVELS_PER_DIFFICULTY):
                if not data["levels_unlocked"][d][i]:
                    data["levels_unlocked"][d][i] = True
                    return data, d, i

        # ---------------------------------------
        # 3. Si no queda nada por desbloquear
        # ---------------------------------------
        return data, None, None
