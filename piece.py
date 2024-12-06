from objetflottant import Objetflottant

class Piece(Objetflottant):
    def __init__(self, x, y, image_path="assets/images/piece.png"):
        super().__init__(x, y, image_path)
        # Autres initialisations spécifiques au Coeur si besoin
