import pygame
import os
from towers.Tower import Tower
from towers.projectiles.Bshroom_projectile import Bshroom_projectile

class Bshroom(Tower):
    def __init__(self, x: float, y: float, screen_size: tuple, difficulty: str) -> None:
        super().__init__(x, y, screen_size, difficulty)
        """Subclase de la torre Boom Shroom
        - x: número real correspondiente a la posición x de la torre
        - y: número real correspondiente a la posición y de la torre
        - screen_size: tupla que contiene el ancho y la altura de la ventana
        - difficulty: cadena de caracteres que corresponde al archivo json de los precios de la torre y mejoras"""

        self.name = "Boom Shroom"
        self.images = [pygame.transform.scale(pygame.image.load(os.path.join(
                        "assets", "towers", "boom_shroom", "boom_shroom.png")).convert_alpha(), (self.width, self.height)),
                       pygame.transform.scale(pygame.image.load(os.path.join(
                        "assets", "towers", "boom_shroom", "boom_shroom2.png")).convert_alpha(), (self.width, self.height)),
                       pygame.transform.scale(pygame.image.load(os.path.join(
                        "assets", "towers", "boom_shroom", "boom_shroom3.png")).convert_alpha(), (self.width, self.height)),
                       pygame.transform.scale(pygame.image.load(os.path.join(
                        "assets", "towers", "boom_shroom", "boom_shroom4.png")).convert_alpha(), (self.width, self.height)),
                       pygame.transform.scale(pygame.image.load(os.path.join(
                        "assets", "towers", "boom_shroom", "boom_shroom3.png")).convert_alpha(), (self.width, self.height)),
                       pygame.transform.scale(pygame.image.load(os.path.join(
                        "assets", "towers", "boom_shroom", "boom_shroom2.png")).convert_alpha(), (self.width, self.height))]
        self.icon_image = pygame.transform.scale(pygame.image.load(os.path.join(
            "assets", "towers", "boom_shroom", "icon.png")).convert_alpha(), (80, 80))
        self.image_index = 0
        self.image = self.images[round(self.image_index)]
        self.animating = False
        self.anim_speed = 0.5
        self.cost = self.upgrades[self.name]["base"]["cost"]
        self.value = self.cost
        self.attack_type = "Physical"
        self.placement_type = "Ground"
        self.range = self.screen_size[0]/3.84  # Rango incrementado
        self.range_circle = pygame.Surface(
            (self.range*2, self.range*2), pygame.SRCALPHA).convert_alpha()
        pygame.draw.circle(self.range_circle, (50, 50, 50, 128),
                           (self.range, self.range), self.range)
        self.attack_value = 10  # Daño reducido a una cuarta parte
        self.shoot_interval = 5  # Velocidad de disparo duplicada
        self.aoe = self.upgrades[self.name]["base"]["aoe"]
        self.upgrade_cost = [self.upgrades[self.name]["0"][str(
            self.level[0]+1)]["upgrade_cost"], self.upgrades[self.name]["1"][str(self.level[1]+1)]["upgrade_cost"]]
        self.sell_cost = int(self.value*0.8)

    def main_attack(self, target, enemies, current_tick, projectiles) -> list:
        """Manejo del ataque de la torre, devuelve el proyectil creado por el ataque de la torre
        - target: enemigo objetivo
        - enemies: lista de enemigos
        - current_tick: entero correspondiente al tick en el cual se llama al método para manejar el intervalo de disparo
        - projectiles: lista de proyectiles a la cual se añadirá el proyectil devuelto"""
        if current_tick - self.last_shot_time > self.shoot_interval:
            self.animating = True
            projectiles.append(Bshroom_projectile(self.x + self.width/2, self.y + self.height/2,
                               target, self.screen_size, self.attack_value, self.attack_type, enemies, self.aoe))
            self.last_shot_time = current_tick
        return projectiles
