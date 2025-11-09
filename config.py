import pygame

# CONFIGURAÇÃO DA TELA
TELA_LARGURA_PEDIDOS = 300  # <-- NOVO PAINEL
TELA_LARGURA_MUNDO = 800
TELA_LARGURA_DASHBOARD = 400
TELA_ALTURA = 1050

# --- MUDANÇA AQUI ---
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
# (Mapa 3x3)
POSICOES_NOS = {
    'A': (100, 100), 'B': (400, 100), 'C': (700, 100),
    'D': (100, 400), 'E': (400, 400), 'F': (700, 400),
    'G': (100, 700), 'H': (400, 700), 'I': (700, 700),
}

MAPA_GRAFO = {
    'A': {'B': 300, 'D': 300},
    'B': {'A': 300, 'C': 300, 'E': 300},
    'C': {'B': 300, 'F': 300},
    'D': {'A': 300, 'E': 300, 'G': 300},
    'E': {'B': 300, 'D': 300, 'F': 300, 'H': 300},
    'F': {'C': 300, 'E': 300, 'I': 300},
    'G': {'D': 300, 'H': 300},
    'H': {'E': 300, 'G': 300, 'I': 300},
    'I': {'F': 300, 'H': 300},
}