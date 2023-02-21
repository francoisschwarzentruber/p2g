import re
from collections import OrderedDict
import os

class Proof:
	def __init__(self, isWithHook = False):
		self.nodes = OrderedDict()
		if isWithHook:
			idHook = generateId()
			self.nodes[idHook] = ""
		self.edges = []
		self.edgesProofOf = []
		self.lastid = None
		

	def addStatement(self, id, statement):
		self.nodes[id] = statement.strip()
		if self.lastid != None:
			self.addEdge(self.lastid, id)
		self.lastid = id


	def addProof(self, id, proof):
		if self.lastid != None:
			proofnodeid = next(iter(proof.nodes))
			self.edgesProofOf.append(("cluster_" + str(id), proofnodeid, self.lastid))
			
		self.nodes[id] = proof
		self.lastid = None

	def addEdge(self, id1, id2):
		self.edges.append((id1, id2))

	def toDot(self):
		lines = []
		for key, value in self.nodes.items():
			if isinstance(value, Proof):
				l = value.toDot()
				lines.append(f"subgraph cluster_{key} {{")
				lines.append(l)
				lines.append("color=blue")
				lines.append("}")
			elif value == "":
				lines.append(f'{key}  [label="" color="blue"];')
			else:
				lines.append(f'{key}  [label="\\text{{{value}}}"  shape=none];')

		for (id1, id2) in self.edges:
			lines.append(f'{id1} -> {id2};')

		for (idcluster1, id1, id2) in self.edgesProofOf:
			lines.append(f'{id2} -> {id1} [lhead="{idcluster1}",dir=none color="blue",style="dashed"];')

		return "\n".join(lines)

nextId = 0
def generateId():
	global nextId
	nextId += 1
	return str(nextId)



reStatementBy = re.compile(r'(.*)by\s\(((\w|,)*)\)')
reStatementId = re.compile(r'(.*)\((\w*)\)')
reStatementById = re.compile(r'(.*)by\s\(((\w|,)*)\)\s*\((\w*)\)')
print(re.match(reStatementBy, "Contradiction        by (irreducible,aeven,beven)").groups())
print(re.match(reStatementById, "azeazeaze by (miaou)   (id)  ").groups())
print(re.match(reStatementId, "Lemma. $a^2$ even implies $a$ even.            (lemma)  ").groups())


def linesToProof(lines, depth = 0):
	proof = Proof(depth > 0)
	while(len(lines) > 0):
		line = lines[0][0:len(lines[0])-1].strip()
		lines.pop(0)
		
		if line == "":
			pass
		
		print(line)
		if line == "{":
			proof.addProof(generateId(), linesToProof(lines, depth+1))
		elif line == "}":
			return proof
		else:

			def extractInfo(line):
				result = re.match(reStatementById, line)
				if result:
					return result.groups()[0], result.groups()[3], result.groups()[1]
				else:
					result = re.match(reStatementBy, line)
					if result:
						return result.groups()[0], generateId(), result.groups()[1]
					else: 
						result = re.match(reStatementId, line)
						if result:
							return result.groups()[0], result.groups()[1], []
						else:
							return line, generateId(), None

			statement, id, by = extractInfo(line)
			
			proof.addStatement(id, statement )

			if by:
				for byid in by.split(','):
					proof.addEdge(byid, id)
			

	return proof

def toTex(innerDot):
	f = open("skeleton.tex", "r")
	lines = f.readlines()
	return "".join(map(lambda line: innerDot if line.strip() == "GRAPHVIZCODE" else line, lines))
	
inputFile = open("sqrt2irrational.proof", "r")
lines = inputFile.readlines()
inputFile.close()
proof = linesToProof(lines)
innerDot = proof.toDot()
texCode = toTex(innerDot)
outputFile = open("out.tex", "w")
outputFile.writelines(texCode)
outputFile.close()
os.system("pdflatex --shell-escape out.tex")