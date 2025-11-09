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
        
        # --- MUDANÇA AQUI: Carregar a imagem PNG ---
        try:
            # Tenta carregar a imagem 'robot.png' da pasta do projeto
            original_image = pygame.image.load("robot.png").convert_alpha()
            # Redimensiona a imagem para o tamanho padrão do robô
            self.image = pygame.transform.scale(original_image, (config.ROBO_TAMANHO, config.ROBO_TAMANHO))
        except FileNotFoundError:
            # Se 'robot.png' não for encontrado, usa o quadrado azul
            print("Aviso: 'robot.png' não encontrado. Usando o quadrado azul padrão.")
            self.image = pygame.Surface((config.ROBO_TAMANHO, config.ROBO_TAMANHO))
            self.image.fill(config.COR_AZUL_CLARO)
        
        self.rect = self.image.get_rect(center=(x, y))
        # --- FIM DA MUDANÇA ---
        
        # Posição vetorial (permite floats para movimento suave)
        self.pos = pygame.math.Vector2(x, y)
        self.velocidade = config.ROBO_VELOCIDADE
        
        # Alvo de movimento
        self.alvo_pos = None
        self.angulo = 0 
        self.comando_atual = "PARADO"
        
        # Simulação dos 8 Sensores QRE-8D
        self.sensores_simulados = [0, 0, 0, 0, 0, 0, 0, 0]

    def set_comando(self, comando, alvo_pos=None):
        """ Recebe um comando do 'Pi' (CerebroPi) """
        self.comando_atual = comando
        
        if self.comando_atual == "FRENTE":
            if alvo_pos:
                self.alvo_pos = pygame.math.Vector2(alvo_pos)
                delta_x = self.alvo_pos.x - self.pos.x
                delta_y = self.alvo_pos.y - self.pos.y
                self.angulo = math.atan2(delta_y, delta_x)
                
                self.sensores_simulados = [0, 0, 1, 1, 1, 1, 0, 0]
            else:
                self.comando_atual = "PARADO"
                self.sensores_simulados = [0, 0, 0, 0, 0, 0, 0, 0]
        
        elif self.comando_atual == "PARADO":
            self.alvo_pos = None
            self.sensores_simulados = [0, 0, 0, 0, 0, 0, 0, 0]

    def update(self, is_active): # Aceita o parâmetro
        """ 
        Loop principal do 'Arduino'. Executa o comando atual.
        SÓ SE MOVE se is_active for True.
        """
        
        status_reportado = None # O que vamos reportar ao "Pi"?
        
        if is_active and self.comando_atual == "FRENTE" and self.alvo_pos:
            
            distancia = self.pos.distance_to(self.alvo_pos)
            
            if distancia < self.velocidade:
                # Chegamos!
                self.pos = self.alvo_pos
                self.alvo_pos = None
                self.comando_atual = "PARADO"
                self.sensores_simulados = [1, 1, 1, 1, 1, 1, 1, 1]
                status_reportado = "CHEGUEI_INTERSECAO"
            else:
                # Move o robô na direção do ângulo
                self.pos.x += math.cos(self.angulo) * self.velocidade
                self.pos.y += math.sin(self.angulo) * self.velocidade
        
        # A atualização do sprite (visual) acontece sempre, mesmo pausado
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        
        return status_reportado