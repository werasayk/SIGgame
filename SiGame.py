import random

import arcade
import arcade.gui

WIDTH = 800
HEIGHT = 600


class GamePause(arcade.View):
    def __init__(self, contgame):
        super().__init__()
        self.sound_click = arcade.Sound('Sounds/Click.mp3')
        self.box = arcade.gui.UIBoxLayout()
        self.manage = arcade.gui.UIManager()
        self.manage.enable()
        self.contgame = contgame

        self.box = arcade.gui.UIBoxLayout()
        arcade.set_background_color(arcade.color.AMAZON)

        self.start_button = arcade.gui.UIFlatButton(text='Start Window')
        self.box.add(self.start_button.with_space_around(bottom=20))

        self.proceed_button = arcade.gui.UIFlatButton(text='Proceed')
        self.box.add(self.proceed_button.with_space_around(bottom=20))

        self.start_button.on_click = self.on_click_start
        self.proceed_button.on_click = self.on_click_procced

        self.manage.add(arcade.gui.UIAnchorWidget(
            anchor_x='center_x',
            anchor_y='center_y',
            child=self.box
        ))

    def on_draw(self):
        arcade.start_render()
        self.clear()
        player = self.contgame.player_list
        coin = self.contgame.coin_list
        player.draw(pixelated=True)
        coin.draw(pixelated=True)
        self.manage.draw()
        out = 'pause'
        arcade.draw_text(out, 350, 400, arcade.color.RED, 30)

    def on_click_start(self, event):
        menu = ManageWindows()
        self.sound_click.play(0.3, 0)
        self.window.show_view(menu)

    def on_click_procced(self, event):
        self.sound_click.play(0.3, 0)
        self.window.show_view(self.contgame)


class ManageWindows(arcade.View):
    def __init__(self):
        super().__init__()
        self.sound_click = arcade.Sound('Sounds/Click.mp3')

        self.up = arcade.key.W
        self.right = arcade.key.D
        self.down = arcade.key.S
        self.left = arcade.key.A

        self.manage = arcade.gui.UIManager()
        self.manage.enable()
        self.box = arcade.gui.UIBoxLayout()
        arcade.set_background_color(arcade.color.AMAZON)
        self.text = arcade.gui.UITextArea(text='',
                                          width=400,
                                          height=100,
                                          font_name="Calibri",
                                          font_size=15,
                                          text_color=arcade.color.WHITE
                                          )
        self.box.add(self.text.with_space_around(bottom=20))

        self.start_button = arcade.gui.UIFlatButton(text='Start')
        self.box.add(self.start_button.with_space_around(bottom=20))
        self.start_button.on_click = self.on_click_start
        self.setting_buton = arcade.gui.UIFlatButton(text='Setting')
        self.box.add(self.setting_buton.with_space_around(bottom=20))
        self.setting_buton.on_click = self.on_click_setting
        self.exit_buton = arcade.gui.UIFlatButton(text='Exit')
        self.box.add(self.exit_buton.with_space_around(bottom=20))
        self.exit_buton.on_click = self.on_click_exit
        self.manage.add(arcade.gui.UIAnchorWidget(
            anchor_x='center_x',
            anchor_y='center_y',
            child=self.box
        ))

    def on_draw(self):
        arcade.start_render()
        self.clear()
        self.manage.draw()

    def on_click_start(self, event):
        game = MyGame(right=self.right, up=self.up, left=self.left, down=self.down)

        self.sound_click.play(0.3, 0)
        self.window.show_view(game)

    def on_click_setting(self, event):
        setting = Setting()
        self.sound_click.play(0.3, 0)
        self.window.show_view(setting)

    @staticmethod
    def on_click_exit(event):
        arcade.close_window()


class Setting(arcade.View):
    def __init__(self):
        super().__init__()

        self.sound_click = arcade.Sound('Sounds/Click.mp3')
        self.manage = arcade.gui.UIManager()
        self.manage.enable()
        self.box = arcade.gui.UIBoxLayout()

        self.up = arcade.key.W
        self.right = arcade.key.D
        self.down = arcade.key.S
        self.left = arcade.key.A
        arcade.set_background_color(arcade.color.AMAZON)

        self.play_button = arcade.gui.UIFlatButton(text='Play')
        self.change_button = arcade.gui.UIFlatButton(text='Change:\n'
                                                          'WASD --> Arrows', width=200)
        self.box.add(self.change_button.with_space_around(bottom=20))
        self.box.add(self.play_button.with_space_around(bottom=20))
        self.change_button.on_click = self.on_click_change
        self.play_button.on_click = self.on_click_play
        self.manage.add(arcade.gui.UIAnchorWidget(
            anchor_x='center_x',
            anchor_y='center_y',
            child=self.box
        ))

    def on_draw(self):
        arcade.start_render()
        self.clear()
        self.manage.draw()

    def on_click_change(self, event):
        self.up = arcade.key.UP
        self.right = arcade.key.RIGHT
        self.down = arcade.key.DOWN
        self.left = arcade.key.LEFT

    def on_click_play(self, event):
        game = MyGame(up=self.up, right=self.right, down=self.down, left=self.left)

        self.sound_click.play(0.3, 0)
        self.window.show_view(game)


class MyGame(arcade.View):
    def __init__(self, right, up, down, left):
        super().__init__()

        self.right = right
        self.up = up
        self.left = left
        self.down = down
        self.sound_click = arcade.Sound('Sounds/Click.mp3')

        self.sound_win = arcade.Sound('Sounds/Win.mp3')

        self.sound_money = arcade.Sound('Sounds/money.mp3')
        self.sound_fon = arcade.Sound('Sounds/fon.mp3')

        self.value = 0.05
        self.score = 0
        self.wins = 0
        self.list_zero = []
        self.player_list = arcade.SpriteList()
        self.player = arcade.AnimatedWalkingSprite()

        self.player.stand_right_textures = []
        self.player.stand_right_textures.append(arcade.load_texture('Sprites/RIGHT1-16x18.png'))
        self.player.walk_right_textures = []
        self.player.walk_right_textures.append(arcade.load_texture('Sprites/RIGHT1-16x18.png'))
        self.player.walk_right_textures.append(arcade.load_texture('Sprites/RIGHT2-16x18.png'))
        self.player.walk_right_textures.append(arcade.load_texture('Sprites/RIGHT3-16x18.png'))

        self.player.stand_left_textures = []
        self.player.stand_left_textures.append(arcade.load_texture('Sprites/LEFT1-16x18.png'))
        self.player.walk_left_textures = []
        self.player.walk_left_textures.append(arcade.load_texture('Sprites/LEFT1-16x18.png'))
        self.player.walk_left_textures.append(arcade.load_texture('Sprites/LEFT2-16x18.png'))
        self.player.walk_left_textures.append(arcade.load_texture('Sprites/LEFT3-16x18.png'))

        self.player.walk_up_textures = []
        self.player.walk_up_textures.append(arcade.load_texture('Sprites/UP1-16x18.png'))
        self.player.walk_up_textures.append(arcade.load_texture('Sprites/UP2-16x18.png'))
        self.player.walk_up_textures.append(arcade.load_texture('Sprites/UP3-16x18.png'))

        self.player.walk_down_textures = []
        self.player.walk_down_textures.append(arcade.load_texture('Sprites/DOWN1-16x18.png'))
        self.player.walk_down_textures.append(arcade.load_texture('Sprites/DOWN2-16x18.png'))
        self.player.walk_down_textures.append(arcade.load_texture('Sprites/DOWN3-16x18.png'))

        self.player.center_x = 400
        self.player.center_y = 300
        self.player.scale = 3.5
        self.player_list.append(self.player)
        self.spikes_list = arcade.SpriteList()

        self.coin_list = arcade.SpriteList()
        for j in range(5):
            self.spike = arcade.Sprite('Sprites/spikes.png', 0.1)
            self.spike.scale = 0.07
            self.spike.center_x = random.randint(30, 770)
            self.spike.center_y = random.randint(30, 570)
            self.spikes_list.append(self.spike)

        self.fon = arcade.Sprite('Sprites/fon.png', center_x=400, center_y=300)
        for j in range(15):
            coin = arcade.Sprite('Sprites/coin.png', 0.1)
            coin.scale = 0.07
            coin.center_x = random.randint(30, 770)
            coin.center_y = random.randint(30, 570)
            self.coin_list.append(coin)

        self.emitter1 = arcade.Emitter((self.player.center_x, self.player.center_y),
                                       emit_controller=arcade.EmitBurst(100),
                                       particle_factory=lambda emitter: arcade.FadeParticle(
                                           filename_or_texture='Sprites/bumper.png',
                                           change_xy=arcade.rand_in_rect((-2, -2), 4, 4),
                                           lifetime=1,
                                           start_alpha=100,
                                           end_alpha=50,

                                       ))

    def on_draw(self):
        arcade.start_render()
        self.clear()
        self.fon.draw(pixelated=True)
        self.coin_list.draw(pixelated=True)
        self.spikes_list.draw(pixelated=True)
        self.player_list.draw(pixelated=True)
        self.emitter1.draw()
        score = f"Score: {self.score}"
        arcade.draw_text(score, 20, 550, arcade.color.GOLD, 30)
        wins = f'Wins: {self.wins}'
        arcade.draw_text(wins, 630, 550, arcade.color.GOLD, 30)

    def on_update(self, delta_time):
        self.player_list.update()
        self.player_list.update_animation()
        self.coin_list.update_animation()
        self.emitter1.update()
        coin_hit_list = arcade.check_for_collision_with_list(self.player, self.coin_list, )
        for i in coin_hit_list:
            i.remove_from_sprite_lists()
            self.emitter1 = arcade.Emitter((self.player.center_x, self.player.center_y),
                                           emit_controller=arcade.EmitBurst(100),
                                           particle_factory=lambda emitter: arcade.FadeParticle(
                                               filename_or_texture='Sprites/bumper.png',
                                               change_xy=arcade.rand_in_rect((-2, -2), 4, 4),
                                               lifetime=1,
                                               start_alpha=100,
                                               end_alpha=50

                                           ))

            self.sound_money.play(0.3, 0)

            self.score += 1

            if self.score == 15:
                self.sound_win.play(0.3, 0)
                self.score = 0
                self.wins += 1
                for j in range(15):
                    coin = arcade.Sprite('Sprites/coin.png', 0.1)
                    coin.center_x = random.randint(30, 770)
                    coin.center_y = random.randint(30, 570)
                    coin.scale = 0.07
                    self.coin_list.append(coin)
        spike_hit_list = arcade.check_for_collision_with_list(self.player, self.spikes_list)

        for i in spike_hit_list:
            i.center_x = random.randint(30, 770)
            i.center_y = random.randint(30, 570)

            if self.score >= 5:
                self.score -= 5
                for j in range(5):
                    coin = arcade.Sprite('Sprites/coin.png', 0.1)
                    coin.scale = 0.07
                    coin.center_x = self.player.center_x + random.randint(70, 100)
                    coin.center_y = self.player.center_y + random.randint(70, 100)
                    self.coin_list.append(coin)
            if self.score < 0:
                self.score = 0
                for o in self.spikes_list:
                    o.remove_from_sprite_lists()
                for j in self.coin_list:
                    j.remove_from_sprite_lists()

                for k in range(15):
                    coin = arcade.Sprite('Sprites/coin.png', 0.1)
                    coin.center_x = random.randint(30, 770)
                    coin.center_y = random.randint(30, 570)
                    coin.scale = 0.07
                    self.coin_list.append(coin)
                for m in range(5):
                    self.spike = arcade.Sprite('Sprites/spikes.png', 0.1)
                    self.spike.scale = 0.1
                    self.spike.center_x = random.randint(30, 770)
                    self.spike.center_y = random.randint(30, 570)
                    self.spikes_list.append(self.spike)
            if self.coin_list == self.list_zero and self.score < 15:
                for k in range(15):
                    coin = arcade.Sprite('Sprites/coin.png', 0.1)
                    coin.center_x = random.randint(30, 770)
                    coin.center_y = random.randint(30, 570)
                    coin.scale = 0.07
                    self.coin_list.append(coin)

        if self.player.center_x > 800:
            self.player.change_x = -2
        if self.player.center_x < 0:
            self.player.change_x = 2
        if self.player.center_y > 600:
            self.player.change_y = -2
        if self.player.center_y < 0:
            self.player.change_y = 2

    def on_key_press(self, symbol, modifiers):
        if symbol == self.right:
            self.player.change_x = 6

        if symbol == self.left:
            self.player.change_x = -6

        if symbol == self.up:
            self.player.change_y = 6

        if symbol == self.down:
            self.player.change_y = -6

        if symbol == arcade.key.ESCAPE:
            self.sound_click.play(0.3, 0)

            pause = GamePause(self)
            self.window.show_view(pause)
        if symbol == arcade.key.F:
            self.sound = arcade.play_sound(self.sound_fon, 0.05, looping=True)
        if symbol == arcade.key.C:
            self.sound.pause()

    def on_key_release(self, symbol, modifiers):
        if symbol == self.right:
            self.player.change_x = 0

        if symbol == self.left:
            self.player.change_x = 0

        if symbol == self.up:
            self.player.change_y = 0

        if symbol == self.down:
            self.player.change_y = 0


def main():
    display = arcade.Window(WIDTH, HEIGHT, "Итоговая игра")
    menu = ManageWindows()
    display.show_view(menu)

    arcade.run()


main()
