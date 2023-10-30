import pygame

class Car:
    car_stopped = 0
    def __init__(self, x, y, width, height, image, text, text_rect, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image
        self.stopped = False
        self.text = text
        self.text_rect = text_rect
        self.color = color
        self.correct = False

    def change_color(self, selected_color):
        if selected_color == self.color:
            self.image = pygame.image.load(f"Car{selected_color.capitalize()}.png").convert_alpha()
            self.correct = True

    def stop(self):
        self.stopped = True
        Car.car_stopped += 1

    @classmethod
    def get_car_stopped(cls):
        # Método de clase para obtener el valor del contador
        return cls.car_stopped