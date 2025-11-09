import pygame
import math
import config

class Robo(pygame.sprite.Sprite):
    """
    Simula o 'Arduino' (controlador de baixo nível).
    Recebe comandos simples (ex: 'FRENTE' até (x,y)) e os executa.
    """
    def __init__(self, x, y):
        super().__init__()
        
        # Atributos visuais (Sprite Pygame)
        self.image = pygame.Surface((config.ROBO_TAMANHO, config.ROBO_TAMANHO))
        self.image.fill(config.COR_AZUL_CLARO)
        self.rect = self.image.get_rect(center=(x, y))
        
        # Posição vetorial (permite floats para movimento suave)
        self.pos = pygame.math.Vector2(x, y)
        self.velocidade = config.ROBO_VELOCIDADE
        
        # Alvo de movimento
        self.alvo_pos = None
        self.angulo = 0 # Ângulo atual de movimento
        
        # Estado do "Arduino"
        self.comando_atual = "PARADO"
        
        # Simulação dos 8 Sensores QRE-8D
        # 0 = Vendo nada, 1 = Vendo linha
        self.sensores_simulados = [0, 0, 0, 0, 0, 0, 0, 0]

    def set_comando(self, comando, alvo_pos=None):
        """ Recebe um comando do 'Pi' (CerebroPi) """
        self.comando_atual = comando
        
        if self.comando_atual == "FRENTE":
            if alvo_pos:
                self.alvo_pos = pygame.math.Vector2(alvo_pos)
                # Calcula o ângulo necessário para ir ao alvo
                delta_x = self.alvo_pos.x - self.pos.x
                delta_y = self.alvo_pos.y - self.pos.y
                self.angulo = math.atan2(delta_y, delta_x)
                
                # Simula sensores de "seguindo linha"
                self.sensores_simulados = [0, 0, 1, 1, 1, 1, 0, 0]
            else:
                self.comando_atual = "PARADO"
                self.sensores_simulados = [0, 0, 0, 0, 0, 0, 0, 0]
        
        elif self.comando_atual == "PARADO":
            self.alvo_pos = None
            self.sensores_simulados = [0, 0, 0, 0, 0, 0, 0, 0]

    def update(self):
        """ Loop principal do 'Arduino'. Executa o comando atual. """
        
        status_reportado = None # O que vamos reportar ao "Pi"?
        
        if self.comando_atual == "FRENTE" and self.alvo_pos:
            # Calcula a distância até o alvo
            distancia = self.pos.distance_to(self.alvo_pos)
            
            if distancia < self.velocidade:
                # Chegamos!
                self.pos = self.alvo_pos
                self.alvo_pos = None
                self.comando_atual = "PARADO"
                
                # Simula sensores de "cheguei na interseção"
                self.sensores_simulados = [1, 1, 1, 1, 1, 1, 1, 1]
                
                # Reporta ao "Pi"
                status_reportado = "CHEGUEI_INTERSECAO"
            else:
                # Move o robô na direção do ângulo
                self.pos.x += math.cos(self.angulo) * self.velocidade
                self.pos.y += math.sin(self.angulo) * self.velocidade
        
        # Atualiza a posição do sprite (visual)
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        
        return status_reportado