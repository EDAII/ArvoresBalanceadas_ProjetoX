import log_manager 

BLACK = "BLACK"
RED = "RED"

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.color = RED

class RBTree:
    def __init__(self):
        self.NIL = Node(None, None)
        self.NIL.color = BLACK
        self.NIL.left = None
        self.NIL.right = None
        self.NIL.parent = None
        self.root = self.NIL
    
    def _get_parent(self, n):
        if n is None:
            return None
        return n.parent
    
    def _get_grandparent(self, n):
        return self._get_parent(self._get_parent(n))
    
    def _get_sibling(self, n):
        p = self._get_parent(n)
        if p is None:
            return None
        
        if n != self.NIL:
            if n == p.left:
                return p.right
            else:
                return p.left
        
        if hasattr(n, '_temp_is_left'):
            if n._temp_is_left:
                return p.right
            else:
                return p.left
        
        if p.left == self.NIL and p.right != self.NIL:
            return p.right
        elif p.right == self.NIL and p.left != self.NIL:
            return p.left
        else:
            return None
    
    def _get_uncle(self, n):
        p = self._get_parent(n)
        return self._get_sibling(p)
    
    def _rotate_left(self, n):
        nnew = n.right
        p = self._get_parent(n)
        assert nnew != self.NIL
        
        n.right = nnew.left
        nnew.left = n
        n.parent = nnew
        
        if n.right != self.NIL:
            n.right.parent = n
        
        if p is not None:
            if n == p.left:
                p.left = nnew
            elif n == p.right:
                p.right = nnew
        nnew.parent = p
        
        if self.root == n:
            self.root = nnew
    
    def _rotate_right(self, n):
        nnew = n.left
        p = self._get_parent(n)
        assert nnew != self.NIL
        
        n.left = nnew.right
        nnew.right = n
        n.parent = nnew
        
        if n.left != self.NIL:
            n.left.parent = n
        
        if p is not None:
            if n == p.left:
                p.left = nnew
            elif n == p.right:
                p.right = nnew
        nnew.parent = p
        
        if self.root == n:
            self.root = nnew

    def insert(self, key, value):
        log_manager.add_log(f"RB: Inserindo pedido {key}...")
        
        n = Node(key, value)
        n.left = self.NIL
        n.right = self.NIL
        n.color = RED
        n.parent = None
        
        if self.root == self.NIL:
            self.root = n
            n.color = BLACK
            return
        
        self._insert_recurse(self.root, n)
        
        self._insert_repair_tree(n)
        
        root = n
        while self._get_parent(root) is not None:
            root = self._get_parent(root)
        self.root = root
    
    def _insert_recurse(self, root, n):
        if n.key < root.key:
            if root.left != self.NIL:
                self._insert_recurse(root.left, n)
            else:
                root.left = n
                n.parent = root
        else:
            if root.right != self.NIL:
                self._insert_recurse(root.right, n)
            else:
                root.right = n
                n.parent = root
    
    def _insert_repair_tree(self, n):
        if self._get_parent(n) is None:
            self._insert_case1(n)
        elif self._get_parent(n).color == BLACK:
            self._insert_case2(n)
        elif self._get_uncle(n) is not None and self._get_uncle(n) != self.NIL and self._get_uncle(n).color == RED:
            self._insert_case3(n)
        else:
            self._insert_case4(n)
    
    def _insert_case1(self, n):
        if self._get_parent(n) is None:
            n.color = BLACK
            log_manager.add_log(f"RB: Caso 1 - Nó {n.key} é raiz, pintado de preto")
    
    def _insert_case2(self, n):
        return
    
    def _insert_case3(self, n):
        log_manager.add_log(f"RB: Caso 3 - Recoloração no nó {n.key}")
        self._get_parent(n).color = BLACK
        self._get_uncle(n).color = BLACK
        g = self._get_grandparent(n)
        g.color = RED
        self._insert_repair_tree(g)
    
    def _insert_case4(self, n):
        p = self._get_parent(n)
        g = self._get_grandparent(n)
        
        if g is not None:
            if n == p.right and p == g.left:
                log_manager.add_log(f"RB: Caso 4 - Rotação esquerda no nó {p.key}")
                self._rotate_left(p)
                n = n.left
            elif n == p.left and p == g.right:
                log_manager.add_log(f"RB: Caso 4 - Rotação direita no nó {p.key}")
                self._rotate_right(p)
                n = n.right
        
        self._insert_case5(n)
    
    def _insert_case5(self, n):
        p = self._get_parent(n)
        g = self._get_grandparent(n)
        
        if g is not None:
            if n == p.left:
                log_manager.add_log(f"RB: Caso 5 - Rotação direita no nó {g.key}")
                self._rotate_right(g)
            else:
                log_manager.add_log(f"RB: Caso 5 - Rotação esquerda no nó {g.key}")
                self._rotate_left(g)
            
            p.color = BLACK
            g.color = RED

    def delete(self, key):
        log_manager.add_log(f"RB: Removendo pedido {key}...")
        n = self._search_tree(self.root, key)
        
        if n == self.NIL:
            log_manager.add_log(f"RB: Pedido {key} não encontrado")
            return
        
        if n.left != self.NIL and n.right != self.NIL:
            successor = self._get_min_value_node(n.right)
            n.key = successor.key
            n.value = successor.value
            n = successor
        
        self._delete_one_child(n)
        
        self.root.color = BLACK
    
    def _replace_node(self, n, child):
        if n.parent is None:
            self.root = child
            child.parent = None
        else:
            if n == n.parent.left:
                n.parent.left = child
            else:
                n.parent.right = child
            child.parent = n.parent
    
    def _delete_one_child(self, n):
        child = n.right if n.left == self.NIL else n.left
        
        if n.parent is not None:
            is_left_child = (n == n.parent.left)
        else:
            is_left_child = None
        
        self._replace_node(n, child)
        
        if child == self.NIL and is_left_child is not None:
            child._temp_is_left = is_left_child
        
        if n.color == RED:
            if hasattr(child, '_temp_is_left'):
                delattr(child, '_temp_is_left')
            return
        
        if child.color == RED:
            child.color = BLACK
            if hasattr(child, '_temp_is_left'):
                delattr(child, '_temp_is_left')
            return
        
        self._delete_case1(child)
        
        if hasattr(child, '_temp_is_left'):
            delattr(child, '_temp_is_left')

    def _delete_case1(self, n):
        if n.parent is not None:
            self._delete_case2(n)
    
    def _delete_case2(self, n):
        s = self._get_sibling(n)
        
        if s is not None and s != self.NIL and s.color == RED:
            log_manager.add_log(f"RB: Delete Caso 2 - Irmão vermelho")
            n.parent.color = RED
            s.color = BLACK
            if n == n.parent.left:
                self._rotate_left(n.parent)
            else:
                self._rotate_right(n.parent)
        
        self._delete_case3(n)
    
    def _delete_case3(self, n):
        s = self._get_sibling(n)
        
        if s is not None and s != self.NIL:
            if (n.parent.color == BLACK and
                s.color == BLACK and
                (s.left == self.NIL or s.left.color == BLACK) and
                (s.right == self.NIL or s.right.color == BLACK)):
                log_manager.add_log(f"RB: Delete Caso 3 - Todos pretos")
                s.color = RED
                self._delete_case1(n.parent)
            else:
                self._delete_case4(n)
        else:
            self._delete_case4(n)
    
    def _delete_case4(self, n):
        s = self._get_sibling(n)
        
        if s is not None and s != self.NIL:
            if (n.parent.color == RED and
                s.color == BLACK and
                (s.left == self.NIL or s.left.color == BLACK) and
                (s.right == self.NIL or s.right.color == BLACK)):
                log_manager.add_log(f"RB: Delete Caso 4 - Pai vermelho")
                s.color = RED
                n.parent.color = BLACK
            else:
                self._delete_case5(n)
        else:
            self._delete_case5(n)
    
    def _delete_case5(self, n):
        s = self._get_sibling(n)
        
        if s is not None and s != self.NIL and s.color == BLACK:
            if (n == n.parent.left and
                (s.right == self.NIL or s.right.color == BLACK) and
                s.left != self.NIL and s.left.color == RED):
                log_manager.add_log(f"RB: Delete Caso 5 - Rotação no irmão")
                s.color = RED
                s.left.color = BLACK
                self._rotate_right(s)
            elif (n == n.parent.right and
                  (s.left == self.NIL or s.left.color == BLACK) and
                  s.right != self.NIL and s.right.color == RED):
                log_manager.add_log(f"RB: Delete Caso 5 - Rotação no irmão")
                s.color = RED
                s.right.color = BLACK
                self._rotate_left(s)
        
        self._delete_case6(n)
    
    def _delete_case6(self, n):
        s = self._get_sibling(n)
        
        if s is not None and s != self.NIL:
            log_manager.add_log(f"RB: Delete Caso 6 - Rotação final")
            s.color = n.parent.color
            n.parent.color = BLACK
            
            if n == n.parent.left:
                if s.right != self.NIL:
                    s.right.color = BLACK
                self._rotate_left(n.parent)
            else:
                if s.left != self.NIL:
                    s.left.color = BLACK
                self._rotate_right(n.parent)

    def get_min_node(self):
        return self._get_min_value_node(self.root)
    
    def _get_min_value_node(self, node):
        if node == self.NIL:
            return None
        while node.left != self.NIL:
            node = node.left
        return node
    
    def _search_tree(self, node, key):
        if node == self.NIL or key == node.key:
            return node
        
        if key < node.key:
            return self._search_tree(node.left, key)
        return self._search_tree(node.right, key)
    
    def _transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent
    
    def _left_rotate(self, x):
        self._rotate_left(x)
    
    def _right_rotate(self, y):
        self._rotate_right(y)