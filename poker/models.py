import random


class Baraja:
    def __init__(self):
        self.cartas = inicializar_baraja()

    def sacar_carta(self):
        carta = random.choice(self.cartas)
        self.cartas.remove(carta)
        return carta


def inicializar_baraja():
    return ['1C', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', '11C', '12C', '13C', '1P', '2P', '3P',
            '4P', '5P', '6P', '7P', '8P', '9P', '10P', '11P', '12P', '13P', '1T', '2T', '3T', '4T', '5T', '6T',
            '7T', '8T', '9T', '10T', '11T', '12T', '13T', '1D', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D',
            '11D', '12D', '13D']
