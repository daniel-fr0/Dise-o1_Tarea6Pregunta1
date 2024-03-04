from Treap import *


def multiplesMultiSwaps(A, swaps):
	treap = Treap(A)
	for a, b in swaps:
		treap.multiSwap(a, b)	
	return list(treap)


if __name__ == "__main__":
	# indices de los multiswaps a realizar
	swaps = [(1, 2), (2, 3), (1, 3), (1, 2), (2, 3), (1, 3), (0, 6), (1, 1), (0,1), (6,7)]

	# lista de elementos
	lista = list(range(8))

	print(multiplesMultiSwaps(lista, swaps))