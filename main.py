import pygame
import sys
import math
import config
import robo
import cerebro_pi
import desenho
import random
import log_manager 

def encontrar_no_clicado(pos_mouse):
    """ 
    Verifica se o clique do mouse foi perto de um nó do mapa.
    Recebe a posição do mouse JÁ AJUSTADA para o painel do mundo.
    """
    for nome_no, pos_no in config.POSICOES_NOS.items():
        if math.dist(pos_mouse, pos_no) < 30: # 30 pixels de raio
            return nome_no
    return None

def main():
    # --- Inicialização ---
    pygame.init()
    pygame.font.init()
    
    tela_principal = pygame.display.set_mode((config.TELA_LARGURA_TOTAL, config.TELA_ALTURA))
    pygame.display.set_caption("Simulação Robô de Logística")
    
    tela_pedidos = pygame.Surface((config.TELA_LARGURA_PEDIDOS, config.TELA_ALTURA))
    tela_mundo = pygame.Surface((config.TELA_LARGURA_MUNDO, config.TELA_ALTURA))
    tela_dashboard = pygame.Surface((config.TELA_LARGURA_DASHBOARD, config.TELA_ALTURA))
    
    clock = pygame.time.Clock()
    
    try:
        font_titulo = pygame.font.SysFont('Calibri', 28, bold=True)
        font_media = pygame.font.SysFont('Calibri', 24)
        font_pequena = pygame.font.SysFont('Calibri', 20)
    except:
        log_manager.add_log("Aviso: Fonte 'Calibri' não encontrada. Usando fonte padrão.")
        font_titulo = pygame.font.Font(None, 28)
        font_media = pygame.font.Font(None, 24)
        font_pequena = pygame.font.Font(None, 20)
    
    # --- Criar Objetos ---
    meu_pi = cerebro_pi.CerebroPi(config.MAPA_GRAFO, config.POSICOES_NOS)
    pos_inicial = config.POSICOES_NOS[meu_pi.no_atual]
    meu_robo = robo.Robo(pos_inicial[0], pos_inicial[1])
    
    grupo_sprites = pygame.sprite.Group()
    grupo_sprites.add(meu_robo)

    # --- Variáveis de Controle ---
    input_mode = False
    input_text = ""
    robot_is_active = False # O robô começa PAUSADO

    # --- Loop Principal da Simulação ---
    rodando = True
    while rodando:
        
        # --- 1. Processar Eventos (Input) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    x_pedidos_fim = config.TELA_LARGURA_PEDIDOS
                    x_mundo_fim = x_pedidos_fim + config.TELA_LARGURA_MUNDO
                    
                    if event.pos[0] < x_pedidos_fim:
                        pass 
                    elif event.pos[0] < x_mundo_fim:
                        if not input_mode:
                            pos_mundo_ajustada = (event.pos[0] - x_pedidos_fim, event.pos[1])
                            no_alvo = encontrar_no_clicado(pos_mundo_ajustada)
                            
                            if no_alvo:
                                log_manager.add_log(f"--- Usuário clicou no Nó (Mov. Manual): {no_alvo} ---") # <-- MUDANÇA
                                meu_pi.add_new_package(0, no_alvo)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and not input_mode:
                    input_mode = True
                    input_text = ""
                
                elif event.key == pygame.K_SPACE and not input_mode:
                    robot_is_active = not robot_is_active
                    if robot_is_active:
                        log_manager.add_log("--- ROBÔ INICIADO ---") 
                    else:
                        log_manager.add_log("--- ROBÔ PAUSADO ---") 
                
                elif input_mode:
                    if event.key == pygame.K_RETURN:
                        destino_node = input_text.upper().strip()
                        if destino_node:
                            log_manager.add_log(f"--- Usuário criou Pedido para: {destino_node} ---") 
                            meu_pi.add_new_package(random.randint(1, 1000), destino_node)
                        
                        input_mode = False
                        input_text = ""
                        
                    elif event.key == pygame.K_ESCAPE:
                        input_mode = False
                        input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.unicode.isalpha():
                        input_text += event.unicode

        # --- 2. Atualizar Lógica (Update) ---
        status_arduino = meu_robo.update(robot_is_active)
        
        if status_arduino == "CHEGUEI_INTERSECAO":
            comando_pi = meu_pi.reportar_chegada_no()
            if comando_pi:
                meu_robo.set_comando(comando_pi[0], comando_pi[1])
        
        if robot_is_active and meu_pi.status == "PARADO":
            comando_pi = meu_pi.check_for_new_job()
            if comando_pi:
                meu_robo.set_comando(comando_pi[0], comando_pi[1])

        # --- 3. Desenhar (Render) ---
        tela_pedidos.fill(config.COR_CINZA_CLARO)
        tela_mundo.fill(config.COR_PRETO)
        tela_dashboard.fill(config.COR_CINZA_CLARO)
        
        desenho.desenhar_painel_pedidos(tela_pedidos, font_titulo, font_media, font_pequena,
                                        input_mode, input_text, robot_is_active)
        desenho.desenhar_mapa(tela_mundo, font_media)
        grupo_sprites.draw(tela_mundo) 
        desenho.desenhar_dashboard(tela_dashboard, meu_pi, meu_robo, 
                                   font_titulo, font_media, font_pequena)
        
        tela_principal.blit(tela_pedidos, (0, 0))
        tela_principal.blit(tela_mundo, (config.TELA_LARGURA_PEDIDOS, 0))
        tela_principal.blit(tela_dashboard, (config.TELA_LARGURA_PEDIDOS + config.TELA_LARGURA_MUNDO, 0))
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()