from astar import AStar, find_path
import config
import math
from avl_tree import AVLTree
from rb_tree import RBTree
import log_manager 

class CerebroPi(AStar):
    """
    Simula o 'Raspberry Pi' (cérebro de alto nível).
    Gerencia a fila de pedidos (AVL) e o pathfinding (A*).
    """
    def __init__(self, mapa_grafo, posicoes_nos):
        self.mapa = mapa_grafo
        self.posicoes_nos = posicoes_nos
        
        self.status = "PARADO"
        self.no_atual = 'A'
        self.no_destino = None
        self.rota_calculada = [] 
        self.proximo_no = None
        
        self.inventory_tree = AVLTree()
        self.rb_tree = RBTree()  
        self.active_job_key = None 

    # --- Funções A* ---
    def neighbors(self, node):
        return self.mapa.get(node, {}).keys()

    def distance_between(self, n1, n2):
        return self.mapa.get(n1, {}).get(n2, float('inf'))

    def heuristic_cost_estimate(self, n1, n2):
        pos1 = self.posicoes_nos[n1]
        pos2 = self.posicoes_nos[n2]
        return math.dist(pos1, pos2)
    
    # --- Gerenciamento de Pedidos ---

    def _pedir_rota(self, no_destino_final):
        """
        Função interna. Calcula a rota e define o status de navegação.
        """
        
        if self.no_atual == no_destino_final:
            log_manager.add_log(f"Raspberry: Já estamos em '{no_destino_final}'. Entregando instantaneamente.")
            log_manager.add_log(f"Raspberry: Entregando pacote {self.active_job_key}!")
            self.inventory_tree.delete(self.active_job_key)
            self.rb_tree.delete(self.active_job_key)  
            self.active_job_key = None
            self.status = "PARADO" 
            self.no_destino = None
            return None 

        log_manager.add_log(f"Raspberry: Calculando rota de {self.no_atual} para {no_destino_final}...")
        caminho_iter = find_path(self.no_atual, no_destino_final, 
                                neighbors_fnct=self.neighbors, 
                                distance_between_fnct=self.distance_between, 
                                heuristic_cost_estimate_fnct=self.heuristic_cost_estimate)
        
        if caminho_iter:
            self.rota_calculada = list(caminho_iter)
            rota_para_log = list(self.rota_calculada) 
            self.no_destino = no_destino_final
            self.status = "NAVEGANDO"
            
            self.rota_calculada.pop(0) 
            self.proximo_no = self.rota_calculada.pop(0) 

            log_manager.add_log(f"Raspberry: Rota: {' -> '.join(rota_para_log)}")
            log_manager.add_log(f"Raspberry: Enviando Robô para {self.proximo_no}")
            
            pos_alvo = self.posicoes_nos[self.proximo_no]
            return ("FRENTE", pos_alvo)
        else:
            log_manager.add_log(f"Raspberry: Erro - Rota de {self.no_atual} para {no_destino_final} não encontrada.")
            self.status = "ERRO"
            return None

    def reportar_chegada_no(self):
        """
        O "Arduino" (Robo) reporta 'CHEGUEI_INTERSECAO'.
        O "Pi" decide o que fazer a seguir.
        """
        self.no_atual = self.proximo_no
        self.proximo_no = None
        
        if self.no_atual == self.no_destino:
            # Tarefa Concluída!
            log_manager.add_log(f"Raspberry: Chegamos ao destino final {self.no_destino}!")
            log_manager.add_log(f"Raspberry: Entregando pacote {self.active_job_key}!")
            
            self.inventory_tree.delete(self.active_job_key)
            self.rb_tree.delete(self.active_job_key)  
            self.active_job_key = None
            self.status = "PARADO"
            self.rota_calculada = []
            self.no_destino = None
            
            return None
        
        if not self.rota_calculada:
            self.status = "ERRO"
            return None
        
        self.proximo_no = self.rota_calculada.pop(0)
        log_manager.add_log(f"Raspberry: Chegou em {self.no_atual}. Enviando Robô para {self.proximo_no}")
        
        pos_alvo = self.posicoes_nos[self.proximo_no]
        return ("FRENTE", pos_alvo)

    def add_new_package(self, package_id, location_node):
        """
        Adiciona um novo PEDIDO à fila (Árvores AVL e Red-Black).
        """
        if location_node not in self.mapa:
            log_manager.add_log(f"Raspberry: Ignorando pedido. Localização '{location_node}' não existe.")
            return False

        log_manager.add_log(f"Raspberry: Pedido {package_id} para {location_node} registrado na fila.")
        self.inventory_tree.insert(package_id, location_node)
        self.rb_tree.insert(package_id, location_node)  
        return True

    def check_for_new_job(self):
        """
        Verifica se o robô está parado e se há pedidos na fila.
        Se sim, inicia o próximo pedido (o de menor ID).
        """
        if self.status == "PARADO" and self.inventory_tree.root:
            proximo_pedido = self.inventory_tree.get_min_node()
            
            if proximo_pedido:
                self.active_job_key = proximo_pedido.key
                destino = proximo_pedido.value
                
                log_manager.add_log(f"--- Raspberry: Pegando novo trabalho da fila! ---")
                log_manager.add_log(f"--- Pedido ID: {self.active_job_key}, Destino: {destino} ---")
                
                return self._pedir_rota(destino)
        
        return None