# Basado en la implementacion Treap de GeeksforGeeks
# https://www.geeksforgeeks.org/implementation-of-search-insert-and-delete-in-treap/

import random 

class Treap:
	def __init__(self, elems = []):
		self.root = None
		for i in range(len(elems)):
			self.insert(elems[i], i)

	def insert(self, key, pos):
		self.root = insert(self.root, key, pos)

	def delete(self, pos):
		self.root = deleteNode(self.root, pos)

	def get(self, pos):
		return get(self.root, pos)

	def inorder(self):
		inorder(self.root)

	def multiSwap(self, a, b):
		# Se divide el treap en 5 partes
		# [0.. a-1],
		# [a.. a+length-1],
		# [a+length.. b-1], 
		# [b.. b+length-1],
		# [b+length.. N-1]
		length = min(b-a, len(self)-b)

		# Se divide en [0.. a-1], [a.. N-1]
		start, end = self.root.split(a)

		# Se divide en [a.. a+length-1], [b.. N-1]
		partA, end = end.split(length)

		# Se divide en [a+length.. b-1], [b.. N-1]
		mid, end = end.split(b-a-length)
		
		# Se divide en [b.. b+length-1], [b+length.. N-1]
		partB, end = end.split(length)

		# Se unen las partes en el orden correcto
		self.root = merge(
			merge(
				merge(start, partB),
				merge(mid, partA)
			),
			end
		)

		
		return self.root
	
	def __len__(self):
		return size(self.root)

	def __iter__(self):
		return self.root.__iter__()

class TreapNode:
	def __init__(self, value):
		self.value = value
		self.priority = random.randint(0, 99)
		self.left = None
		self.right = None
		self.size = 1

	def split(self, pos):
		return split(self, pos)
	

	def __iter__(self):
		if self.left:
			yield from self.left.__iter__()
		yield self.value
		if self.right:
			yield from self.right.__iter__()

# Se actualiza el tamaño del subarbol cada vez que se inserta o elimina un nodo
def updateSize(node):
	if node:
		node.size = 1 + size(node.left) + size(node.right)

def size(node):
	return node.size if node else 0

# Ejemplo del sitio web de GeeksforGeeks para el rightRotate y leftRotate
# T1, T2 and T3 are subtrees of the tree rooted with y
# (on left side) or x (on right side)
#			 y							 x
#			 / \	 Right Rotation		 / \
#			x   T3    – – – – – – – >	T1  y
#		   / \     	 < - - - - - - -	   / \
#		  T1  T2	 	Left Rotation 	  T2 T3 */
def rightRotate(y):
	x = y.left
	T2 = x.right
	
	x.right = y
	y.left = T2
	
	updateSize(y)
	updateSize(x)
	
	return x
	
def leftRotate(x):
	y = x.right
	T2 = y.left
	
	y.left = x
	x.right = T2
	
	updateSize(x)
	updateSize(y)
	
	return y

def insert(root, key, pos):
	# Caso base
	if not root:
		return TreapNode(key)
	
	# Se inserta en el subarbol derecho si la posicion es mayor,
	# el tamaño del subarbol izquierdo nos da la posicion relativa, esta
	# se resta del indice para obtener la posicion relativa en el subarbol derecho
	if size(root.left) < pos:
		root.right = insert(root.right, key, pos - size(root.left) - 1)

		# Rotacion de ser necesario para respetar el min heap
		if root.right and root.right.priority < root.priority:
			root = leftRotate(root)

	# Se inserta en el subarbol izquierdo si la posicion es menor o igual
	else:
		root.left = insert(root.left, key, pos)
		if root.left and root.left.priority > root.priority:
			root = rightRotate(root)
	
	updateSize(root)
	return root

def deleteNode(root, pos):
	# Caso base
	if not root:
		return root
	
	# Se elimina del subarbol derecho si la posicion es mayor
	if size(root.left) < pos:
		root.right = deleteNode(root.right, pos - size(root.left) - 1)
		if root.right and root.left and root.left.priority < root.right.priority:
			root = leftRotate(root)

	# Se elimina del subarbol izquierdo si la posicion es menor
	elif size(root.left) > pos:
			root.left = deleteNode(root.left, pos)
			if root.right and root.left and root.right.priority < root.left.priority:
				root = rightRotate(root)

	# Si la posicion es igual, se elimina y reemplaza por alguno de sus hijos
	else:
		# Si tiene un solo hijo o ninguno
		if not root.left or not root.right:
			root = root.left if root.left else root.right

		# Sino, se reemplaza por el hijo con prioridad mas baja
		elif root.left.priority > root.right.priority:
			root = leftRotate(root)
			root.left = deleteNode(root.left, pos)
		else:
			root = rightRotate(root)
			root.right = deleteNode(root.right, pos - size(root.left) - 1)
	
	updateSize(root)
	return root

# Se realiza busqueda binaria por indice
def get(root, pos):
	if not root:
		return None
	
	if size(root.left) < pos:
		return get(root.right, pos - size(root.left) - 1)
	elif size(root.left) > pos:
		return get(root.left, pos)
	else:
		return root

def inorder(root):
	if root:
		inorder(root.left)
		print("value:", root.value, "| priority:", root.priority, "| size:", root.size)
		inorder(root.right)

def split(root, pos):
	if not root:
		return None, None
	
	# Si la posicion es mayor, se busca donde dividir el subarbol derecho
	if size(root.left) < pos:
		left, right = split(root.right, pos - size(root.left) - 1)
		root.right = left
		updateSize(root)
		return root, right
	
	# Si la posicion es menor o igual, se busca donde dividir el subarbol izquierdo
	else:
		left, right = split(root.left, pos)
		root.left = right
		updateSize(root)
		return left, root

def merge(left, right):
	# Casos base
	if not left or not right:
		return left if left else right
	
	# Se elige el subarbol con menor prioridad como raiz
	if left.priority < right.priority:
		left.right = merge(left.right, right)
		updateSize(left)
		return left
	else:
		right.left = merge(left, right.left)
		updateSize(right)
		return right


if __name__ == '__main__':
	random.seed(0)

	treap = Treap([50, 30, 20, 40, 70, 60, 80])

	# treap.insert(50, 0)
	# treap.insert(30, 1)
	# treap.insert(20, 2)
	# treap.insert(40, 3)
	# treap.insert(70, 4)
	# treap.insert(60, 5)
	# treap.insert(80, 6)

	print("Inorder traversal of the given tree")
	treap.inorder()
	
	print("\nDelete 2")
	treap.delete(2)
	print("Inorder traversal of the modified tree")
	treap.inorder()

	print("\nDelete 1")
	treap.delete(1)
	print("Inorder traversal of the modified tree")
	treap.inorder()

	print("\nDelete 0")
	treap.delete(0)
	print("Inorder traversal of the modified tree")
	treap.inorder()

	res = treap.get(0)
	if res is None:
		print("0 Not Found")
	else:
		print("0 found, value:", res.value)

	print(list(treap))