import arcade
import random
from pathlib import Path

# ------------------ Percorso ------------------
BASE_DIR = Path(__file__).parent
ASSETS = BASE_DIR / "assets"

# ---------------- Costanti ----------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
SCREEN_TITLE = "Flappy Bird (Arcade 3.3)"

GRAVITY = -0.5
FLAP_STRENGTH = 8
PIPE_SPEED = 2
PIPE_GAP = 150
PIPE_WIDTH = 80
PIPE_HEIGHT = 400
BIRD_SCALE = 0.6
PIPE_SCALE = 1.0
BACKGROUND_SPEED = 1
BACKGROUND_SCALE = 1.0


# ---------------- Uccellino ----------------
class Bird(arcade.Sprite):
    def __init__(self):
        super().__init__(ASSETS / "bird.png", BIRD_SCALE)
        self.center_x = 100
        self.center_y = SCREEN_HEIGHT // 2
        self.change_y = 0

    def update(self, delta_time: float = 1 / 60):
        self.change_y += GRAVITY
        self.center_y += self.change_y


# ------------------ Tubo ------------------
class Pipe(arcade.Sprite):
    def __init__(self, x, y, flipped=False):
        super().__init__(ASSETS / "pipe.png", PIPE_SCALE)
        self.center_x = x
        self.center_y = y
        self.change_x = -PIPE_SPEED

        if flipped:
            self.angle = 180

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x


# ------------ Finestra di gioco ------------
class FlappyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Liste di immagini
        self.background_list = arcade.SpriteList()
        self.bird_list = arcade.SpriteList()
        self.pipe_list = arcade.SpriteList()

        self.bird = None
        self.score = 0
        self.game_over = False
        self.primo_avvio = True

        # Suoni
        self.flap_sound = arcade.load_sound(ASSETS / "flap.wav")
        self.hit_sound = arcade.load_sound(ASSETS / "hit.wav")
        self.score_sound = arcade.load_sound(ASSETS / "score.wav")

    # ------------------ Setup ------------------
    def setup(self):
        self.background_list.clear()
        self.bird_list.clear()
        self.pipe_list.clear()

        self.score = 0
        if self.primo_avvio:
            self.game_over = True
        else:
            self.game_over = False

        # Immagine di sfondo (2 per alternarle)
        bg1 = arcade.Sprite(ASSETS / "background.png", BACKGROUND_SCALE)
        bg1.left = 0
        bg1.bottom = 0

        bg2 = arcade.Sprite(ASSETS / "background.png", BACKGROUND_SCALE)
        bg2.left = bg1.width
        bg2.bottom = 0

        self.background_list.extend([bg1, bg2])

        # Bird
        self.bird = Bird()
        self.bird_list.append(self.bird)

        self.spawn_pipes()

    # ------------------ Tubi ------------------
    def spawn_pipes(self):
        gap_y = random.randint(200, 400)
        x = SCREEN_WIDTH + PIPE_WIDTH

        self.pipe_list.append(
            Pipe(x, gap_y - PIPE_GAP // 2 - PIPE_HEIGHT // 2, flipped=False)
        )
        self.pipe_list.append(
            Pipe(x, gap_y + PIPE_GAP // 2 + PIPE_HEIGHT // 2, flipped=True)
        )

        arcade.play_sound(self.score_sound)

    # ------------------ Disegno ------------------
    def on_draw(self):
        self.clear()

        self.background_list.draw()
        self.bird_list.draw()
        self.pipe_list.draw()

        arcade.draw_text(
            f"Score: {self.score}",
            10,
            SCREEN_HEIGHT - 30,
            arcade.color.BLACK,
            16
        )

        if self.game_over:
            arcade.draw_text(
                "Premi SPAZIO per iniziare",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 48,
                arcade.color.RED,
                24,
                anchor_x="center",
                anchor_y="center",
                align="center"
            )
            arcade.draw_text(
                "Premi ESC per uscire",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                arcade.color.RED,
                24,
                anchor_x="center",
                anchor_y="center",
                align="center"
            )
            if not self.primo_avvio:
                arcade.draw_text(
                    "GAME OVER",
                    SCREEN_WIDTH // 2,
                    SCREEN_HEIGHT // 2 - 48,
                    arcade.color.RED,
                    24,
                    anchor_x="center",
                    anchor_y="center",
                    align="center"
                )

    # -------------- Ciclo di aggiornamento --------------
    def on_update(self, delta_time):
        if self.game_over:
            return

        # Scorrimento sfondo
        for bg in self.background_list:
            bg.center_x -= BACKGROUND_SPEED

            if bg.right <= 0:
                bg.left = max(b.right for b in self.background_list)

        self.bird_list.update(delta_time)
        self.pipe_list.update(delta_time)

        # Collisioni
        if arcade.check_for_collision_with_list(self.bird, self.pipe_list):
            arcade.play_sound(self.hit_sound)
            self.game_over = True

        # Limiti schermo
        if self.bird.center_y < 0 or self.bird.center_y > SCREEN_HEIGHT:
            arcade.play_sound(self.hit_sound)
            self.game_over = True

        # Genera tubi e aggiorna punteggio
        if len(self.pipe_list) == 0 or self.pipe_list[-1].center_x < SCREEN_WIDTH - PIPE_HEIGHT // 2:
            self.spawn_pipes()
            self.score += 1

        # Rimuovi i tubi fuori dallo schermo
        for pipe in self.pipe_list[:]:
            if pipe.right < 0:
                pipe.remove_from_sprite_lists()

    # ------------------ Input ------------------
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            if self.game_over:
                if self.primo_avvio:
                    self.primo_avvio = False
                self.setup()
            else:
                self.bird.change_y = FLAP_STRENGTH
                arcade.play_sound(self.flap_sound)

        elif key == arcade.key.ESCAPE:
            # Quit the game
            arcade.close_window()


# ------------------ Main ------------------
def main():
    game = FlappyGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()

