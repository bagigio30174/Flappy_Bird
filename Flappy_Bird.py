import arcade
import random

# ---------------- Costanti ----------------
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Flappy Bird (Arcade 3.3)"

GRAVITY = -0.5
FLAP_STRENGTH = 8
PIPE_SPEED = 2
PIPE_GAP = 150
PIPE_WIDTH = 80
PIPE_HEIGHT = 400


# ---------------- Uccellino ----------------
class Bird(arcade.SpriteSolidColor):
    def __init__(self):
        super().__init__(30, 30, arcade.color.YELLOW)
        self.center_x = 100
        self.center_y = SCREEN_HEIGHT // 2
        self.change_y = 0

    def update(self, delta_time: float = 1 / 60):
        self.change_y += GRAVITY
        self.center_y += self.change_y


# ------------------ Tubo ------------------
class Pipe(arcade.SpriteSolidColor):
    def __init__(self, x, y, height):
        super().__init__(PIPE_WIDTH, height, arcade.color.GREEN)
        self.center_x = x
        self.center_y = y
        self.change_x = -PIPE_SPEED

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x


# ------------ Finestra di gioco ------------
class FlappyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.SKY_BLUE)

        # Liste di immagini
        self.bird_list = arcade.SpriteList()
        self.pipe_list = arcade.SpriteList()

        self.bird = None
        self.score = 0
        self.game_over = False

    # ------------------ Setup ------------------
    def setup(self):
        self.bird_list.clear()
        self.pipe_list.clear()

        self.score = 0
        self.game_over = False

        # Bird
        self.bird = Bird()
        self.bird_list.append(self.bird)

        self.spawn_pipes()

    # ------------------ Tubi ------------------
    def spawn_pipes(self):
        gap_y = random.randint(200, 400)
        x = SCREEN_WIDTH + PIPE_WIDTH

        self.pipe_list.append(
            Pipe(x, gap_y - PIPE_GAP // 2 - PIPE_HEIGHT // 2, PIPE_HEIGHT)
        )
        self.pipe_list.append(
            Pipe(x, gap_y + PIPE_GAP // 2 + PIPE_HEIGHT // 2, PIPE_HEIGHT)
        )

    # ------------------ Disegno ------------------
    def on_draw(self):
        self.clear()

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
                "GAME OVER",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
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

        self.bird_list.update(delta_time)
        self.pipe_list.update(delta_time)

        # Collisioni
        if arcade.check_for_collision_with_list(self.bird, self.pipe_list):
            self.game_over = True

        # Limiti schermo
        if self.bird.center_y < 0 or self.bird.center_y > SCREEN_HEIGHT:
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
                self.setup()
            else:
                self.bird.change_y = FLAP_STRENGTH


# ------------------ Main ------------------
def main():
    game = FlappyGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()

