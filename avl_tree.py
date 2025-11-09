# --- ARQUIVO MODIFICADO: avl_tree.py ---

class Node:
    """ Um nó em uma Árvore AVL """
    def __init__(self, key, value):
        self.key = key      # ID do pacote (a chave de ordenação)
        self.value = value  # Localização (ex: 'A', 'B')
        self.left = None
        self.right = None
        self.height = 1     # Altura do nó (folhas têm altura 1)

class AVLTree:
    """ A classe da Árvore AVL """
    def __init__(self):
        self.root = None

    # --- INSERÇÃO (Existente) ---
    def insert(self, key, value):
        print(f"AVL: Inserindo pedido {key}...")
        self.root = self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        if not node:
            return Node(key, value)
        elif key < node.key:
            node.left = self._insert(node.left, key, value)
        else:
            node.right = self._insert(node.right, key, value)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)

        if balance > 1 and key < node.left.key:
            print(f"AVL: Rotação LL no nó {node.key}")
            return self._right_rotate(node)
        if balance < -1 and key > node.right.key:
            print(f"AVL: Rotação RR no nó {node.key}")
            return self._left_rotate(node)
        if balance > 1 and key > node.left.key:
            print(f"AVL: Rotação LR no nó {node.key}")
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        if balance < -1 and key < node.right.key:
            print(f"AVL: Rotação RL no nó {node.key}")
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)
        return node

    # --- REMOÇÃO (Nova) ---
    def delete(self, key):
        print(f"AVL: Removendo pedido {key}...")
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if not node:
            return node

        # 1. Encontrar e deletar o nó
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Nó encontrado! Hora de deletar.
            # Caso 1: Nó com 0 ou 1 filho
            if node.left is None:
                temp = node.right
                node = None
                return temp
            elif node.right is None:
                temp = node.left
                node = None
                return temp
            
            # Caso 2: Nó com 2 filhos
            # Encontra o sucessor in-order (menor da sub-árvore direita)
            temp = self._get_min_value_node(node.right)
            node.key = temp.key
            node.value = temp.value
            node.right = self._delete(node.right, temp.key)

        if node is None:
            return node

        # 2. Atualizar altura
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        
        # 3. Rebalancear
        balance = self._get_balance(node)

        # Rotação LL
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._right_rotate(node)
        # Rotação RR
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._left_rotate(node)
        # Rotação LR
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        # Rotação RL
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    # --- FUNÇÕES AUXILIARES (Modificadas/Novas) ---

    def get_min_node(self):
        """ Retorna o nó com a menor chave (o próximo pedido) """
        return self._get_min_value_node(self.root)

    def _get_min_value_node(self, node):
        if node is None or node.left is None:
            return node
        return self._get_min_value_node(node.left)

    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y