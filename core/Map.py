import pygame  # Importa la biblioteca Pygame para desarrollo de videojuegos
import os  # Importa la biblioteca os para interactuar con el sistema operativo
import json  # Importa la biblioteca json para manejar datos en formato JSON

class Map:
    def __init__(self, nom_map: str, screen_size: tuple) -> None:
        """Inicializa un mapa para el juego.
        
        Args:
            nom_map (str): Nombre del mapa a cargar.
            screen_size (tuple): Tamaño de la pantalla (ancho, alto).
        """
        # Establece las dimensiones de la pantalla basadas en el argumento proporcionado
        self.width = screen_size[0]
        self.height = screen_size[1]
        # Calcula el tamaño de una 'unidad' basada en la altura de la pantalla, para posicionar elementos en el mapa
        self.unit = (self.height - (self.height//10)) // 8
        # Calcula el tamaño de una 'unidadL' basada en el ancho de la pantalla, usado para el posicionamiento horizontal
        self.unitL = self.width / 14
        # Guarda el nombre del mapa
        self.nom_map = nom_map

        # Carga los datos de los mapas desde un archivo JSON
        with open("data/Maps.json", "r") as maps_file:
            self.maps = json.load(maps_file)

        # Convierte las posiciones y tamaños de los elementos del mapa de los datos JSON a valores utilizables
        self.convert_json_maps()
        # Carga y escala la imagen de fondo del mapa al tamaño de la pantalla
        self.bg = pygame.transform.scale(pygame.image.load(os.path.join(
            "assets", "maps", self.maps[nom_map]["asset"])).convert(), (self.width, self.height*0.9))
        # Asigna las posiciones de inicio, camino, torres y agua basadas en los datos del mapa
        self.start = self.maps[nom_map]["start"]
        self.path = self.maps[nom_map]["path"]
        self.tower_places = self.maps[nom_map]["tower_placement"]
        self.water_places = self.maps[nom_map]["water_placement"]
        # Intenta cargar la música del mapa y maneja la excepción si el archivo no existe
        try:
            self.music = pygame.mixer.Sound(os.path.join(
                "assets", "sounds", "musics", self.maps[nom_map]["music"]))
        except pygame.error:
            self.music = None

    def convert_json_maps(self) -> None:
        """Convierte las coordenadas de los elementos del mapa de valores relativos a valores absolutos basados en el tamaño de la pantalla."""
        # Itera a través de cada mapa y sus datos
        for map_name, mapdata in self.maps.items():
            # Itera a través de cada tipo de dato en el mapa (inicio, camino, etc.)
            for data_name, data_value in mapdata.items():
                # Convierte las coordenadas de inicio a valores absolutos
                if data_name == "start":
                    self.maps[map_name]["start"] = (
                        data_value[0]*self.unitL, data_value[1]*self.unit)
                # Convierte las coordenadas del camino
                if data_name == "path":
                    for coord in data_value:
                        # Ajusta las coordenadas basándose en si el mapa es "meadow" o no
                        self.maps[map_name]["path"][self.maps[map_name]["path"].index(
                            coord)] = (coord[0]*self.unitL, coord[1]*self.unit) if self.nom_map == "meadow" else (
                                coord[0]*self.unitL + (self.unitL*0.15), coord[1]*self.unit)
                # Convierte las coordenadas de colocación de torres
                if data_name == "tower_placement":
                    if data_value != [[]]:  # Verifica que haya datos para convertir
                        for coord in data_value:
                            # Ajusta las coordenadas igual que con el camino
                            self.maps[map_name]["tower_placement"][self.maps[map_name]["tower_placement"].index(
                                coord)] = (coord[0]*self.unitL, coord[1]*self.unit) if self.nom_map == "meadow" else (
                                    coord[0]*self.unitL + (self.unitL*0.15), coord[1]*self.unit)
                # Convierte las coordenadas de colocación de agua
                if data_name == "water_placement":
                    if data_value != [[]]:  # Verifica que haya datos para convertir
                        for coord in data_value:
                            # Ajusta las coordenadas igual que con el camino y las torres
                            self.maps[map_name]["water_placement"][self.maps[map_name]["water_placement"].index(
                                coord)] = (coord[0]*self.unitL, coord[1]*self.unit) if self.nom_map == "meadow" else (
                                    coord[0]*self.unitL + (self.unitL*0.15), coord[1]*self.unit)

    def reset_placements(self) -> None:
        """Reinicia las colocaciones de torres y agua a sus valores predeterminados."""
        # Recarga los datos de los mapas desde el archivo JSON
        with open("data/Maps.json", "r") as maps_file:
            self.maps = json.load(maps_file)
        # Reaplica las conversiones de coordenadas a los datos recargados
        self.convert_json_maps()
        # Actualiza las colocaciones de torres y agua a los valores recién convertidos
        self.tower_places = self.maps[self.nom_map]["tower_placement"]
        self.water_places = self.maps[self.nom_map]["water_placement"]
