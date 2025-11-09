import pygame
import sys
import math
import config
import robo
import cerebro_pi
import desenho

def encontrar_no_clicado(pos_mouse):
    """ Verifica se o clique do mouse foi perto de um nó do mapa. """
    for nome_no, pos_no in config.POSICOES_NOS.items():
        if math.dist(pos_mouse, pos_no) < 30: # 30 pixels de raio
            return nome_no
    return None

def main():
    # --- Inicialização ---
    pygame.init()
    pygame.font.init()
    
    # Criar a tela principal
    tela_principal = pygame.display.set_mode((config.TELA_LARGURA_TOTAL, config.TELA_ALTURA))
    pygame.display.set_caption("Simulação Robô de Logística (Pi + Arduino)")
    
    # Criar "sub-telas" (Surfaces) para o mundo e o dashboard
    # Isso facilita desenhar e gerenciar as coordenadas
    tela_mundo = pygame.Surface((config.TELA_LARGURA_MUNDO, config.TELA_ALTURA))
    tela_dashboard = pygame.Surface((config.TELA_LARGURA_DASHBOARD, config.TELA_ALTURA))
    
    # Relógio para controlar o FPS
    clock = pygame.time.Clock()
    
    # Fontes de texto
    font_titulo = pygame.font.Font(None, 28)
    font_media = pygame.font.Font(None, 24)
    font_pequena = pygame.font.Font(None, 20)
    
    # --- Criar Objetos ---
    
    # 1. Cérebro (Pi)
    meu_pi = cerebro_pi.CerebroPi(config.MAPA_GRAFO, config.POSICOES_NOS)
    
    # 2. Robô (Arduino)
    pos_inicial = config.POSICOES_NOS[meu_pi.no_atual]
    meu_robo = robo.Robo(pos_inicial[0], pos_inicial[1])
    
    # 3. Grupo de Sprites (para desenhar o robô)
    grupo_sprites = pygame.sprite.Group()
    grupo_sprites.add(meu_robo)

    # --- Loop Principal da Simulação ---
    rodando = True
    while rodando:
        
        # --- 1. Processar Eventos (Input) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Botão esquerdo
                    # Verifica se o clique foi na tela_mundo
                    if tela_mundo.get_rect().collidepoint(event.pos):
                        no_alvo = encontrar_no_clicado(event.pos)
                        if no_alvo:
                            print(f"--- Usuário clicou no Nó: {no_alvo} ---")
                            # Envia a ordem para o "Pi"
                            comando_pi = meu_pi.pedir_rota(no_alvo)
                            if comando_pi:
                                # Envia o primeiro comando do "Pi" para o "Arduino"
                                meu_robo.set_comando(comando_pi[0], comando_pi[1])
        
        # --- 2. Atualizar Lógica (Update) ---
        
        # Atualiza o "Arduino" (move o robô)
        status_arduino = meu_robo.update()
        
        # Comunicação: Arduino -> Pi
        if status_arduino == "CHEGUEI_INTERSECAO":
            # Avisa o "Pi" que chegamos
            comando_pi = meu_pi.reportar_chegada_no()
            
            # Comunicação: Pi -> Arduino
            if comando_pi:
                # O Pi deu um novo comando (ir para o próximo nó)
                meu_robo.set_comando(comando_pi[0], comando_pi[1])

        # --- 3. Desenhar (Render) ---
        
        # Limpa as sub-telas
        tela_mundo.fill(config.COR_PRETO)
        tela_dashboard.fill(config.COR_CINZA_CLARO)
        
        # Desenha o mundo
        desenho.desenhar_mapa(tela_mundo)
        grupo_sprites.draw(tela_mundo) # Desenha o robô
        
        # Desenha o dashboard
        desenho.desenhar_dashboard(tela_dashboard, meu_pi, meu_robo, 
                                   font_titulo, font_media, font_pequena)
        
        # Coloca as sub-telas na tela principal
        tela_principal.blit(tela_mundo, (0, 0))
        tela_principal.blit(tela_dashboard, (config.TELA_LARGURA_MUNDO, 0))
        
        # Atualiza o display
        pygame.display.flip()
        
        # Controla o FPS
        clock.tick(60) # 60 FPS

    # --- Fim ---
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()