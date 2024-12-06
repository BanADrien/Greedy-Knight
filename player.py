import pygame
from constants import SCREEN_WIDTH

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path="assets/images/player.webp"):
        super().__init__()


        # Charger l'image du joueur
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (40, 90))  # Redimensionner l'image
        self.rect = pygame.Rect(x, y, 40, 80)  # Hitbox du joueur avec position x et y et taille largeur et hauteur

        # Physique
        self.player_pos_y_change = 0
        self.is_jumping = False
        self.jumps_left = 2  # Nombre de sauts (double saut inclus)
        self.gravity = 1.2  # Gravité
        self.jump_speed = -22  # Vitesse du saut

        # Dash
        self.is_dashing = False
        self.dash_time = 0
        self.dash_duration = 160  # Durée du dash en millisecondes
        self.dash_speed = 26  # Vitesse du dash
        self.left_dash = 1  # Nombre de dashs disponibles
        self.fall = False
        self.side = 1  # 0 pour face à droite, 1 pour face à gauche
        self.fall_timer = 0  # Timer pour la chute
        
        # Vélocité
        self.max_speed = 10  # Vitesse maximale
        self.acceleration = 0.4  # Accélération
        self.deceleration = 0.4  # Décélération douce
        self.current_speed = 0  # Vitesse actuelle
    

    def move_left(self):
        # Vérifie si le joueur est dans les limites de l'écran
        if self.rect.x > 0:  # Évite de sortir du bord gauche
            # Réinitialise la vitesse si le joueur change de direction
            if self.side == 0:  # Si le joueur faisait face à droite
                self.current_speed = 0
            
            # Applique l'accélération pour atteindre la vitesse maximale à gauche
            if self.current_speed > -self.max_speed:
                self.current_speed -= self.acceleration
            
            # Déplace le joueur à gauche
            self.rect.x += self.current_speed

            # Inverse l'image si le joueur change de direction
            if self.side == 0:  # Si le joueur faisait face à droite
                self.image = pygame.transform.flip(self.image, True, False)
                self.side = 1  # Met à jour la direction


    def move_right(self):
        # Vérifie si le joueur est dans les limites de l'écran
        if self.rect.x < SCREEN_WIDTH - self.rect.width:  # Évite de sortir du bord droit
            # Réinitialise la vitesse si le joueur change de direction
            if self.side == 1:  # Si le joueur faisait face à gauche
                self.current_speed = 0
            
            # Applique l'accélération pour atteindre la vitesse maximale à droite
            if self.current_speed < self.max_speed:
                self.current_speed += self.acceleration
            
            # Déplace le joueur à droite
            self.rect.x += self.current_speed

            # Inverse l'image si le joueur change de direction
            if self.side == 1:  # Si le joueur faisait face à gauche
                self.image = pygame.transform.flip(self.image, True, False)
                self.side = 0  # Met à jour la direction

    def update_speed(self, keys):
        # Si aucune touche gauche ou droite n'est pressée
        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_q] and not keys[pygame.K_d]:
            # Appliquer une décélération progressive
            if self.current_speed > 0:
                self.current_speed -= self.deceleration
            elif self.current_speed < 0:
                self.current_speed += self.deceleration

            # Arrêter complètement si la vitesse devient négligeable
            if abs(self.current_speed) < self.deceleration:
                self.current_speed = 0

    def move_down(self):
        self.fall = True
        self.fall_timer = pygame.time.get_ticks()  # Démarrer le timer pour la chute

    def jump(self):
        if self.jumps_left > 0:  # Saut seulement si des sauts sont disponibles
            self.is_jumping = True
            self.player_pos_y_change = self.jump_speed
            self.jumps_left -= 1  # Réduction du nombre de sauts

    def dash(self):
        if self.left_dash > 0:  # Dash seulement si disponible
            if not self.is_dashing:
                self.is_dashing = True
                self.dash_time = pygame.time.get_ticks()
                self.left_dash -= 1

    def update(self, plateformes):
        # Appliquer la gravité
        self.rect.y += self.player_pos_y_change 
        self.player_pos_y_change += self.gravity
        keys = pygame.key.get_pressed()
        if not (keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]) and not keys[pygame.K_q] and not keys[pygame.K_d]:
            self.update_speed(keys)  
        # Réduire l'accélération de chute
        if self.player_pos_y_change > 20:
            self.player_pos_y_change = 15
        
        # Gérer les collisions avec les plateformes
        self.handle_platform_collision(plateformes)
        self.actual_time = pygame.time.get_ticks()
            # si on tombe depuis 0.5 sec fall deviens false
        if self.fall and self.actual_time - self.fall_timer > 115:
            self.fall = False
        # Gérer le dash
        if self.is_dashing:
            current_time = pygame.time.get_ticks()
            if self.side == 0:  # Dash vers la droite
                self.rect.x += self.dash_speed
            else:  # Dash vers la gauche
                self.rect.x -= self.dash_speed

            if current_time - self.dash_time > self.dash_duration:
                self.is_dashing = False

        # Empêcher de dépasser les limites de l'écran
        self.collide_with_walls(SCREEN_WIDTH)

    def handle_platform_collision(self, plateformes):
        # Vérifie les collisions avec les plateformes
        if not self.fall:
            for plateforme in plateformes:
                if self.rect.colliderect(plateforme):
                    # Collision par le dessus
                    if self.player_pos_y_change >= 0 and self.rect.bottom > plateforme.top and self.rect.bottom <= plateforme.top + 40:
                        self.rect.bottom = plateforme.top
                        self.player_pos_y_change = 0
                        self.jumps_left = 2  # Réinitialiser les sauts
                        self.left_dash = 1  # Réinitialiser le dash
                        self.fall_timer = pygame.time.get_ticks()  # Réinitialiser le timer de la chute
                        

    def collide_with_walls(self, screen_width):
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > screen_width - 40:  # Limite droite
            self.rect.x = screen_width - 40

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        # Dessiner la hitbox (facultatif pour debug)
        #pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
