import pygame
import arcade

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("My Game")

pygame.mixer.music.load("music.mp3")
collision_sound = pygame.mixer.Sound("explosion1.wav")
player_image = pygame.image.load("vamp.png").convert_alpha()
item_image = pygame.image.load("coinGold.png").convert_alpha()
thorn_image = pygame.image.load("spikes.png").convert_alpha()
particle_image = pygame.image.load("star.png").convert_alpha()
background_image = pygame.image.load("abstract_1.jpg").convert()

player_x = 50
player_y = 50
player_speed = 5
item_x = 500
item_y = 500
thorn_x = 300
thorn_y = 300
particles = []
score = 0


def draw_particles():
    for particle in particles:
        screen.blit(particle_image, (particle[0], particle[1]))


def update_particles():
    for particle in particles:
        particle[0] += particle[2]
        particle[1] += particle[3]
        particle[4] -= 1
        if particle[4] == 0:
            particles.remove(particle)


def check_collision():
    global score
    player_rect = pygame.Rect(player_x, player_y, player_image.get_width(), player_image.get_height())
    item_rect = pygame.Rect(item_x, item_y, item_image.get_width(), item_image.get_height())
    if player_rect.colliderect(item_rect):
        particles.append([item_x, item_y, 0, -5, 30])
        score += 10
        item_x = 1000
        item_y = 1000
    thorn_rect = pygame.Rect(thorn_x, thorn_y, thorn_image.get_width(), thorn_image.get_height())
    if player_rect.colliderect(thorn_rect):
        particles.append([player_x, player_y, -5, -5, 10])
        particles.append([player_x, player_y, 0, -5, 10])
        particles.append([player_x, player_y, 5, -5, 10])
        particles.append([player_x, player_y, -5, 0, 10])
        particles.append([player_x, player_y, 5, 0, 10])
        particles.append([player_x, player_y, -5, 5, 10])
        particles.append([player_x, player_y, 0, 5, 10])
        particles.append([player_x, player_y, 5, 5, 10])
        score -= 5


def draw():
    screen.blit(background_image, (0, 0))
    screen.blit(player_image, (player_x, player_y))
    screen.blit(item_image, (item_x, item_y))
    screen.blit(thorn_image, (thorn_x, thorn_y))
    font = pygame.font.SysFont(None, 50)
    text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(text, (10, 10))
    draw_particles()

def update():
    global player_x, player_y, item_x, item_y
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_image.get_width():
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < screen_height - player_image.get_height():
        player_y += player_speed
    check_collision()
    update_particles()

def start_game():
    pygame.mixer.music.play(-1)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        update()
        draw()
        pygame.display.update()
    pygame.mixer.music.stop()

def settings():
    pass

def exit_game():
    pygame.quit()
    exit()

def draw_menu():
    screen.blit(background_image, (0, 0))
    font = pygame.font.SysFont(None, 100)
    text = font.render("MY GAME", True, (255, 255, 255))
    screen.blit(text, (200, 100))
    font = pygame.font.SysFont(None, 50)
    text = font.render("START", True, (255, 255, 255))
    screen.blit(text, (350, 250))
    text = font.render("SETTINGS", True, (255, 255, 255))
    screen.blit(text, (330, 350))
    text = font.render("EXIT", True, (255, 255, 255))
    screen.blit(text, (380, 450))

def start_menu():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_RETURN:
                    if cursor_rect.colliderect(start_rect):
                        start_game()
                    elif cursor_rect.colliderect(settings_rect):
                        settings()
                    elif cursor_rect.colliderect(exit_rect):
                        exit_game()
        screen.blit(background_image, (0, 0))
        draw_menu()
        cursor_rect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)
        start_rect = pygame.Rect(350, 250, 100, 50)
        settings_rect = pygame.Rect(330, 350, 150, 50)
        exit_rect = pygame.Rect(380, 450, 100, 50)
        pygame.draw.rect(screen, (255, 255, 255), start_rect, 2)
        pygame.draw.rect(screen, (255, 255, 255), settings_rect, 2)
        pygame.draw.rect(screen, (255, 255, 255), exit_rect, 2)
        if cursor_rect.colliderect(start_rect):
            pygame.draw.rect(screen, (255, 255, 255), start_rect, 5)
        elif cursor_rect.colliderect(settings_rect):
            pygame.draw.rect(screen, (255, 255, 255), settings_rect, 5)
        elif cursor_rect.colliderect(exit_rect):
            pygame.draw.rect(screen, (255, 255, 255), exit_rect, 5)
        pygame.display.update()

start_menu()

pygame.quit()
exit()