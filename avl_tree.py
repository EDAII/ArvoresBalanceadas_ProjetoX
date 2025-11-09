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

    def insert(self, key, value):
        """ Interface pública para inserir um nó """
        print(f"AVL: Inserindo {key}...")
        self.root = self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        # 1. Inserção normal de Árvore Binária de Busca (BST)
        if not node:
            return Node(key, value)
        elif key < node.key:
            node.left = self._insert(node.left, key, value)
        else:
            node.right = self._insert(node.right, key, value)

        # 2. Atualizar a altura do nó ancestral
        node.height = 1 + max(self._get_height(node.left),
                            self._get_height(node.right))

        # 3. Obter o Fator de Balanço
        balance = self._get_balance(node)
        
        # 4. Se estiver desbalanceado, rebalancear (4 casos)

        # Caso 1: Rotação Simples à Direita (Left-Left)
        if balance > 1 and key < node.left.key:
            print(f"AVL: Rotação LL no nó {node.key}")
            return self._right_rotate(node)

        # Caso 2: Rotação Simples à Esquerda (Right-Right)
        if balance < -1 and key > node.right.key:
            print(f"AVL: Rotação RR no nó {node.key}")
            return self._left_rotate(node)

        # Caso 3: Rotação Dupla Esquerda-Direita (Left-Right)
        if balance > 1 and key > node.left.key:
            print(f"AVL: Rotação LR no nó {node.key}")
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # Caso 4: Rotação Dupla Direita-Esquerda (Right-Left)
        if balance < -1 and key < node.right.key:
            print(f"AVL: Rotação RL no nó {node.key}")
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        # Retorna o nó (potencialmente) novo
        return node

    # --- Funções Auxiliares de Rotação e Balanço ---

    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _left_rotate(self, z):
        # z é o nó desbalanceado
        y = z.right
        T2 = y.left

        # Executa a rotação
        y.left = z
        z.right = T2

        # Atualiza alturas (IMPORTANTE: z primeiro, depois y)
        z.height = 1 + max(self._get_height(z.left),
                            self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left),
                            self._get_height(y.right))

        # Retorna a nova raiz desta sub-árvore
        return y

    def _right_rotate(self, z):
        # z é o nó desbalanceado
        y = z.left
        T3 = y.right

        # Executa a rotação
        y.right = z
        z.left = T3

        # Atualiza alturas (IMPORTANTE: z primeiro, depois y)
        z.height = 1 + max(self._get_height(z.left),
                            self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left),
                            self._get_height(y.right))

        # Retorna a nova raiz desta sub-árvore
        return y