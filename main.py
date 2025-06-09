import pygame, sys
import random as r
from scripts.background import Background
from scripts.player import Player
from scripts.space_object import Object_Behaviour
from scripts.laser import Laser
from scripts.file_manager import load_data, save_data, load_numbers, save_numbers, reset_files, ensure_void_runner_folder

class Game:
    def __init__(self):
        ensure_void_runner_folder()
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480), pygame.SCALED|pygame.FULLSCREEN)  # Set the window size
        pygame.display.set_caption("Void Runner")
        self.clock = pygame.time.Clock()

        self.assets = {
            'background': pygame.image.load('assets/images/background.png'),
            'player1': pygame.image.load('assets/images/player1.png'),
            'player2': pygame.transform.scale(pygame.image.load('assets/images/player2.png'), (40, 40)),
            'player3': pygame.transform.scale(pygame.image.load('assets/images/player3.png'), (40, 40)),
            'player4': pygame.transform.scale(pygame.image.load('assets/images/player4.png'), (40, 40)),
            'orb': pygame.transform.scale(pygame.image.load('assets/images/orb.png'), (18, 18)),
            'obstacle': pygame.transform.scale(pygame.image.load('assets/images/obstacle.png'), (59, 23)),
            'rock': pygame.transform.scale(pygame.image.load('assets/images/rock.png'), (60, 65)),
            'shift': pygame.image.load('assets/images/shift.png'), 
            'magnet': pygame.transform.scale(pygame.image.load('assets/images/magnet.png'), (29, 33)),
            'orbitron': 'assets/fonts/Orbitron/Orbitron-VariableFont_wght.ttf',
            '2x': pygame.image.load('assets/images/2x.png'),
            'booster': pygame.image.load('assets/images/boost.png'),
            'pause': pygame.image.load('assets/images/pause.png'),
            'coin': pygame.image.load('assets/images/coin.png'),
            'on': pygame.image.load('assets/images/on.png'),
            'off': pygame.image.load('assets/images/off.png'),
            'back': pygame.transform.scale(pygame.image.load('assets/images/back.png'), (40, 25)),
            'next': pygame.transform.scale(pygame.image.load('assets/images/next.png'), (40, 25)),
            'options': pygame.transform.scale(pygame.image.load('assets/images/options.png'), (94, 26)),
            'buy': pygame.transform.scale(pygame.image.load('assets/images/buy.png'), (135, 99)),
            'escape': pygame.transform.scale(pygame.image.load('assets/images/escape.png'), (60, 50)),
            'space': pygame.transform.scale(pygame.image.load('assets/images/space.png'), (100, 47)),
            'left_click': pygame.transform.scale(pygame.image.load('assets/images/left-click.png'), (37, 51)),
            'background_music': 'assets/sfx/background.ogg',
            'orb_sound': 'assets/sfx/orb.wav',
            'boost_sound': 'assets/sfx/boost.wav',
            'shift_sound': 'assets/sfx/shift.wav',
            'laser_sound': 'assets/sfx/laser.wav',
            'powerup_sound': 'assets/sfx/powerup.wav',
            'collision_sound': 'assets/sfx/collision.mp3',
            'rejected_sound': 'assets/sfx/rejected.mp3',
            'kaching_sound': 'assets/sfx/kaching.mp3'
        }

        pygame.display.set_icon(self.assets['player1'])
        self.player_selected = int(load_data('player.txt')) if int(load_data('player.txt')) != 0 else 1 
        self.background = Background(self.assets['background'])
        self.orbs = Object_Behaviour(self.assets['orb'], type='orb', probability=0.005, speed=[2, 0], wait=[0, 180], bouncing=True)
        self.obstacles = Object_Behaviour(self.assets['obstacle'], type='obstacle', probability=0.01, speed=[2, 0], wait=[0, 0])
        self.rocks = Object_Behaviour(self.assets['rock'], type='rock', probability=0.01, speed=[3, 2], wait=[0, 300])
        self.shift = Object_Behaviour(self.assets['shift'], type='shift', probability=0.005, speed=[2, 0], wait=[0, 0], bouncing=True)
        self.magnet = Object_Behaviour(self.assets['magnet'], type='magnet', probability=0.00125, speed=[2, 0], wait=[0, 2400], bouncing=True)
        self.twox = Object_Behaviour(self.assets['2x'], type='2x', probability=0.001, speed=[2, 0], wait=[0, 2400], bouncing=True)
        self.booster = Object_Behaviour(self.assets['booster'], type='booster', probability=0.00125, speed=[2, 0], wait=[0, 3600], bouncing=True)
        self.laser = Laser()
        
        self.high_score = int(load_data('highscore.txt'))
        self.coins = int(load_data('coins.txt'))
        self.music = True if int(load_data('music.txt')) == 1 else False
        self.sfx = True if int(load_data('sfx.txt')) == 1 else False
        self.score = 0
        self.timer = 0
        self.collision = []

    def reset(self):
        self.score = 0 
        self.timer = 0
        self.collision = []
        self.background.reset()
        self.player.reset()
        self.orbs.reset()
        self.obstacles.reset()
        self.rocks.reset()
        self.shift.reset()
        self.magnet.reset()
        self.twox.reset()
        self.booster.reset()
        self.laser.reset()

    def draw_text(self, size=32, text='', pos=[100, 100], colour='#d8d8d8', bold=False, underline=False):
        font = pygame.font.Font(self.assets['orbitron'], size)
        if bold:
            font.bold = True        
        if underline:
            font.underline = True
        word = font.render(text, True, colour)
        self.screen.blit(word, (pos[0], pos[1]))

    def activate_boost(self):
        self.background.boost = True
        self.orbs.boost = True
        self.obstacles.boost = True
        self.rocks.boost = True
        self.shift.boost = True
        self.magnet.boost = True
        self.twox.boost = True

    def deactivate_boost(self):
        self.background.boost = False
        self.orbs.boost = False
        self.obstacles.boost = False
        self.rocks.boost = False
        self.shift.boost = False
        self.magnet.boost = False
        self.twox.boost = False

    def main_menu(self):
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.load(self.assets['background_music'])
        if self.music: pygame.mixer.music.play(-1)
        play = pygame.Rect(230, 210, 190, 60)
        options = pygame.Rect(230, 290, 190, 60)
        store = pygame.Rect(230, 370, 190, 60)
        while True:
            mx, my = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.run()
                    
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if play.collidepoint((mx, my)):
                            self.run()
                        elif options.collidepoint((mx, my)):
                            self.options()
                        elif store.collidepoint((mx, my)):
                            self.store()

            self.background.render(self.screen) 
            self.background.update()

            if play.collidepoint((mx, my)):
                pygame.draw.rect(self.screen, '#1a1b1c', play)
            if options.collidepoint((mx, my)):
                pygame.draw.rect(self.screen, '#1a1b1c', options)
            if store.collidepoint((mx, my)):
                pygame.draw.rect(self.screen, '#1a1b1c', store)

            self.screen.blit(self.assets['coin'], (10, 10))
            self.draw_text(text=str(self.coins), size=16, pos=[45, 15], bold=True)
            self.draw_text(text="HighScore: "+str(self.high_score), size=16, pos=[100, 150])
            self.draw_text(text='Void Runner', size=60, colour='#aabbcc', pos=[100, 50], bold=True, underline=True)
            self.draw_text(text='Play', size=32, colour='#55bbcc', pos=[280, 220], bold=True, underline=True)
            self.draw_text(text='Options', size=32, colour='#ff00c8', pos=[260, 300], bold=True, underline=True)
            self.draw_text(text='Store', size=32, colour='#ffcc08', pos=[275, 380], bold=True, underline=True)
            self.draw_text(text='Music by Abstraction', size=16, bold=True, pos=[450, 428])

            pygame.display.update()
            self.clock.tick(60)
    
    def game_over(self, orbs):
        running = True
        score_coins = self.score // 100
        high_score = self.high_score
        orb_coins = orbs * 5
        total = score_coins + orb_coins
        self.coins += total
        save_data('coins.txt', str(self.coins))
        if self.score > self.high_score:
            self.high_score = self.score
            save_data('highscore.txt', str(self.high_score))  
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    running = False
 
            self.background.render(self.screen)  # Render the background
            self.background.update()

            if self.score > high_score:
                self.draw_text(text='New High Score!', size=32, colour='#00eeff', pos=[10, 5], bold=True)  
            self.draw_text(text='Game Over!', size=50, pos=[150, 50], bold=True, underline=True)
            self.draw_text(text="Score: "+str(self.score), size=20, pos=[50, 150])
            self.draw_text(text="Orbs Collected:", size=20, pos=[50, 200])
            self.draw_text(text=str(orbs), size=20, pos=[250, 200])
            self.screen.blit(self.assets['orb'], (225, 205))
            self.draw_text(text="+", size=20, pos=[400, 150])
            self.draw_text(text="+", size=20, pos=[400, 200])
            self.screen.blit(self.assets['coin'], (420, 150))
            self.screen.blit(self.assets['coin'], (420, 200))
            self.draw_text(text=str(score_coins), size=20, pos=[460, 151])
            self.draw_text(text=str(orb_coins), size=20, pos=[460, 201])
            self.draw_text(text="Total coins received: ", size=20, pos=[150, 300], bold=True, underline=True)
            self.screen.blit(self.assets['coin'], (420, 300))
            self.draw_text(text=str(total), size=20, pos=[460, 301], bold=True)
            self.draw_text(text="Press to main menu...", size=20, pos=[200, 400], colour='#aabbcc', underline=True)    

            pygame.display.update()
            self.clock.tick(60)

    def run(self):
        self.player = Player(self.assets['player' + str(self.player_selected)], [80, 180])

        running = True
        pause = False
        twox = 0
        boost = 0
        dead = False
        dead_timer = 30
        orbs = 0
        offset = [0, 0]
        screen_shake = 0

        #regions
        option_button = pygame.Rect(350, 25, 94, 26)
        pause_button = pygame.Rect(300, 25, 25, 29)

        #sounds
        orb_sound = pygame.mixer.Sound(self.assets['orb_sound'])
        boost_sound = pygame.mixer.Sound(self.assets['boost_sound'])
        shift_sound = pygame.mixer.Sound(self.assets['shift_sound'])
        laser_sound = pygame.mixer.Sound(self.assets['laser_sound'])
        powerup_sound = pygame.mixer.Sound(self.assets['powerup_sound'])
        collision_sound = pygame.mixer.Sound(self.assets['collision_sound'])
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if pause:
                            pause = False
                        else:
                            self.player.jumping = True

                    if event.key == pygame.K_ESCAPE:
                        pause = not pause

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.player.jumping = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if pause:
                            if option_button.collidepoint((mx, my)):
                                self.options()
                            if pause_button.collidepoint((mx, my)):
                                pause = False
                        else:
                            self.player.jumping = True

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.player.jumping = False
                    
            mx, my = pygame.mouse.get_pos()

            if screen_shake:
                offset[0] += r.randint(0, 8) - 4
                offset[1] += r.randint(0, 8) - 4
                screen_shake -= 1
            else:
                offset = [0, 0]

            #rendering
            self.background.render(self.screen, offset=offset)  
            self.obstacles.render(self.screen, offset=offset)
            self.orbs.render(self.screen, offset=offset)
            
            if self.score >= 500:
                self.rocks.render(self.screen, offset=offset)

            if self.score >= 250:
                self.shift.render(self.screen, offset=offset)
                self.magnet.render(self.screen, offset=offset)
                self.twox.render(self.screen, offset=offset)
                self.booster.render(self.screen, offset=offset)
            if self.score >= 1000 and boost == 0:
                self.laser.render(self.screen)
            self.player.render(self.screen, offset=offset)
            
            if pause:
                self.screen.blit(self.assets['pause'], (300, 25))
                self.screen.blit(self.assets['options'], (350, 25))

            #updating
            if not pause and not dead:
                self.background.update()
                self.obstacles.update()
                self.orbs.update()
                if self.score >= 500:
                    self.rocks.update()
                if self.score >= 250:
                    self.shift.update()
                    self.magnet.update()
                    self.twox.update()
                    self.booster.update()
                if self.score >= 1000 and boost == 0:
                    self.laser.update()
                self.player.update()

            if self.laser.timer == 1860:
                screen_shake = 20
                if self.sfx:
                    laser_sound.play().set_volume(0.4)

            self.draw_text(text="Score: "+str(self.score), pos=[20, 20])

            #Collision with OBSTACLES and ROCKS
            if ((self.player.has_collided(self.obstacles.get_objects_rects())[0] or self.player.has_collided(self.rocks.get_objects_rects())[0]) and boost == 0) or self.player.pos[1] > 480 or (self.player.has_collided(self.laser.get_rects())[0] and self.laser.timer > 1800 and self.laser.timer <= 1860 ):
                if not dead:
                    boost = 0
                    self.deactivate_boost()
                    screen_shake = 5
                    dead = True
                    if self.sfx:
                        collision_sound.play().set_volume(0.4)
            
            #Collision with POWERUPS
            #SHIFT
            self.collision = self.player.has_collided(self.shift.get_objects_rects())
            if self.collision[0]:
                self.shift.objects.pop(self.collision[1])
                self.player.glow('#00ff7b')
                self.player.gravity *= -1
                if self.sfx:
                    shift_sound.play().set_volume(0.4)

            if self.player.gravity < 0:
                self.shift.display(self.screen)

            #MAGNET
            self.collision = self.player.has_collided(self.magnet.get_objects_rects())
            if self.collision[0]:
                self.magnet.objects.pop(self.collision[1])
                self.player.glow('#d62828')
                self.player.magnet = 1200
                if self.sfx:
                    powerup_sound.play().set_volume(0.4)

            #2X
            self.collision = self.player.has_collided(self.twox.get_objects_rects())
            if self.collision[0]:
                self.twox.objects.pop(self.collision[1])
                self.player.glow('#d9d9d9')
                twox = 1200
                if self.sfx:
                 powerup_sound.play().set_volume(0.4)

            if twox > 0:
                self.twox.display(self.screen)
                self.draw_text(text=str(twox//60 + 1)+"s", pos=[80, 80])

            #BOOSTER
            self.collision = self.player.has_collided(self.booster.get_objects_rects())
            if self.collision[0]:
                self.booster.objects.pop(self.collision[1])
                self.player.glow('#8a00c4', 600)
                boost = 600
                if self.sfx:
                    boost_sound.play().set_volume(0.4)

            if boost > 0:
                self.booster.display(self.screen)
                self.draw_text(text=str(boost//60 + 1) + "s", pos=[580, 400])
                self.activate_boost()
            else:
                self.deactivate_boost()

            #Collision with ORBS
            if self.player.magnet > 0:
                self.magnet.display(self.screen)
                self.draw_text(text=str(self.player.magnet//60 + 1) + "s", pos=(550, 20))
                self.collision = self.player.has_collided_magnet(self.orbs.get_objects_rects())
            else:
                self.collision = self.player.has_collided(self.orbs.get_objects_rects())
            if self.collision[0]:
                self.orbs.objects.pop(self.collision[1])
                self.score += 100
                self.player.glow('#ffe500', 15) 
                orbs += 1
                if self.sfx:
                    orb_sound.play()
            
            if not pause and not dead:
                self.timer += 1
                twox = max(twox - 1, 0)
                boost = max(boost - 1, 0)
                if self.timer % 12 == 0:
                    if boost > 0:
                        if twox > 0:
                            self.score += 8
                        else:
                            self.score += 5
                    else:
                        if twox > 0:
                            self.score += 3
                        else:
                            self.score += 1

            if dead:
                dead_timer = max(dead_timer - 1, 0)

            if dead_timer == 0:
                self.background.reset()
                self.game_over(orbs=orbs)
                self.reset()
                running = False

            if self.score > 1500 and not dead:
                self.background.white_speed = 2
                self.background.medium_speed = 1.75 
                self.background.dark_speed = 1.5
                self.orbs.speed[0] = 3
                self.obstacles.speed[0] = 3
                self.twox.speed[0] = 3
                self.shift.speed[0] = 3
                self.magnet.speed[0] = 3
                self.booster.speed[0] = 3
                self.rocks.speed[0] = 4
                self.rocks.spawn = [480, 640]
            if self.score > 2000 and not dead:
                self.background.white_speed = 3
                self.background.medium_speed = 2.75 
                self.background.dark_speed = 2.5
                self.orbs.speed[0] = 4
                self.obstacles.speed[0] = 4
                self.twox.speed[0] = 4
                self.shift.speed[0] = 4
                self.magnet.speed[0] = 4
                self.booster.speed[0] = 4
                self.rocks.speed[0] = 5
                self.obstacles.probability = 0.02
                self.rocks.probability = 0.02
                self.laser.probability = 0.0025
                self.orbs.probability = 0.01
                self.score += 1
            if self.score > 3000 and not dead:
                self.background.white_speed = 4
                self.background.medium_speed = 3.75 
                self.background.dark_speed = 3.5
                self.orbs.speed[0] = 5
                self.obstacles.speed[0] = 5
                self.twox.speed[0] = 5
                self.shift.speed[0] = 5
                self.magnet.speed[0] = 5
                self.booster.speed[0] = 5
                self.obstacles.probability = 0.04
                self.rocks.probability = 0.04
                self.laser.probability = 0.05
                self.orbs.probability = 0.02

            pygame.display.update()  # Update the display
            self.clock.tick(60)  # Limit to 60 FPS

    def options(self):
        running = True
        music_button = pygame.Rect(100, 128, 38, 20)
        sfx_button = pygame.Rect(470, 128, 38, 20)
        back_button = pygame.Rect(10, 10, 40, 25)
        reset = pygame.Rect(500, 420, 120, 20)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if music_button.collidepoint((mx, my)):
                            self.music = not self.music
                            data = 1 if self.music else 0
                            save_data('music.txt', str(data))
                            if self.music: pygame.mixer.music.play(-1)
                            else : pygame.mixer.music.stop()
                        if sfx_button.collidepoint((mx, my)):
                            self.sfx = not self.sfx
                            data = 1 if self.sfx else 0
                            save_data('sfx.txt', str(data))
                        if back_button.collidepoint((mx, my)):
                            running = False
                        if reset.collidepoint((mx, my)):
                            reset_files()
                            pygame.quit()
                            sys.exit()


            self.background.render(self.screen)
            self.background.update()

            mx, my = pygame.mouse.get_pos()

            self.screen.blit(self.assets['back'], (10, 10))
            self.draw_text(text='Sounds', size=40, pos=[20, 50], bold=True, colour='#aabbcc', underline=True)
            self.draw_text(text='Music: ', size=20, pos=[20, 125])
            if self.music:self.screen.blit(self.assets['on'], (100, 128))
            else: self.screen.blit(self.assets['off'], (100, 128))
            self.draw_text(text='Sound Effects: ', size=20, pos=[300, 125])
            if self.sfx:self.screen.blit(self.assets['on'], (470, 128))
            else: self.screen.blit(self.assets['off'], (470, 128))

            self.draw_text(text='Controls', size=40, pos=[20, 200], bold=True, colour='#aabbcc', underline=True)
            self.draw_text(text='Dash: ', size=20, pos=[20, 275])
            self.draw_text(text='OR ', size=20, pos=[230, 275])
            self.draw_text(text='Pause: ', size=20, pos=[20, 350])
            self.screen.blit(self.assets['space'], (100, 268))
            self.screen.blit(self.assets['left_click'], (300, 262))
            self.screen.blit(self.assets['escape'], (100, 340))

            if reset.collidepoint((mx, my)):
                pygame.draw.rect(self.screen, '#3e3e3e', reset)
            self.draw_text(text='RESET FILES', size=16, bold=True, underline=True, colour='#ff0000', pos=[500, 420])

            pygame.display.update()
            self.clock.tick(60) 

    def store(self):
        running = True
        back1_button = pygame.Rect(10, 10, 40, 25)
        back2_button = pygame.Rect(10, 220, 40, 25)
        next_button = pygame.Rect(600, 220, 40, 25)
        box1 = pygame.Rect(40, 100, 160, 250)
        box2 = pygame.Rect(240, 100, 160, 250)
        box3 = pygame.Rect(440, 100, 160, 250)
        box4 = pygame.Rect(240, 100, 160, 250)
        buy_box = pygame.Rect(253, 380, 135, 99)
        rejection_sound = pygame.mixer.Sound(self.assets['rejected_sound'])
        kaching_sound = pygame.mixer.Sound(self.assets['kaching_sound'])
        players = load_numbers('store.txt', True)
        page = 1
        to_buy = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        page = 1
                        running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if buy_box.collidepoint((mx, my)) and to_buy:
                            price = (to_buy - 2)*250 + 500
                            if price <= self.coins:
                                kaching_sound.play().set_volume(0.4)
                                self.coins -= price
                                players[to_buy - 1] = 1
                                save_data('coins.txt', str(self.coins))
                                save_numbers('store.txt', players)
                                to_buy = 0
                            else:
                                rejection_sound.play().set_volume(0.4)
                        else:
                            to_buy = 0
                        if back1_button.collidepoint((mx, my)):
                            running = False
                        
                        if page == 1:
                            if next_button.collidepoint((mx, my)):
                                page = 2

                            if box1.collidepoint((mx, my)):
                                self.player_selected = 1
                                save_data('player.txt', str(self.player_selected))
                            if box2.collidepoint((mx, my)):
                                if players[1]:
                                    self.player_selected = 2
                                    save_data('player.txt', str(self.player_selected))
                                else:
                                    to_buy = 2
                            if box3.collidepoint((mx, my)):
                                if players[2]:
                                    self.player_selected = 3
                                    save_data('player.txt', str(self.player_selected))
                                else:
                                    to_buy = 3
                            
                        if page == 2:
                            if back2_button.collidepoint((mx, my)) and page == 2:
                                page = 1

                            if box4.collidepoint((mx, my)):
                                if players[3]:
                                    self.player_selected = 4
                                    save_data('player.txt', str(self.player_selected))
                                else:
                                    to_buy = 4
            

            mx, my = pygame.mouse.get_pos()

            self.background.render(self.screen)
            self.screen.blit(self.assets['back'], (10, 10))
            self.draw_text(size=40, text='Store', underline=True, colour='#aabbcc', bold=True, pos=[250, 10])
            self.screen.blit(self.assets['coin'], (500, 20))
            self.draw_text(text=str(self.coins), bold=True, size=16, pos=[540, 25])

            if page == 1:
                self.screen.blit(self.assets['next'], (600, 220))
                for i in range(3):
                    self.draw_player_card(i+1, players[i], (i - 1)*250+500, [i*160 + 40 + i*40, 100])
            elif page == 2:
                self.screen.blit(self.assets['back'], (10, 220))
                self.draw_player_card(4, players[3], 1000, [240, 100])


            if to_buy:
                self.screen.blit(self.assets['buy'], (253, 380))
                self.screen.blit(self.assets['coin'], (275, 445))
                self.draw_text(text=str((to_buy - 2)*250 + 500), size=20, colour='black', pos=[310, 447], bold=True)

            self.background.update()

            pygame.display.update()
            self.clock.tick(60)

    def draw_player_card(self, id, bought, price, pos=[0, 0]):
        
        frame = pygame.Rect(pos[0], pos[1], 160, 250)
        selection = pygame.Rect(pos[0], pos[1] + 200, 160, 50)
        pygame.draw.rect(self.screen, '#222266', frame)
        names = {
            1: "Neon Triangle",
            2: "Goofy Circle",
            3: "Crossy X",
            4: "Mr Tomato"
        }
        self.draw_text(text=names[id], size=20, pos=[pos[0] + 10, 110])
        self.screen.blit(self.assets['player'+str(id)], (pos[0] + 60, 200))

        if self.player_selected == id:
            pygame.draw.rect(self.screen, 'green', selection)
            self.draw_text(text='Selected', pos=[pos[0] + 30, 310], size=20, bold=True, colour='black')
        else:
            pygame.draw.rect(self.screen, 'grey', selection)
            if bought:
                self.draw_text(text='Owned', pos=[pos[0] + 30, 310], size=20, bold=True, colour='black')
            else:
                self.screen.blit(self.assets['coin'], (pos[0] + 30, 310))
                self.draw_text(text=str(price), size=20, bold=True, colour='black', pos=[pos[0] + 60, 312])
            


if __name__ == "__main__":
    Game().main_menu()
