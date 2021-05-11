from collections import defaultdict

class Node:
	def __init__(self, charSet='', frequency=0):
		assert(isinstance(charSet, str))
		assert(isinstance(frequency, int))
		assert(frequency >= 0)

		self.charSet = charSet
		self.frequency = frequency
		self.left = None
		self.right = None

	@classmethod
	def fromNodes(cls, leftNode, rightNode):
		assert(isinstance(leftNode, Node))
		assert(isinstance(rightNode, Node))

		parentCharSet = leftNode.charSet+rightNode.charSet
		parentFrequency = leftNode.frequency+rightNode.frequency
		parentNode = cls(parentCharSet, parentFrequency)
		parentNode.left = leftNode
		parentNode.right = rightNode
		return parentNode

	def __add__(self, other):
		if (isinstance(other, int)):
			return self.frequency + other
		elif (isinstance(other, Node)):
			return self.frequency + other.frequency

	def __lt__(self, other):
		return self.frequency < other.frequency

	def __contains__(self, other):
		return other in self.charSet

	def __str__(self, paddingAll='', ptr=''):
		if not self.left and not self.right:
			return ptr + self.__repr__() + '\n'
		outputString = ptr + str(self.frequency) + '\n'
		outputString += paddingAll + self.left.__str__(paddingAll + '│  ', '├──')
		outputString += paddingAll + self.right.__str__(paddingAll + '   ', '└──')
		return outputString

	def __repr__(self):
		return '({}, {})'.format(self.charSet, self.frequency)


class HuffmanTree:
	def __init__(self, text):
		assert(isinstance(text, str))
		self.text = text
		self.root = Node()
		self.constructTree()

	def constructTree(self):
		charFrequencies = defaultdict(int)
		for char in self.text:
			charFrequencies[char] += 1
		nodes = [Node(pair[0], pair[1]) for pair in sorted(charFrequencies.items(), key=lambda item: item[1])]

		while len(nodes) > 1:
			combinedNode = Node.fromNodes(nodes[0], nodes[1])
			nodes.append(combinedNode)
			nodes.pop(0)
			nodes.pop(0)
			nodes = sorted(nodes)

		self.root = nodes[0]

	def getEncoded(self, text):
		assert(isinstance(text, str))

		for char in text:
			yield self.getCharEncoding(char)

	def getCharEncoding(self, char):
		assert(isinstance(char, str))

		node = self.root
		encoding = []
		while True:
			if char in node and len(node.charSet)==1:
				return encoding
			elif char in node.left:
				encoding.append(0)
				node = node.left
			elif char in node.right:
				encoding.append(1)
				node = node.right

	def getDecoded(self, bits):
		assert(isinstance(bits, list))

		node = self.root
		offset = 0
		while offset != len(bits):
			if bits[offset] == 0:
				node = node.left
				offset += 1
			elif bits[offset] == 1:
				node = node.right
				offset += 1
			else:
				break

			if len(node.charSet) == 1:
				yield node.charSet[0]
				node = self.root

	def __str__(self):
		return self.root.__str__()