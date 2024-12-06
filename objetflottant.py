import pygame
import random


class Objetflottant(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Variables pour le flottement
        self.direction = 1  # 1 = descend, -1 = monte
        self.last_change_time = pygame.time.get_ticks()  # Temps du dernier changement
        self.flottement_interval = 300  # Intervalle en millisecondes pour changer la direction
        self.flottement_amplitude = 1  # Distance du flottement (en pixels)

    @staticmethod
    def generate_random_position(screen_width, screen_height, floor_height):
        """
        Génère une position aléatoire pour la pièce dans la zone jouable.
        """
        x = random.randint(50, screen_width - 50)  # Assure que la pièce reste à l'intérieur de l'écran
        y = random.randint(30, floor_height - 30)  # Limite la hauteur pour ne pas dépasser le sol
        return x, y

    def update(self):
        # Temps actuel
        current_time = pygame.time.get_ticks()

        # Change de direction toutes les flottement_interval millisecondes
        if current_time - self.last_change_time > self.flottement_interval:
            self.direction *= -1  # Inverse la direction
            self.last_change_time = current_time  # Réinitialise le temps

        # Déplace la pièce dans la direction actuelle
        self.rect.y += self.direction * self.flottement_amplitude
