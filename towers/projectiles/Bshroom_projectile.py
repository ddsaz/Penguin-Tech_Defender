import pygame
import os
import math
from towers.projectiles.Projectile import Projectile

class Bshroom_projectile(Projectile):
    def __init__(self, x: float, y: float, target, screen_size: tuple, attack_value: int, attack_type: str, enemies: list, aoe: int) -> None:
        super().__init__(x, y, target, screen_size)
        self.original_image = pygame.transform.scale(pygame.image.load(os.path.join(
            "assets", "towers", "projectiles", "bshroom_projectile.png")).convert_alpha(), (screen_size[0]/60, screen_size[0]/60))
        self.width = self.original_image.get_width()
        self.height = self.original_image.get_height()
        self.image = self.original_image  # La imagen que será rotada
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed = 8
        self.attack_value = attack_value
        self.attack_type = attack_type
        self.enemies = enemies
        self.aoe = aoe
        self.rotate_towards_target()

    def rotate_towards_target(self):
        """Rota la imagen del proyectil para que apunte hacia el objetivo."""
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        angle = math.degrees(math.atan2(-dy, dx)) - 90  # -90 grados para ajustar si el proyectil apunta hacia arriba inicialmente
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
        """Método para atacar al objetivo
        (Reduce el escudo o la vida de todos los objetivos dentro del rango de explosión de la torre)"""
        for enemy in self.enemies:
            if self.target.x + self.aoe >= enemy.x >= self.target.x - self.aoe and self.target.y + self.aoe >= enemy.y >= self.target.y - self.aoe:
                if enemy.Bresistance():
                    enemy.bouclier -= int(round(self.attack_value /
                                          enemy.resistance[self.attack_type]))

                else:
                    enemy.health -= int(round(self.attack_value /
                                        enemy.resistance[self.attack_type]))
