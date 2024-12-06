import pygame

class Menu:
    def __init__(self, screen, font_path=None):
        self.screen = screen
        self.running = True  # Indique si le menu est actif
        self.title_font = pygame.font.Font(font_path, 50) if font_path else pygame.font.SysFont("Arial", 50)
        self.option_font = pygame.font.Font(font_path, 30) if font_path else pygame.font.SysFont("Arial", 30)
        self.options = ["Start Game", "Quit"]
        self.selected_option = 0  # Option sélectionnée

    def draw(self):
        # Remplir l'écran avec une couleur de fond
        self.screen.fill((0, 0, 0))

        # Afficher le titre
        title_text = self.title_font.render("Main Menu", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title_text, title_rect)

        # Afficher les options
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            option_text = self.option_font.render(option, True, color)
            option_rect = option_text.get_rect(center=(self.screen.get_width() // 2, 200 + i * 50))
            self.screen.blit(option_text, option_rect)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:  # Entrée ou Espace
                    if self.selected_option == 0:  # Start Game
                        return "start_game"
                    elif self.selected_option == 1:  # Quit
                        self.running = False

        return None

    def run(self):
        while self.running:
            action = self.handle_input()
            if action == "start_game":
                return "start_game"
            self.draw()
            pygame.display.flip()
