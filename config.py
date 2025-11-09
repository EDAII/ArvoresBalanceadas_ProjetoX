import pygame

# CONFIGURAÇÃO DA TELA
TELA_LARGURA_PEDIDOS = 520  # <-- MUDANÇA (era 300)
TELA_LARGURA_MUNDO = 800
TELA_LARGURA_DASHBOARD = 450  # <-- MUDANÇA (era 400)
TELA_ALTURA = 900           # <-- MUDANÇA (era 1050)

# --- MUDANÇA AQUI ---
# Nova largura total = 350 + 800 + 450 = 1600
TELA_LARGURA_TOTAL = TELA_LARGURA_PEDIDOS + TELA_LARGURA_MUNDO + TELA_LARGURA_DASHBOARD

# CORES (R, G, B)
COR_PRETO = (20, 20, 20)
COR_BRANCO = (230, 230, 230)
COR_CINZA = (100, 100, 100)
COR_CINZA_CLARO = (40, 40, 40)
COR_LINHA = (50, 50, 50) # Fundo da linha
COR_LINHA_CENTRO = (255, 255, 0) # Linha amarela que o robô segue
COR_VERMELHO = (255, 80, 80)
COR_VERDE = (80, 255, 80)
COR_AZUL = (80, 80, 255)
COR_AZUL_CLARO = (100, 150, 255)

# CONFIGURAÇÃO DO ROBÔ
ROBO_TAMANHO = 40
ROBO_VELOCIDADE = 3.0 # pixels por frame

# --- O MAPA DO ARMAZÉM ---
# (Mapa 4x4)

# 1. Posições dos Nós na tela (em pixels)
#    (x, y) - Uma grade 4x4
#    (Ajustado para a nova altura de 900px)
POSICOES_NOS = {
    # Linha 1
    'A': (100, 100), 'B': (300, 100), 'C': (500, 100), 'D': (700, 100),
    # Linha 2
    'E': (100, 300), 'F': (300, 300), 'G': (500, 300), 'H': (700, 300),
    # Linha 3
    'I': (100, 500), 'J': (300, 500), 'K': (500, 500), 'L': (700, 500),
    # Linha 4
    'M': (100, 700), 'N': (300, 700), 'O': (500, 700), 'P': (700, 700),
}

# 2. Conexões do Grafo e suas distâncias (pesos)
#    Distância H: 200px, Distância V: 200px
MAPA_GRAFO = {
    'A': {'B': 200, 'E': 200},
    'B': {'A': 200, 'C': 200, 'F': 200},
    'C': {'B': 200, 'D': 200, 'G': 200},
    'D': {'C': 200, 'H': 200},
    
    'E': {'A': 200, 'F': 200, 'I': 200},
    'F': {'B': 200, 'E': 200, 'G': 200, 'J': 200},
    'G': {'C': 200, 'F': 200, 'H': 200, 'K': 200},
    'H': {'D': 200, 'G': 200, 'L': 200},
    
    'I': {'E': 200, 'J': 200, 'M': 200},
    'J': {'F': 200, 'I': 200, 'K': 200, 'N': 200},
    'K': {'G': 200, 'J': 200, 'L': 200, 'O': 200},
    'L': {'H': 200, 'K': 200, 'P': 200},
    
    'M': {'I': 200, 'N': 200},
    'N': {'J': 200, 'M': 200, 'O': 200},
    'O': {'K': 200, 'N': 200, 'P': 200},
    'P': {'L': 200, 'O': 200},
}