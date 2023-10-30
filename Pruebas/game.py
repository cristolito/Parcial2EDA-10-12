import pygame
import sys
from car import Car
import random
class Game:
    def __init__(self):
        pygame.init()

        # Configuración de la pantalla
        self.WIDTH, self.HEIGHT = 736, 420
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Juego de Colores")
        self.background = pygame.image.load("Background.jpg")

        # Configuración de los coches
        self.car_width = 135
        self.MIN_DISTANCE = 30  # Ajusta esta constante según tu preferencia
        self.car_height = 30
        self.max_cars = 5  # Máximo número de coches permitidos antes del game over
        self.cars = []
        self.car_speed = 5
        self.speed_increase_interval = 8000  # Aumentar la velocidad cada 5 segundos (en milisegundos)
        self.speed_increase_amount = 1  # Aumentar la velocidad en 2 unidades
        self.last_speed_increase_time = pygame.time.get_ticks()

        # Configuración de la paleta
        self.colors = ["blue", "green", "pink"]
        self.palette_colors = [(0, 0, 255), (0, 255, 0), (255, 182, 193)]
        self.palette_width = 160
        self.palette_height = 60
        self.palette_x = (self.WIDTH - self.palette_width) // 2
        self.palette_y = 20
        self.palette_rects = [pygame.Rect(self.palette_x + i * (self.palette_width // len(self.colors)), self.palette_y,
                                          self.palette_width // len(self.colors), self.palette_height)
                              for i in range(len(self.colors))]

        # Reloj para controlar la velocidad del juego
        self.clock = pygame.time.Clock()

        # Cargar imágenes
        self.white_image = pygame.image.load("CarWhite.png").convert_alpha()
        self.blue_image = pygame.image.load("CarBlue.png").convert_alpha()
        self.green_image = pygame.image.load("CarGreen.png").convert_alpha()
        self.pink_image = pygame.image.load("CarPink.png").convert_alpha()

        # Game over
        self.game_over = False

        # start screen
        self.in_start_screen = True

    def show_start_screen(self):
        font = pygame.font.Font("Pixeltype.ttf", 74)
        start_text = font.render("Press SPACE to Start", True, (0, 0, 255))
        start_rect = start_text.get_rect(center=(self.WIDTH / 2, self.HEIGHT / 2))

        self.screen.fill((255, 255, 255))
        self.screen.blit(start_text, start_rect)
        pygame.display.flip()

        waiting_for_start = True
        while waiting_for_start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting_for_start = False
            self.clock.tick(60)

    def draw_palette(self):
        for i, rect in enumerate(self.palette_rects):
            pygame.draw.rect(self.screen, self.palette_colors[i], rect)
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)  # Dibujar bordes negros alrededor de los bloques

    def draw_cars(self):
        for car in self.cars:
            car.text_rect.center = car.rect.center
            self.screen.blit(car.image, car.rect)
            self.screen.blit(car.text, car.text_rect)

    def create_random_color_text(self):
        # Selecciona un color aleatorio entre azul, verde y rosado
        random_color = random.choice(self.colors)
        text = pygame.font.Font("Pixeltype.ttf", 36).render(random_color.capitalize(), True, self.palette_colors[self.colors.index(random_color)])
        return text, text.get_rect(), random_color

    def reset(self):
        self.cars = []
        self.car_speed = 3
        self.game_over = False
        Car.car_stopped = 0

    def move_cars(self):
        for i, car in enumerate(self.cars):
            if not car.stopped:
                car.rect.move_ip(-self.car_speed, 0)

                # Verificar si el coche actual está lo suficientemente cerca del coche de adelante
                if not car.correct and i > 0 and car.rect.colliderect(self.cars[i - 1].rect.inflate(-self.MIN_DISTANCE, 0)):
                    car.stop()
                    self.spawn_cars()
                    self.check_game_over()
                    if self.game_over:
                        self.show_game_over_screen()
                        return
                    
                if self.cars and (self.cars[-1].rect.left + 50) <= self.car_speed:
                    self.cars.pop(-1)
                    self.spawn_cars()
                    Car.car_stopped -= 1
        
        # Verificar si algún coche ha alcanzado el final
        if not car.correct and self.cars and self.cars[-1].rect.left <= self.car_speed:  # Ajuste aquí para evitar traspasar el borde
            for i, car in enumerate(self.cars):
                car.rect.left = i * (self.car_width * 2 + 20)  # Colocar los coches en una cola

            self.cars[-1].stop()
            self.spawn_cars()

        if self.cars and (self.cars[-1].rect.left + 50) <= self.car_speed:
            self.cars.pop(-1)
            Car.car_stopped -= 1

    def spawn_cars(self):
        text_surface, text_rect, random_color = self.create_random_color_text()
        new_car = Car(self.WIDTH, 300, self.car_width, self.car_height, self.white_image, text_surface, text_rect, random_color)
        self.cars.append(new_car)

    def check_game_over(self):
        if Car.get_car_stopped() == 5:
            self.game_over = True

    def increase_speed(self):
        self.car_speed += self.speed_increase_amount / 1000

    def show_game_over_screen(self):
        font = pygame.font.Font("Pixeltype.ttf", 74)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(self.WIDTH / 2, self.HEIGHT / 2))

        play_again_text = font.render("Press R to Play Again", True, (0, 0, 255))
        play_again_rect = play_again_text.get_rect(center=(self.WIDTH / 2, self.HEIGHT / 2 + 100))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.reset()
                    return  # Salir del bucle y continuar el juego si se presiona 'R'

            self.screen.fill((255, 255, 255))
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(play_again_text, play_again_rect)
            pygame.display.flip()
            self.clock.tick(60)

    def run(self):
        selected_color = None  # Variable para almacenar el color seleccionado en la paleta
        self.spawn_cars()

        while not self.game_over:
            if self.in_start_screen:
                self.show_start_screen()
                self.in_start_screen = False
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Botón izquierdo del ratón
                        for i, rect in enumerate(self.palette_rects):
                            if rect.collidepoint(event.pos):
                                selected_color = self.colors[i]


                        # Cambiar color del último coche si hay un color seleccionado
                        if selected_color is not None and self.cars:
                            self.cars[-1].change_color(selected_color)
                            selected_color = None  # Restablecer la variable después de cambiar el color
            self.screen.blit(self.background, (0, 0))

            self.draw_palette()
            self.move_cars()

            if not self.cars:
                self.spawn_cars()

            self.draw_cars()
            
            # Verificar si algún coche ha alcanzado el final
            if self.cars[-1].rect.left <= -self.car_width:
                self.spawn_cars()

            self.increase_speed()

            pygame.display.flip()
            self.clock.tick(60)  # Ajustar el valor para aumentar o disminuir la velocidad
