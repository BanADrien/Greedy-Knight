import pygame
import random
import time
from constants import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path="assets/images/enemy.png"):
        super().__init__()

        # Charger et redimensionner l'image de l'ennemi
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (90, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Variables pour le mouvement progressif
        self.move_x = 0
        self.move_y = 0
        self.last_move_time = time.time()
        self.move_duration = 0.4  # Changer la direction toutes les 0.4 secondes

    def move_randomly(self):
        """Déplace l'ennemi aléatoirement avec des limites imposées"""
        current_time = time.time()

        # Changer de direction après un intervalle
        if current_time - self.last_move_time > self.move_duration:
            self.move_x = random.randint(-5, 5)  # Nouvelle vitesse aléatoire sur X
            self.move_y = random.randint(-5, 5)  # Nouvelle vitesse aléatoire sur Y
            self.last_move_time = current_time

        # Appliquer le mouvement
        self.rect.x += self.move_x
        self.rect.y += self.move_y

        # Empêcher l'ennemi de dépasser les bords
        if self.rect.x < 0:
            self.rect.x = 0
            self.move_x *= -1  # Inverser le déplacement en X
        if self.rect.x > SCREEN_WIDTH - self.rect.width - 50:
            self.rect.x = SCREEN_WIDTH - self.rect.width - 50
            self.move_x *= -1

        if self.rect.y < 70:  # Limite supérieure
            self.rect.y = 70
            self.move_y *= -1
        if self.rect.y > SCREEN_HEIGHT - self.rect.height:  # Limite inférieure
            self.rect.y = SCREEN_HEIGHT - self.rect.height
            self.move_y *= -1

    def draw(self, screen):
        """Dessiner l'ennemi sur l'écran"""
        screen.blit(self.image, self.rect)
        # Debug : Afficher la hitbox (commenter pour désactiver)
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
