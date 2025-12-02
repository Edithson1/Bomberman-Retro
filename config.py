# ===========================
# CONFIGURACIÓN GLOBAL
# ===========================

WIDTH = 1024
HEIGHT = 576
FPS = 60

# Colores generales
COLOR_BG = (10, 10, 20)
COLOR_PANEL = (20, 20, 40)
COLOR_BUTTON = (80, 20, 150)
COLOR_BUTTON_HOVER = (140, 60, 220)
COLOR_TEXT = (255, 255, 255)
DIFFICULTY_CONFIG = {
    "Fácil": {
        "player_lives": 5,
        "enemy_speed": 8,
        "enemy_ai": "random",
        "bomb_time": 2000,
        "extra_fire": 0,
        "powerup_drop_rate": 0.20,
        "time_limit": None,
        "increase_blocks": 0
    },

    "Medio": {
        "player_lives": 3,
        "enemy_speed": 4,
        "enemy_ai": "avoid_bombs",
        "bomb_time": 1800,
        "extra_fire": 0,
        "powerup_drop_rate": 0.10,
        "time_limit": 150 * 1000,
        "increase_blocks": 0
    },

    "Difícil": {
        "player_lives": 1,
        "enemy_speed": 1,
        "enemy_ai": "chase_player",
        "bomb_time": 1500,
        "extra_fire": 1,
        "powerup_drop_rate": 0.04,
        "time_limit": 90 * 1000,
        "increase_blocks": 0
    }
}
FONT_PATH = "assets/fonts/game.ttf"
LOCK_IMAGE_PATH = "assets/images/lock.png"

MUSIC_MENU = "assets/music/menu.mp3"
MUSIC_DIFFICULTY = "assets/music/menu.mp3"
MUSIC_LEVEL_SELECT = "assets/music/menu.mp3"
MUSIC_GAME = "assets/music/menu.mp3"
MUSIC_VICTORY = "assets/music/menu.mp3"
MUSIC_DEFEAT = "assets/music/menu.mp3"

SAVE_FILE = "save.json"

DIFFICULTIES = ["Fácil", "Medio", "Difícil"]
LEVELS_PER_DIFFICULTY = 5
