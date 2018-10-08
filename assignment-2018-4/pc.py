from copy import deepcopy
from collections import OrderedDict, ChainMap, deque
from math import inf
from sys import argv

#Directed Acyclic Graph Object Class
class DAG(object):

    #Init Object
    def __init__(self):
        self.init()

    #Add Node in DAG
    def addNode(self, node, graph=None):
        try:
            if graph is None:
                graph = self.graph
            if node in graph:
                raise Exception()
            graph[node] = set()
        except:
            pass

    #Delete Node in DAG
    def delNode(self, node, graph=None):
        if graph is None:
            graph = self.graph
        if node in graph:
            graph.pop(node)
        else:
            pass

    #Add an edge in a node
    def addEdge(self, node, edgeToAdd, graph=None):
        try:
            if graph is None:
                graph = self.graph
            if node not in graph or edgeToAdd not in graph:
                raise Exception()
            graph[node].add(edgeToAdd)
        except:
            pass

    #Delete an edge in a node
    def delEdge(self, node, edgeToDel, graph=None):
        if graph is None:
            graph = self.graph
        if edgeToDel in graph.get(node, []):
            graph[node].remove(edgeToDel)
        else:
            pass

    #Boolean that indicates that a node is in the graph or not
    def inGraph(self, node, graph=None):
        if graph is None:
            graph = self.graph
        if node in graph:
            return True
        return False

    #Print of DAG
    def print(self, graph=None):
        if graph is None:
            graph = self.graph
        for i in graph:
            print(graph[i])

    #Size of DAG
    def size(self):
        return len(self.graph)

    #Init the dictionary
    def init(self):
        self.graph = OrderedDict()


#Bipartite Graph Object Class
class BG(object):

    #Init object
    def __init__(self):
        self.init()

    #Create a Bipartite Graph from a DAG
    def createFromDAG(self, dag):
        for i in dag.graph:
            self.addNodes(i)
        for i in dag.graph:
            list = dag.graph[i]
            for j in list:
                self.addEdge(str(i)+"'", str(j)+"''")

    #Add nodes in graph
    def addNodes(self, node, graph=None):
        if graph is None:
            graph = self.graph
        nodeT = str(node)+"'"
        node2T = str(node)+"''"
        if nodeT not in graph and node2T not in graph:
            graph[nodeT] = set()
            graph[node2T] = set()
        else:
            pass

    #Delete nodes from graph from DAG node
    def delNodes(self, node, graph=None):
        if graph is None:
            graph = self.graph
        nodeT = str(node)+"'"
        node2T = str(node)+"''"
        if nodeT in graph and node2T in graph:
            graph.pop(nodeT)
            graph.pop(node2T)
        else:
            pass

    #Add an edge in the graph
    def addEdge(self, node, edgeToAdd, graph=None):
        if graph is None:
            graph = self.graph
        if node in graph and edgeToAdd in graph:
            graph[node].add(edgeToAdd)
        else:
            pass

    #Delete an edge from the graph
    def delEdge(self, node, edgeToDel, graph=None):
        if graph is None:
            graph = self.graph
        if edgeToDel in graph.get(node, []):
            graph[node].remove(edgeToDel)

    def hopcrofKarp(self, graph=None):
        if graph is None:
            graph = self.graph
        B = set()
        for v in graph:
            if not str.endswith(v, "''"):
                B.add(v)
        M = ChainMap()
        for v in graph:
            M[v] = None
        augmented = True
        while augmented:
            augmented = False
            D = self.BFS(B, M)
            for v in B:
                if M.get(v) is None:
                    temp = self.DFS(v, B, M, D)
                    if temp:
                        augmented = True
        return M

    def BFS(self, B, M, graph=None):
        if graph is None:
            graph = self.graph
        Q = deque()
        D = ChainMap()
        for v in graph:
            if v in B and M.get(v) is None:
                D[v] = 0
                Q.append(v)
            else:
                D[v] = inf
        while len(Q) != 0:
            c = Q.pop()
            for v in graph[c]:
                if D.get(v) == inf:
                    if (c in B and v != M.get(c)) or (c not in B and v == M.get(c)):
                        d = D.get(c) + 1
                        D[v] = d
                        Q.append(v)
        return D

    def DFS(self, s, B, M, D, graph=None):
        if graph is None:
            graph = self.graph
        if s not in B and M.get(s) is None:
            D[s] = inf
            return True
        for v in graph[s]:
            if (s in B and v != M.get(s)) or (s not in B and v == M.get(s)):
                if D.get(v) == (D.get(s)+1):
                    temp = self.DFS(v, B, M, D, graph)
                    if temp:
                        if s in B:
                            M[s] = v
                            M[v] = s
                        return True
        D[s] = inf
        return False

    def getResults(self, graph=None):
        if graph is None:
            graph = self.graph
        map = self.hopcrofKarp(graph)
        res = []
        counter = 0
        for i in graph:
            if not str.endswith(i, "''"):
                node = i
                leaf = map.get(node)
                while True:
                    res.append(node[:-1])
                    if leaf is None:
                        break
                    node = leaf[:-1]
                    leaf = map.get(node)
        print(res)


    # Boolean that indicates that a node is in the graph or not
    def inGraph(self, node, graph=None):
        if graph is None:
            graph = self.graph
        if node in graph:
            return True
        return False

    #Print the graph
    def print(self, graph=None):
        if graph is None:
            graph = self.graph
        for i in graph:
            print(graph[i])

    #Get size of graph
    def size(self):
        return len(self.graph)

    #Init the dictionary
    def init(self):
        self.graph = OrderedDict()

#Main Method
def main():
    dag = DAG()
    file = open(argv[1], "r")
    for i in file:
        words = i.split()
        dag.addNode(words[0])
        dag.addNode(words[1])
        dag.addEdge(words[0], words[1])
    bg = BG()
    bg.createFromDAG(dag)
    bg.getResults()

if __name__ == '__main__':
    main()
