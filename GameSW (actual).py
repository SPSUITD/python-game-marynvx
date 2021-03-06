import arcade


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640
SCREEN_TITLE = "Sweet world"

TILE_SCALING = 1
CHARACTER_SCALING = 0.5

COIN_SCALING = 0.5

PLAYER_X_SPEED = 4
PLAYER_Y_SPEED = 5

JUMP_MAX_HEIGHT = 130

PLAYER_SPRITE_IMAGE_CHANGE_SPEED = 20

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

        self.gui_camera = None
        self.score = 0

        self.coin_list = None
        self.coin_coordinate_list = None
        self.coin_c = None
       

        #self.level = 1

       # arcade.set_background_color(arcade.csscolor.PINK)

    def setup(self):

        self.player_list = arcade.SpriteList()
        image_source = "Pics/zefir1.png"

        self.coin_list = arcade.SpriteList(use_spatial_hash=True)

        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 92
        self.player_list.append(self.player_sprite)

        for i in range(1, 3):
            self.player_sprite_images.append(arcade.load_texture(f"Pics/zefir{i}.png"))
        for i in range(2, 0, -1):
            self.player_sprite_images_left.append(arcade.load_texture(f"Pics/zefir{i}.png", flipped_horizontally=True))

        self.player_sprite_image_standing = arcade.load_texture(f"Pics/zefir_standing.png")
        self.player_sprite_image_jump = arcade.load_texture(f"Pics/zefir_jump.png")

        
            

        self.jump_start = self.player_sprite.center_x


        map_name = f"NewSweetMapDay/newsweetmap.json"

        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            },
            #"Coins": {
                #"use_spatial_hash": True
           # }
        }

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        #self.coin_list = arcade.SpriteList()
        coin_coordinate_list = [[128,410],[670,410],[512,90]]
        
        for coordinate in coin_coordinate_list:
            coin = arcade.Sprite (
                "Pics/coin.png", COIN_SCALING
            )
            coin.center_x = coordinate[0]
            coin.center_y = coordinate[1]
        
            #coin_c = coordinate
            self.coin_list.append(coin)


        self.scene = arcade.Scene.from_tilemap(self.tile_map)

       
        self.gui_camera = arcade.Camera(self.width, self.height)
        self.score = 0

        

    def on_draw(self):
        self.clear()
        self.scene.draw()
        self.coin_list.draw()
        self.player_list.draw()

        self.gui_camera.use()

        #if self.score == 3:
            #self.level += 1

        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            610,
            arcade.csscolor.WHITE,
            18,
        )

    

    def coin_collision(self):

        for coi in self.coin_list["Coins"]:
            if (self.player_sprite.center_x + self.player_sprite.width / 2 >= coi.center_x - coi.width / 2 and self.player_sprite.center_x - self.player_sprite.width / 2 <= coi.center_x + coi.width / 2) \
                    and (self.player_sprite.center_y + self.player_sprite.height / 2 >= coi.center_y - coi.height / 2 and self.player_sprite.center_y - self.player_sprite.height / 2 <= coi.center_y + coi.height / 2):
                self.coin_collide = True
            

    '''def hit_coin(self):
        self.coin_collision()
        if self.coin_collide:
            for i in self.coin_list:
                if i == self.coin_c:
                    self.coin_list.remove(i)
                    self.score +=1'''


    def calculate_collision(self):

        for block in self.scene["Platforms"]:
            if (self.player_sprite.center_x + self.player_sprite.width / 2 >= block.center_x - block.width / 2 and self.player_sprite.center_x - self.player_sprite.width / 2 <= block.center_x + block.width / 2) \
                    and (self.player_sprite.center_y + self.player_sprite.height / 2 >= block.center_y - block.height / 2 and self.player_sprite.center_y - self.player_sprite.height / 2 <= block.center_y + block.height / 2):
                self.collide = True
                


    def on_update(self, delta_time: float):
        self.player_movement()
        if self.player_jump:
            self.collide = False
        else:
            self.calculate_collision()

        '''self.coin_collision()
        if self.coin_collide == True:
            for i in self.coin_list:
                if i == self.coin_coordinate_list:
                    self.coin_list.remove(i)
                    self.score += 1'''

        '''coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.coin_list
        )

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1'''

        



    def player_movement(self):
        if self.collide:
            #self.player_dx = 0
            self.player_dy = 0
        else:
            self.player_dx = PLAYER_X_SPEED
            self.player_dy = PLAYER_Y_SPEED

        if self.key_right_pressed:
            self.player_sprite.center_x += self.player_dx
            self.player_sprite.texture = self.player_sprite_images[int(self.player_sprite.center_x / PLAYER_SPRITE_IMAGE_CHANGE_SPEED) % 2]
            
        if self.key_left_pressed:
            self.player_sprite.center_x -= self.player_dx
            self.player_sprite.texture = self.player_sprite_images_left[int(self.player_sprite.center_x / PLAYER_SPRITE_IMAGE_CHANGE_SPEED) % 2]

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
            self.player_sprite.texture = self.player_sprite_image_jump

    def on_key_release(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.key_right_pressed = False
            self.player_sprite.texture = self.player_sprite_image_standing
        elif key == arcade.key.LEFT:
            self.key_left_pressed = False
            self.player_sprite.texture = self.player_sprite_image_standing
        elif key == arcade.key.UP:
            self.player_sprite.change_y = 0
            self.player_sprite.texture = self.player_sprite_image_standing



def main():
    window = gameSW()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()