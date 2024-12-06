from objetflottant import Objetflottant
class Heart(Objetflottant):
    def __init__(self, x, y, image_path="assets/images/vie.png"):
        super().__init__(x, y, image_path) # Taille de l'objet
        # Autres initialisations spécifiques au Coeur si besoin
