import math
import pygame
import os
from towers.projectiles.Projectile import Projectile


class Wshroom_projectile(Projectile):
    def __init__(self, x: float, y: float, target, screen_size: tuple, attack_value: int, attack_type: str) -> None:
        super().__init__(x, y, target, screen_size)
        """Sous-classe du projectile du Wizard shroom
        - x: nombre réel correspondant à la coordonnée x de départ du projectile
        - y: nombre réel correspondant à la coordonnée y de départ du projectile
        - target: ennemi ciblé
        - screen_size: tuple contenant la largeur et la hauteur de la fenêtre
        - attack_value: nombre entier correspondant aux dégats infligés à la cible
        - attack_type: chaine de caractère désignant le type d'attaque (Physique ou Magique)"""

        self.image = pygame.transform.scale(pygame.image.load(os.path.join(
            "assets", "towers", "projectiles", "wshroom_projectile.png")).convert_alpha(), (50, 50))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed = 15
        self.attack_value = attack_value
        self.attack_type = attack_type

    def rotate_towards_target(self):
        """Rota la imagen del proyectil para que apunte hacia el objetivo."""
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        angle = math.degrees(math.atan2(-dy, dx))  # -90 grados para ajustar si el proyectil apunta hacia arriba inicialmente
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)  # Ajusta el rect para mantener el centro

    def update(self):
        """Actualiza la posición del proyectil y su orientación hacia el objetivo."""
        # Calcula la diferencia de posición entre el proyectil y el objetivo
        dx, dy = self.target.x - self.x, self.target.y - self.y
        # Calcula el ángulo hacia el objetivo en radianes y luego lo convierte a grados
        angle = math.atan2(dy, dx)
        self.image = pygame.transform.rotate(self.original_image, -math.degrees(angle))
        # Actualiza el rectángulo para que coincida con la nueva imagen rotada
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Mueve el proyectil hacia el objetivo (la lógica de movimiento se mantiene igual)


    def attack(self) -> None:
        """Méthode pour attaquer la cible
        (Retirer du bouclier ou de la vie)"""

        if self.target.Bresistance():
            self.target.bouclier -= int(round(self.attack_value /
                                        self.target.resistance[self.attack_type]))

        else:
            self.target.health -= int(round(self.attack_value /
                                      self.target.resistance[self.attack_type]))
