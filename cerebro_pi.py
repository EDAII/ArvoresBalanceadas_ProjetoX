from astar import AStar, find_path
import config
import math

class CerebroPi(AStar):
    """
    Simula o 'Raspberry Pi' (cérebro de alto nível).
    Conhece o mapa, calcula rotas (A*) e gerencia a máquina de estados.
    Herda de AStar para usar os métodos de pathfinding.
    """
    def __init__(self, mapa_grafo, posicoes_nos):
        self.mapa = mapa_grafo
        self.posicoes_nos = posicoes_nos
        
        # Máquina de Estados do "Pi"
        self.status = "PARADO" # PARADO, NAVEGANDO, ERRO
        self.no_atual = 'A'
        self.no_destino = None
        self.rota_calculada = [] # Lista de nós (ex: ['A', 'B', 'D'])
        self.proximo_no = None

    def neighbors(self, node):
        """ Método obrigatório do A* (retorna vizinhos) """
        return self.mapa.get(node, {}).keys()

    def distance_between(self, n1, n2):
        """ Método obrigatório do A* (retorna distância/peso) """
        return self.mapa.get(n1, {}).get(n2, float('inf'))

    def heuristic_cost_estimate(self, n1, n2):
        """ Método obrigatório do A* (heurística - distância em linha reta) """
        pos1 = self.posicoes_nos[n1]
        pos2 = self.posicoes_nos[n2]
        return math.dist(pos1, pos2)
    
    def pedir_rota(self, no_destino_final):
        """
        Ponto de entrada. Chamado pelo usuário (ex: clique do mouse).
        Calcula a rota A* e retorna o primeiro comando para o robô.
        """
        if self.status == "NAVEGANDO":
            print("Cérebro (Pi): Ignorando novo pedido, já estou navegando.")
            return None # Já está ocupado
            
        if no_destino_final not in self.mapa:
            print(f"Cérebro (Pi): Erro - Nó '{no_destino_final}' não existe.")
            self.status = "ERRO"
            return None

        if self.no_atual == no_destino_final:
            print(f"Cérebro (Pi): Já estamos em '{no_destino_final}'.")
            self.status = "PARADO"
            return None

        print(f"Cérebro (Pi): Calculando rota de {self.no_atual} para {no_destino_final}...")
        
        # Roda o A*
        caminho_iter = find_path(self.no_atual, no_destino_final, neighbors_fnct=self.neighbors, distance_between_fnct=self.distance_between, heuristic_cost_estimate_fnct=self.heuristic_cost_estimate)
        if caminho_iter:
            self.rota_calculada = list(caminho_iter)
            self.no_destino = no_destino_final
            self.status = "NAVEGANDO"
            
            # ANTES de modificar a lista, guarde a rota completa para o log
            rota_para_log = list(self.rota_calculada)

            # Remove o nó atual da rota e pega o próximo
            self.rota_calculada.pop(0) # Remove o self.no_atual
            self.proximo_no = self.rota_calculada.pop(0) # Pega o próximo destino

            print(f"Cérebro (Pi): Rota: {' -> '.join(rota_para_log)}")
            print(f"Cérebro (Pi): Enviando Robô para {self.proximo_no}")
            
            # Retorna o primeiro comando para o "Arduino"
            pos_alvo = self.posicoes_nos[self.proximo_no]
            return ("FRENTE", pos_alvo)
        else:
            print(f"Cérebro (Pi): Erro - Rota de {self.no_atual} para {no_destino_final} não encontrada.")
            self.status = "ERRO"
            return None

    def reportar_chegada_no(self):
        """
        O "Arduino" (Robo) chama esta função quando reporta 'CHEGUEI_INTERSECAO'.
        O "Pi" decide o que fazer a seguir.
        """
        self.no_atual = self.proximo_no
        self.proximo_no = None
        
        if self.no_atual == self.no_destino:
            # Tarefa Concluída!
            print(f"Cérebro (Pi): Chegamos ao destino final {self.no_destino}!")
            self.status = "PARADO"
            self.rota_calculada = []
            self.no_destino = None
            return None # Sem próximo comando
        
        if not self.rota_calculada:
            # Isso não deveria acontecer se o status for NAVEGANDO
            print(f"Cérebro (Pi): Erro - Cheguei em {self.no_atual} mas a rota está vazia.")
            self.status = "ERRO"
            return None
        
        # Pega o próximo nó da rota
        self.proximo_no = self.rota_calculada.pop(0)
        print(f"Cérebro (Pi): Chegou em {self.no_atual}. Enviando Robô para {self.proximo_no}")
        
        pos_alvo = self.posicoes_nos[self.proximo_no]
        return ("FRENTE", pos_alvo)