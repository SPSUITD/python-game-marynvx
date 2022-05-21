import arcade


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640
SCREEN_TITLE = "Sweet world"

TILE_SCALING = 1
CHARACTER_SCALING = 0.5

PLAYER_X_SPEED = 3
PLAYER_Y_SPEED = 5

JUMP_MAX_HEIGHT = 200

class gameSW(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.tile_map = None
        self.player_list = None

        self.player_sprite = None

        self.key_right_pressed = False
        self.key_left_pressed = False
        #self.key_up_pressed = False

        self.player_jump = False
        self.jump_start = None

        self.player_dx = PLAYER_X_SPEED
        self.player_dy = PLAYER_Y_SPEED

        self.collide = False

        self.player_sprite_images = []
        self.player_sprite_images_left = []

       # arcade.set_background_color(arcade.csscolor.PINK)

    def setup(self):



        self.player_list = arcade.SpriteList()
        image_source = "Картинки/zefir1.png"

        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 92
        self.player_list.append(self.player_sprite)

        for i in range(1, 3):
            self.player_sprite_images.append(arcade.load_texture(f"Картинки/zefir{i}.png"))
        for i in range(2, 0, -1):
            self.player_sprite_images_left.append(arcade.load_texture(f"Картинки/zefir{i}.png", flipped_horizontally=True))

        self.jump_start = self.player_sprite.center_x


        map_name = "SweetMapDay/mapday.json"

        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            },
        }

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

    def on_draw(self):
        self.clear()
        self.scene.draw()
        self.player_list.draw()


    def calculate_collision(self):

        for block in self.scene["Platforms"]:
            if (self.player_sprite.center_x + self.player_sprite._get_width() / 2 >= block.center_x - block._get_width() / 2 and self.player_sprite.center_x - self.player_sprite._get_width() / 2 <= block.center_x + block._get_width() / 2) \
                    and (self.player_sprite.center_y + self.player_sprite._get_height() / 2 >= block.center_y - block._get_height() / 2 and self.player_sprite.center_y - self.player_sprite._get_height() / 2 <= block.center_y + block._get_height() / 2):
                self.collide = True


    def on_update(self, delta_time: float):
        #self.physics_engine.update()
        self.player_movement()
        if self.player_jump:
            self.collide = False
        else:
            self.calculate_collision()

    def player_movement(self):
        if self.collide:
            self.player_dy = 0
        else:
            self.player_dx = PLAYER_X_SPEED
            self.player_dy = PLAYER_Y_SPEED

        if self.key_right_pressed:
            self.player_sprite.center_x += self.player_dx
        if self.key_left_pressed:
            self.player_sprite.center_x -= self.player_dx

        if self.player_jump:
            self.player_sprite.center_y += self.player_dy
            if self.player_sprite.center_y > self.jump_start + JUMP_MAX_HEIGHT:
                self.player_jump = False
        else:
            self.player_sprite.center_y -= self.player_dy


    def on_key_press(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.key_right_pressed = True
        elif key == arcade.key.LEFT:
            self.key_left_pressed = True
        elif key == arcade.key.UP:
            self.player_jump = True
            self.jump_start = self.player_sprite.center_y

    def on_key_release(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.key_right_pressed = False
        elif key == arcade.key.LEFT:
            self.key_left_pressed = False
        elif key == arcade.key.UP:
            self.player_sprite.change_y = 0

def main():
    window = gameSW()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()