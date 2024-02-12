import pygame
import os
import math
from towers.projectiles.Projectile import Projectile

class SPshroom_projectile(Projectile):
    def __init__(self, x: float, y: float, target, screen_size: tuple, attack_value: int, attack_type: str, creator) -> None:
        super().__init__(x, y, target, screen_size)
        self.original_image = pygame.transform.scale(pygame.image.load(os.path.join(
            "assets", "towers", "projectiles", "spshroom_projectile.png")).convert_alpha(), (screen_size[0]/60, screen_size[0]/60))
        self.image = self.original_image  # La imagen se actualizará con la rotación
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed = 10  # Velocidad ajustada para simulación de despegue y movimiento parabólico
        self.attack_value = attack_value
        self.attack_type = attack_type
        self.creator = creator
        self.vertical_movement = True  # Indica si el proyectil está en movimiento vertical inicial
        self.vertical_timer = pygame.time.get_ticks()  # Temporizador para el movimiento vertical
        self.parabola_start = False  # Indica si el proyectil ha iniciado el movimiento en parábola
        self.angle_to_target = 0  # Ángulo hacia el objetivo para la orientación y movimiento del cohete

    def update(self, enemies):
        current_time = pygame.time.get_ticks()
        if self.vertical_movement:
            # Mover verticalmente hacia arriba durante 1 segundo
            self.y -= self.speed * 0.5  # Desplazamiento más lento en la fase vertical
            if current_time - self.vertical_timer > 1000:  # Después de 1 segundo
                self.vertical_movement = False
                self.parabola_start = True
                self.calculate_parabola_angle()

        elif self.parabola_start:
            self.move_in_parabola()

        self.rect.x, self.rect.y = self.x, self.y
        self.rotate_to_target()

    def calculate_parabola_angle(self):
        # Calcular el ángulo hacia el objetivo para el movimiento parabólico
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        self.angle_to_target = math.atan2(dy, dx)

    def move_in_parabola(self):
        # Mover en parábola hacia el objetivo
        self.x += math.cos(self.angle_to_target) * self.speed
        self.y += math.sin(self.angle_to_target) * self.speed

    def rotate_to_target(self):
        # Rotar la imagen del proyectil para que siempre apunte hacia el objetivo o la dirección de movimiento
        if self.vertical_movement:
            angle_degrees = -90  # Apuntar hacia arriba durante el movimiento vertical
        else:
            angle_degrees = math.degrees(self.angle_to_target) - 90
        self.image = pygame.transform.rotate(self.original_image, angle_degrees)
        self.rect = self.image.get_rect(center=(self.x, self.y))  # Ajustar el rectángulo al centro de la imagen rotada

    def attack(self):
        """Método para atacar la cible, adaptado del SNshroom_projectile"""
        # Asumiendo que el método enemy_check verifica si el proyectil ha colisionado con un enemigo.
        # Esto requiere que `self.target` sea accesible y tenga atributos `health`, `resistance`, etc.
        if not hasattr(self.target, 'Bresistance') or not self.target.Bresistance():
            self.target.health -= int(round(self.attack_value / self.target.resistance[self.attack_type]))
        else:
            self.target.bouclier -= int(round(self.attack_value / self.target.resistance[self.attack_type]))

        # Considera implementar la lógica de 'M.res debuff' si es relevante para tu juego.
