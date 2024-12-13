import pygame
from player import Player
from enemy import Enemy
from piece import Piece
from heart import Heart
from constants import SCREEN_WIDTH
import time


class Game:
    def __init__(self):
        # Fenêtre de jeu
        self.screen_width = pygame.display.Info().current_w  # Largeur de l'écran
        self.screen_height = pygame.display.Info().current_h  # Hauteur de l'écran
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        # ecrire les dimention de la fenetre dans le terminal
        
        pygame.display.set_caption("Jeu avec saut, double saut et dash")
        self.floor = 720
        # Charger l'image de fond
        self.background = pygame.image.load("assets/images/map.png")
        self.plateformimg = pygame.image.load("assets/images/mapvierge.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.screen_width, 1400))
        self.plateformimg = pygame.transform.scale(self.plateformimg, (self.screen_width, self.screen_height))
        # decaler l'image de fond
        self.x_offset = 0
        self.y_offset = -250
        self.screen.blit(self.background, (self.x_offset, self.y_offset))
        
        # mettre des collision sur les plateformes de la map
        self.plateformes = [
            pygame.Rect(0, 640, 340, 50),  # (x, y, largeur, hauteur)
            pygame.Rect(290, 482, 300, 45), #
            pygame.Rect(690, 335, 120, 40), #
            pygame.Rect(380, 780, 180, 50), #
            pygame.Rect(155, 140, 270, 40), #
            pygame.Rect(380, 258, 315, 45), #
            pygame.Rect(845, 255, 170, 45), #
            pygame.Rect(735, 540, 230, 45), #
            pygame.Rect(1100, 580, 210, 45), #
            pygame.Rect(1275, 710, 160, 45), #
            pygame.Rect(1070, 360, 250, 45), #
            pygame.Rect(1338, 55, 150, 45), #


            
        ]
        
        self.life_image = pygame.image.load("assets/images/vie.png")
        self.life_image = pygame.transform.scale(self.life_image, (40, 40))  # Taille de l'icône des vies

        # Créer une instance du joueur
        self.player = Player(50, 330)
        self.enemy = Enemy(400, 200)
        self.enemies = [self.enemy]

        # Créer une liste de pièces
        self.pieces = []
        self.last_piece_spawn_time = 0  # Temps depuis la dernière pièce
        self.piece_spawn_interval = 2000  # Intervalle de génération des pièces (en ms)
        
        # créer une liste de hearts
        self.hearts = []
        self.last_heart_spawn_time = 0  # Temps depuis le dernier heart
        self.heart_spawn_interval = 60000  # Intervalle de génération des hearts toute les minutes
        

        # Initialiser le temps
        self.start_time = time.time()

        # initialiser les vies
        self.lives = 3
        self.immortality = False
        self.immortality_start_time = 0
        self.score = 0
        self.best_score = 0  # Meilleur score initialisé
        self.load_best_score()  # Charger le meilleur score sauvegardé
        self.alive = True  # Initialiser alive à True
        self.started = True
        self.clock = pygame.time.Clock()  # Pour contrôler la vitesse de la boucle
        
        
    def load_best_score(self):
        """Charge le meilleur score depuis un fichier."""
        try:
            with open("best_score.txt", "r") as file:
                self.best_score = int(file.read())
        except FileNotFoundError:
            self.best_score = 0  # Aucun fichier trouvé, initialise à 0
        except ValueError:
            self.best_score = 0  # Fichier corrompu, initialise à 0

    def save_best_score(self):
        """Sauvegarde le meilleur score dans un fichier."""
        with open("best_score.txt", "w") as file:
            file.write(str(self.best_score))
    def restart_game(self):
            # Réinitialiser toutes les variables du jeu
            self.player = Player(50, 330)  # Réinitialiser la position du joueur
            self.enemy = Enemy(500, 200)  # Réinitialiser la position de l'ennemi
            self.pieces = []  # Réinitialiser les pièces
            self.last_piece_spawn_time = pygame.time.get_ticks() # Réinitialiser le timer des pièces
            
            self.start_time = time.time()  # Réinitialiser le timer du jeu
            self.score = 0  # Réinitialiser le score
            self.alive = True  # Réinitialiser l'état du joueur
            self.started = True  # S'assurer que la boucle principale redémarre
            self.enemies = [self.enemy]  # Réinitialiser les ennemis
            self.lives = 3  # Réinitialiser les vies
            self.hearts.clear()
            self.last_heart_spawn_time = pygame.time.get_ticks()  # Temps depuis le dernier heart
            self.immortality = False
    def draw_lives(self):
        """Affiche les icônes de vie en bas à gauche."""
        for i in range(self.lives):
            x = 10 + i * 45  # Espacement entre les vies
            y = self.screen.get_height() - 50  # Position en bas
            if self.life_image:  # Vérifier si l'image est bien chargée
                self.screen.blit(self.life_image, (x, y))
            else:
                print("Image des vies non chargée")

    def check_collision(self):
    
        for enemy in self.enemies:  # Parcours tous les ennemis
            if self.player.rect.colliderect(enemy.rect) and not self.immortality:
                self.lives -= 1
                self.immortality = True  # Activer l'immortalité
                self.immortality_start_time = pygame.time.get_ticks()
                print(f"Vies restantes: {self.lives}")
                if self.lives == 0:
                    self.alive = False  # Le joueur est mort
                    self.animate_death()  # Animer la mort
                break  # Arrêter la vérification après une collision

    def update_immortality(self):
        if self.immortality and pygame.time.get_ticks() - self.immortality_start_time > 1500:  # 2 secondes
            self.immortality = False
            print("Immortalité désactivée")
    def lose_lives(self):
        # Faire clignoter le joueur et le rendre sombre
        elapsed_time = pygame.time.get_ticks() - self.immortality_start_time

        if elapsed_time % 400 < 200:  # Clignote toutes les 200ms
            # Afficher le joueur normalement
            self.screen.blit(self.player.image, self.player.rect)
        else:
            # Rendre le joueur sombre
            dark_image = self.player.image.copy()
            dark_image.fill((50, 50, 50), special_flags=pygame.BLEND_RGB_MULT)  # Assombrit l'image
            self.screen.blit(dark_image, self.player.rect)
    def animate_death(self):
        # Animation de chute
        fall_speed = 16  # Vitesse de la chute
        while self.player.rect.bottom < self.screen.get_height():
            # Afficher le fond redimensionné avec offsets
            background_resized = pygame.transform.scale(self.background, (self.screen_width, 1400))
            self.screen.blit(background_resized, (self.x_offset, self.y_offset))

            # Créer une superposition semi-transparente
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))  # Noir avec transparence (alpha = 100)
            self.screen.blit(overlay, (0, 0))  # Afficher l'overlay

            # Déplacer le joueur vers le bas pour l'animation de chute
            self.player.rect.y += fall_speed

            # Afficher l'image du joueur
            self.screen.blit(self.player.image, self.player.rect)

            # Afficher l'image de l'ennemi
            self.screen.blit(self.enemy.image, self.enemy.rect)

            # Mettre à jour l'écran
            pygame.display.flip()

            # Gérer les événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.clock.tick(60)

        # Une fois le joueur tombé, afficher un écran noir pendant 2 secondes
        self.show_game_over()



    def show_game_over(self):
        # Mettre à jour le meilleur score si le score actuel est plus élevé
        if self.score > self.best_score:
            self.best_score = self.score
            self.save_best_score()

        # Affichage de l'écran de fin
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Noir avec transparence (alpha = 150)

        font = pygame.font.Font(None, 48)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        restart_text = font.render("Appuyez sur R pour recommencer", True, (255, 255, 255))
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        best_score_text = font.render(f"Best Score: {self.best_score}", True, (255, 255, 0))  # Meilleur score

        # Redimensionner l'image de fond pour qu'elle couvre toute la hauteur souhaitée
        background_resized = pygame.transform.scale(self.background, (self.screen_width, 1400))

        # Décaler l'image avec les offsets définis
        self.screen.blit(background_resized, (self.x_offset, self.y_offset))

        # Affichage de l'overlay et des textes
        self.screen.blit(overlay, (0, 0))  # Overlay
        self.screen.blit(game_over_text, (self.screen.get_width() // 2 - game_over_text.get_width() // 2, 200))
        self.screen.blit(restart_text, (self.screen.get_width() // 2 - restart_text.get_width() // 2, 300))
        self.screen.blit(score_text, (self.screen.get_width() // 2 - score_text.get_width() // 2, 400))
        self.screen.blit(best_score_text, (self.screen.get_width() // 2 - best_score_text.get_width() // 2, 450))
        
        pygame.display.flip()

        # Attendre que l'utilisateur appuie sur 'R' pour recommencer
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Recommencer le jeu
                        self.restart_game()
                        waiting_for_input = False
    def fall_death(self):
        if self.player.rect.y > self.screen.get_height() + 220:
            self.alive = False
            self.animate_death()
    def run(self):
        while self.started:
            if not self.alive:
                return  # Si le joueur est mort, sortir de la boucle

            # Afficher l'image du joueur
            self.screen.blit(self.background, (self.x_offset, self.y_offset))
            self.screen.blit(self.plateformimg, (0, 0))
            
                # Dessiner les plateformes
            self.player.update(self.plateformes)
            
            for plateforme in self.plateformes:
                # Dessine la plateforme avec un décalage de 5 pixels vers le bas
                plateforme_visuelle = pygame.Rect(
                    plateforme.x, 
                    plateforme.y + 5,  # Décalage de 5 pixels vers le bas
                    plateforme.width, 
                    plateforme.height
                )
                # ------------- ici ------------------
                #pygame.draw.rect(self.screen, (255, 255, 255), plateforme_visuelle)
        
            if not self.pieces and pygame.time.get_ticks() - self.last_piece_spawn_time > self.piece_spawn_interval:
                x, y = Piece.generate_random_position(self.screen.get_width(), self.screen.get_height(), self.floor)
                new_piece = Piece(x, y)
                self.pieces.append(new_piece)  # Ajouter la pièce à la liste
                self.last_piece_spawn_time = pygame.time.get_ticks()  # Réinitialiser le timer
            
            for piece in self.pieces[:]:
                piece.update()
                self.screen.blit(piece.image, piece.rect)
                if self.player.rect.colliderect(piece.rect):  # Collision avec une pièce
                    self.pieces.remove(piece)
                    self.score += 1
                    
                    
            if  pygame.time.get_ticks() - self.last_heart_spawn_time > self.heart_spawn_interval:
                x, y = Heart.generate_random_position(self.screen.get_width(), self.screen.get_height(), self.floor)
                new_heart = Heart(x, y)
                self.hearts.append(new_heart)
                print(self.last_heart_spawn_time)
                self.last_heart_spawn_time = pygame.time.get_ticks()
                
            for heart in self.hearts[:]:
                heart.update()
                self.screen.blit(heart.image, heart.rect)
                if self.player.rect.colliderect(heart.rect):
                    self.hearts.remove(heart)
                    self.lives += 1
                    
            self.player.draw(self.screen)
            self.enemy.draw(self.screen)
            self.fall_death()
            self.player.collide_with_walls(self.screen.get_width())

            for enemy in self.enemies:
                enemy.draw(self.screen)  # Dessiner l'ennemi
                enemy.move_randomly()    # Déplacer l'ennemi de manière aléatoire (si tu veux ce comportement)

            # Afficher l'image de l'ennemi
            self.check_collision()
            self.update_immortality()
            if self.immortality:
                self.lose_lives()  # Faire clignoter le joueur
            else:
                self.screen.blit(self.player.image, self.player.rect)
            # Mettre à jour l'affichage
            font = pygame.font.Font(None, 70)
            # Texte en noir (contour)
            outline_text = font.render(f"Score: {self.score}", True, (0, 0, 0))
            for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # 4 directions autour du texte principal
                self.screen.blit(outline_text, (720 + offset[0], 10 + offset[1]))

            # Texte principal (couleur verte)
            score_text = font.render(f"Score: {self.score}", True, (100, 255, 0))

            self.screen.blit(score_text, (720 , 10))

            self.draw_lives()
            pygame.display.flip()

            # Gérer les événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Fermeture du jeu")
                    self.started = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:  # Saut
                        self.player.jump()
                    if event.key == pygame.K_LSHIFT:  # Dash
                        self.player.dash()

            # Gérer les touches maintenues
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q] or keys[pygame.K_LEFT]:  # Déplacement vers la gauche
                self.player.move_left()
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # Déplacement vers la droite
                self.player.move_right()
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.player.move_down()
            # keys = pygame.key.get_pressed()
            # self.player.update_speed(keys)

            current_time = pygame.time.get_ticks()  # Temps actuel


                    
        
            
            

            # Afficher et gérer les pièces

            #ajouter des enemy
            if self.score % 5 == 0 and (self.score // 5) >= len(self.enemies):
                # faire apparaitre l'enemy a l'oposer de player
                if self.player.rect.x < SCREEN_WIDTH / 2:
                    x = 1400
                    y = 400
                else:
                    x = 50
                    y = 400

                
                
                # Vérifie que l'ennemi n'apparaît pas sur le joueur
                if not self.player.rect.colliderect(pygame.Rect(x, y, 50, 50)):
                    new_enemy = Enemy(x, y)
                    self.enemies.append(new_enemy)
                
                
            self.clock.tick(60)

