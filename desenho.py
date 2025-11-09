import pygame
import config

# --- Funções Auxiliares de Desenho ---

def desenhar_texto(surface, texto, pos, font, cor=config.COR_BRANCO):
    """ Desenha texto simples na tela. """
    text_surface = font.render(str(texto), True, cor)
    surface.blit(text_surface, pos)

def desenhar_mapa(surface):
    """ Desenha o mapa (linhas e nós) no mundo da simulação. """
    # 1. Desenha as Linhas (Arestas)
    for no_inicio, conexoes in config.MAPA_GRAFO.items():
        pos_inicio = config.POSICOES_NOS[no_inicio]
        for no_fim in conexoes:
            pos_fim = config.POSICOES_NOS[no_fim]
            # Linha de fundo (cinza)
            pygame.draw.line(surface, config.COR_LINHA, pos_inicio, pos_fim, 10)
            # Linha central (amarela)
            pygame.draw.line(surface, config.COR_LINHA_CENTRO, pos_inicio, pos_fim, 2)

    # 2. Desenha os Nós (Vértices)
    for nome, pos in config.POSICOES_NOS.items():
        pygame.draw.circle(surface, config.COR_VERMELHO, pos, 20)
        desenhar_texto(surface, nome, (pos[0] + 25, pos[1] - 15), pygame.font.Font(None, 30))

def desenhar_dashboard(surface, cerebro_pi, robo, font_titulo, font_media, font_pequena):
    """ Desenha todo o painel de controle da direita. """
    surface.fill(config.COR_CINZA_CLARO)
    
    # Posição Y atual (para desenhar linha por linha)
    y = 20

    # --- Painel 1: Cérebro (Pi) ---
    desenhar_texto(surface, "Cérebro (Pi) - Alto Nível", (10, y), font_titulo, config.COR_AZUL_CLARO)
    y += 40
    
    cor_status_pi = config.COR_VERDE if cerebro_pi.status == "NAVEGANDO" else \
                      config.COR_VERMELHO if cerebro_pi.status == "ERRO" else config.COR_BRANCO
    desenhar_texto(surface, f"Status:", (15, y), font_media)
    desenhar_texto(surface, f"{cerebro_pi.status}", (130, y), font_media, cor_status_pi)
    y += 30
    
    desenhar_texto(surface, f"Nó Atual:", (15, y), font_media)
    desenhar_texto(surface, f"{cerebro_pi.no_atual}", (130, y), font_media, config.COR_VERDE)
    y += 30
    
    desenhar_texto(surface, f"Destino:", (15, y), font_media)
    desenhar_texto(surface, f"{cerebro_pi.no_destino or 'N/A'}", (130, y), font_media)
    y += 30
    
    rota_str = ' -> '.join([cerebro_pi.no_atual, cerebro_pi.proximo_no or '?', *cerebro_pi.rota_calculada]) \
               if cerebro_pi.status == "NAVEGANDO" else "Nenhuma"
    desenhar_texto(surface, "Rota (A*):", (15, y), font_media)
    y += 30
    desenhar_texto(surface, f"{rota_str}", (25, y), font_pequena)
    y += 50

    # Linha divisória
    pygame.draw.line(surface, config.COR_CINZA, (10, y), (config.TELA_LARGURA_DASHBOARD - 10, y), 2)
    y += 30

    # --- Painel 2: Controlador (Arduino) ---
    desenhar_texto(surface, "Controlador (Arduino) - Baixo Nível", (10, y), font_titulo, config.COR_AZUL_CLARO)
    y += 40
    
    cor_status_robo = config.COR_VERDE if robo.comando_atual == "FRENTE" else config.COR_BRANCO
    desenhar_texto(surface, f"Comando:", (15, y), font_media)
    desenhar_texto(surface, f"{robo.comando_atual}", (130, y), font_media, cor_status_robo)
    y += 30
    
    velocidade = config.ROBO_VELOCIDADE if robo.comando_atual == "FRENTE" else 0
    desenhar_texto(surface, f"Velocidade:", (15, y), font_media)
    desenhar_texto(surface, f"{velocidade:.1f} px/f", (130, y), font_media)
    y += 50
    
    # Desenhar os 8 Sensores QRE-8D
    desenhar_texto(surface, "Sensores QRE-8D (Simulado):", (15, y), font_media)
    y += 40
    sensor_x_start = 30
    for i, valor_sensor in enumerate(robo.sensores_simulados):
        cor_sensor = config.COR_VERDE if valor_sensor == 1 else config.COR_CINZA
        pos_x = sensor_x_start + (i * (30 + 10)) # 30 = tamanho, 10 = espaço
        pygame.draw.rect(surface, cor_sensor, (pos_x, y, 30, 30))
        desenhar_texto(surface, f"{i+1}", (pos_x + 10, y + 35), font_pequena)
    y += 80
    
    # --- Painel 3: Ajuda ---
    pygame.draw.line(surface, config.COR_CINZA, (10, y), (config.TELA_LARGURA_DASHBOARD - 10, y), 2)
    y += 30
    desenhar_texto(surface, "Instruções:", (10, y), font_titulo)
    y += 40
    desenhar_texto(surface, "Clique em um Nó (A, B, C, D)", (15, y), font_media)
    y += 30
    desenhar_texto(surface, "para definir um novo destino.", (15, y), font_media)