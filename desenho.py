import pygame
import config
import log_manager 

# --- Funções Auxiliares de Desenho ---

def desenhar_texto(surface, texto, pos, font, cor=config.COR_BRANCO):
    """ Desenha texto simples na tela. """
    text_surface = font.render(str(texto), True, cor)
    surface.blit(text_surface, pos)

def desenhar_mapa(surface, font): # Recebe a fonte
    """ Desenha o mapa (linhas e nós) no mundo da simulação. """
    for no_inicio, conexoes in config.MAPA_GRAFO.items():
        pos_inicio = config.POSICOES_NOS[no_inicio]
        for no_fim in conexoes:
            pos_fim = config.POSICOES_NOS[no_fim]
            pygame.draw.line(surface, config.COR_LINHA, pos_inicio, pos_fim, 10)
            pygame.draw.line(surface, config.COR_LINHA_CENTRO, pos_inicio, pos_fim, 2)

    for nome, pos in config.POSICOES_NOS.items():
        pygame.draw.circle(surface, config.COR_VERMELHO, pos, 20)
        desenhar_texto(surface, nome, (pos[0] + 25, pos[1] - 15), font)

def desenhar_avl_tree(surface, node, x, y, h_spacing, v_spacing, font):
    """
    Função recursiva para desenhar a Árvore AVL no dashboard.
    """
    if node is None:
        return
    pygame.draw.circle(surface, config.COR_AZUL, (int(x), int(y)), 20)
    desenhar_texto(surface, node.key, (int(x) - 12, int(y) - 10), font, config.COR_BRANCO)
    y_filho = y + v_spacing
    if node.left:
        x_filho_esq = x - h_spacing
        pygame.draw.line(surface, config.COR_CINZA, (x, y + 20), (x_filho_esq, y_filho - 20), 2)
        desenhar_avl_tree(surface, node.left, x_filho_esq, y_filho, h_spacing / 2, v_spacing, font)
    if node.right:
        x_filho_dir = x + h_spacing
        pygame.draw.line(surface, config.COR_CINZA, (x, y + 20), (x_filho_dir, y_filho - 20), 2)
        desenhar_avl_tree(surface, node.right, x_filho_dir, y_filho, h_spacing / 2, v_spacing, font)

def desenhar_rb_tree(surface, node, nil_node, x, y, h_spacing, v_spacing, font):
    """
    Função recursiva para desenhar a Árvore Red-Black no dashboard.
    node: nó atual
    nil_node: referência ao nó NIL da árvore (sentinela)
    """
    if node is None or node == nil_node:
        return
    
    
    cor_no = config.COR_VERMELHO if node.color == "RED" else config.COR_PRETO
    
    pygame.draw.circle(surface, cor_no, (int(x), int(y)), 20)
    desenhar_texto(surface, node.key, (int(x) - 12, int(y) - 10), font, config.COR_BRANCO)
    
    y_filho = y + v_spacing
    
    if node.left != nil_node:
        x_filho_esq = x - h_spacing
        pygame.draw.line(surface, config.COR_CINZA, (x, y + 20), (x_filho_esq, y_filho - 20), 2)
        desenhar_rb_tree(surface, node.left, nil_node, x_filho_esq, y_filho, h_spacing / 2, v_spacing, font)
    
    if node.right != nil_node:
        x_filho_dir = x + h_spacing
        pygame.draw.line(surface, config.COR_CINZA, (x, y + 20), (x_filho_dir, y_filho - 20), 2)
        desenhar_rb_tree(surface, node.right, nil_node, x_filho_dir, y_filho, h_spacing / 2, v_spacing, font)


# --- PAINEL DE PEDIDOS (ESQUERDA) ---
def desenhar_painel_pedidos(surface, font_titulo, font_media, font_pequena,
                            input_mode, input_text, robot_is_active):
    
    surface.fill(config.COR_CINZA_CLARO)
    y = 20
    
    desenhar_texto(surface, "Controle de Pedidos", (10, y), font_titulo, config.COR_AZUL_CLARO)
    y += 50
    
    desenhar_texto(surface, "Aperte 'P' para novo Pedido:", (15, y), font_media)
    y += 40

    if input_mode:
        desenhar_texto(surface, "Novo Pedido:", (15, y), font_media, config.COR_VERDE)
        y += 30
        desenhar_texto(surface, "Digite o Nó (A-P) e aperte ENTER:", (15, y), font_pequena)
        y += 25
        pygame.draw.rect(surface, config.COR_PRETO, (15, y, config.TELA_LARGURA_PEDIDOS - 30, 40))
        pygame.draw.rect(surface, config.COR_BRANCO, (15, y, config.TELA_LARGURA_PEDIDOS - 30, 40), 1)
        
        cursor = "_" if (pygame.time.get_ticks() // 500) % 2 == 0 else ""
        desenhar_texto(surface, f"{input_text.upper()}{cursor}", (25, y + 10), font_media)
        y += 60
    else:
         y += 125 # Pula o espaço da caixa de texto
         
    # --- Botões de Controle ---
    pygame.draw.line(surface, config.COR_CINZA, (10, y), (config.TELA_LARGURA_PEDIDOS - 10, y), 2)
    y += 30
    
    if robot_is_active:
        desenhar_texto(surface, "Robô ATIVO", (15, y), font_media, config.COR_VERDE)
        y += 30
        desenhar_texto(surface, "Aperte 'ESPAÇO' para PAUSAR", (15, y), font_pequena)
    else:
        desenhar_texto(surface, "Robô PAUSADO", (15, y), font_media, config.COR_VERMELHO)
        y += 30
        desenhar_texto(surface, "Aperte 'ESPAÇO' para INICIAR", (15, y), font_pequena)
    y += 50
    
    # --- PAINEL: LOG DO SISTEMA ---
    pygame.draw.line(surface, config.COR_CINZA, (10, y), (config.TELA_LARGURA_PEDIDOS - 10, y), 2)
    y += 30
    desenhar_texto(surface, "Log do Sistema:", (10, y), font_titulo)
    y += 40

    mensagens = log_manager.get_messages()
    
    log_font = font_pequena
    cor_log = config.COR_CINZA
    altura_linha = log_font.get_height() + 3
    
    for i, msg in enumerate(mensagens):
        msg_limpa = msg.replace("---", "")
        desenhar_texto(surface, msg_limpa, (15, y + (i * altura_linha)), log_font, cor_log)


# --- DASHBOARD (DIREITA) ---
def desenhar_dashboard(surface, cerebro_pi, robo, font_titulo, font_media, font_pequena):
    """ Desenha o painel de status da direita. """
    surface.fill(config.COR_CINZA_CLARO)
    
    y = 20 # Posição Y atual

    # --- Painel 1: Cérebro (Pi) ---
    desenhar_texto(surface, "Raspberry Pi - Status", (10, y), font_titulo, config.COR_AZUL_CLARO)
    y += 40
    cor_status_pi = config.COR_VERDE if cerebro_pi.status == "NAVEGANDO" else config.COR_BRANCO
    desenhar_texto(surface, f"Status:", (15, y), font_media)
    desenhar_texto(surface, f"{cerebro_pi.status}", (130, y), font_media, cor_status_pi)
    y += 30
    desenhar_texto(surface, f"Pedido Ativo:", (15, y), font_media)
    desenhar_texto(surface, f"{cerebro_pi.active_job_key or 'Nenhum'}", (130, y), font_media, config.COR_VERDE)
    y += 30
    desenhar_texto(surface, f"Nó Atual:", (15, y), font_media)
    desenhar_texto(surface, f"{cerebro_pi.no_atual}", (130, y), font_media)
    y += 30
    desenhar_texto(surface, f"Destino:", (15, y), font_media)
    desenhar_texto(surface, f"{cerebro_pi.no_destino or 'N/A'}", (130, y), font_media)
    y += 30
    rota_str = ' -> '.join([cerebro_pi.no_atual, cerebro_pi.proximo_no or '?', *cerebro_pi.rota_calculada]) \
               if cerebro_pi.status == "NAVEGANDO" else "Nenhuma"
    desenhar_texto(surface, "Rota (A*):", (15, y), font_media)
    y += 30
    desenhar_texto(surface, f"{rota_str}", (25, y), font_pequena)
    y += 30

    # --- Painel 2: Controlador (Arduino) ---
    pygame.draw.line(surface, config.COR_CINZA, (10, y), (config.TELA_LARGURA_DASHBOARD - 10, y), 2)
    y += 20
    desenhar_texto(surface, "Esp32 - Status", (10, y), font_titulo, config.COR_AZUL_CLARO)
    y += 40
    cor_status_robo = config.COR_VERDE if robo.comando_atual == "FRENTE" else config.COR_BRANCO
    desenhar_texto(surface, f"Comando:", (15, y), font_media)
    desenhar_texto(surface, f"{robo.comando_atual}", (130, y), font_media, cor_status_robo)
    y += 30
    velocidade = config.ROBO_VELOCIDADE if robo.comando_atual == "FRENTE" else 0
    desenhar_texto(surface, f"Velocidade:", (15, y), font_media)
    desenhar_texto(surface, f"{velocidade:.1f} m/s", (130, y), font_media)
    y += 40
    desenhar_texto(surface, "Sensor QRE-8D:", (15, y), font_media)
    y += 40
    sensor_x_start = (config.TELA_LARGURA_DASHBOARD - (8 * 40 - 10)) / 2 # Centraliza os sensores
    for i, valor_sensor in enumerate(robo.sensores_simulados):
        cor_sensor = config.COR_VERDE if valor_sensor == 1 else config.COR_CINZA
        pos_x = sensor_x_start + (i * 40) # 30 = tamanho, 10 = espaço
        pygame.draw.rect(surface, cor_sensor, (pos_x, y, 30, 30))
        desenhar_texto(surface, f"{i+1}", (pos_x + 10, y + 35), font_pequena)
    y += 60

    # --- MUDANÇA AQUI: Painel 3 e 4 para Árvores Lado a Lado ---
    pygame.draw.line(surface, config.COR_CINZA, (10, y), (config.TELA_LARGURA_DASHBOARD - 10, y), 2)
    y += 20
    desenhar_texto(surface, "Filas de Pedidos", (10, y), font_titulo, config.COR_AZUL_CLARO)
    y += 40

    # --- Painel 3: Fila de Pedidos (Árvore AVL) ---
    # Metade Esquerda do Painel
    avl_panel_x = config.TELA_LARGURA_DASHBOARD / 4 
    avl_tree_start_y = y + 40
    desenhar_texto(surface, "Árvore AVL", (avl_panel_x - 50, y), font_media, config.COR_BRANCO)
    
    desenhar_avl_tree(surface, cerebro_pi.inventory_tree.root, 
                      avl_panel_x, avl_tree_start_y, 
                      h_spacing=50, v_spacing=50, font=font_pequena) # Espaçamento menor

    # --- Painel 4: Fila de Pedidos (Árvore Red-Black) ---
    # Metade Direita do Painel
    rb_panel_x = (config.TELA_LARGURA_DASHBOARD / 4) * 3
    rb_tree_start_y = y + 40
    desenhar_texto(surface, "Árvore Red-Black", (rb_panel_x - 70, y), font_media, config.COR_BRANCO)


    desenhar_rb_tree(surface, cerebro_pi.rb_tree.root, cerebro_pi.rb_tree.NIL,
                    rb_panel_x, rb_tree_start_y, 
                    h_spacing=50, v_spacing=50, font=font_pequena)