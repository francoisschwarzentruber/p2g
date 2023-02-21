import re
from collections import OrderedDict
import os

class Proof:
	def __init__(self):
		self.nodes = OrderedDict()
		self.edges = []

	def addStatement(self, id, statement):
		self.nodes[id] = statement.strip()

	def addProof(self, id, proof):
		self.nodes[id] = proof

	def addEdge(self, id1, id2):
		self.edges.append((id1, id2))

	def toDot(self):
		lines = []
		for key, value in self.nodes.items():
			if isinstance(value, Proof):
				l = value.toDot()
				lines.append(l)
			else:
				lines.append(f'{key}  [label="\\text{{{value}}}"];')
		return "\n".join(lines)

nextId = 0
def generateId():
	global nextId
	nextId += 1
	return nextId


def linesToProof(lines):
	proof = Proof()
	reStatementBy = re.compile(r'(.*)by\s\((\w*)\)')
	reStatementId = re.compile(r'(.*)\((\w*)\)')
	reStatementById = re.compile(r'(.*)by\s\((\w*)\)\s*\((\w*)\)')

	while(len(lines) > 0):
		line = lines[0][0:len(lines[0])-1]
		lines.pop(0)
		print(line)
		
		if line == "{":
			proof.addProof("a", linesToProof(lines))
		elif line == "}":
			return proof
		else:
			result = re.match(reStatementById, line)
			if result:
				id = result.groups()[2]
				statement = result.groups()[0]
				proof.addStatement(id, statement )

				for byid in by.split(','):
						proof.addEdge(byid, id)
			else:
				result = re.match(reStatementBy, line)

				if result:
					id = generateId()
					by = result.groups()[1]
					statement = result.groups()[0]
					proof.addStatement(id, statement)
					for byid in by.split(','):
						proof.addEdge(byid, id)
				else:
					result = re.match(reStatementId, line)
					if result:
						id = result.groups()[1]
						statement = result.groups()[0]
						proof.addStatement(id, statement)

		

	return proof

def toTex(innerDot):
	f = open("skeleton.tex", "r")
	lines = f.readlines()
	str = ""

	for line in lines:
		if line.strip() == "GRAPHVIZCODE":
			str += innerDot
		str += line
	return str

f = open("sqrt2irrational.proof", "r")
lines = f.readlines()
proof = linesToProof(lines)
innerDot = proof.toDot()
texCode = toTex(innerDot)
out = open("miaou.tex", "w")
out.writelines(texCode)


os.system("pdflatex --shell-escape miaou.tex")