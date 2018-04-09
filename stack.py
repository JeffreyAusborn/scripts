class Stack:

	def __init__(self):
		self.items = []

	def isEmpty(Self):
		return self.items == []

	def push(self, top):
		self.items.append(top)

	def pop(self):
		return self.items.pop()

	def size(self):
		return len(self.items)

	def peek(self):
		return self.items[len(self.items)-1]

	def contents(self):
		return self.items