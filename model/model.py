import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._ordersBySelectedStore = []
        self._idMapOrders = {}
        self._longestPath = []
        self._maxLen = 0
        self._bestPath = []
        self._bestScore = 0


    def getAllStoreId(self):
        return DAO.getAllStoreId()

    def _getAllOrdersBySelectedStore(self, storeId):
        self._ordersBySelectedStore = []
        self._idMapOrders = {}
        self._ordersBySelectedStore = DAO.getAllOrdersByStoreId(storeId)
        for order in self._ordersBySelectedStore:
            self._idMapOrders[order.order_id] = order

    def buildGraph(self, storeId, numMaxGiorni):
        self._grafo.clear()
        self._getAllOrdersBySelectedStore(storeId)
        nodi = self._ordersBySelectedStore
        self._grafo.add_nodes_from(nodi)
        archi = DAO.getAllEdges(storeId, numMaxGiorni)
        for arco in archi:
            self._grafo.add_edge(self._idMapOrders[arco[0]], self._idMapOrders[arco[1]], weight=arco[2])

    def getGraphDetails(self):
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def getAllNodes(self):
        return self._grafo.nodes()

    def getLongestPath(self, source):
        self._longestPath = []
        self._maxLen = 0
        parziale = [source]
        archi_uscenti = self._grafo.out_edges(source)
        vicini = []
        for arco in archi_uscenti:
            vicini.append(arco[1])
        for vicino in vicini:
            parziale.append(vicino)
            self._ricorsione(parziale)
            parziale.pop()
        return self._longestPath

    def _ricorsione(self, parziale):
        archi_uscenti = self._grafo.out_edges(parziale[-1])
        vicini = []
        for arco in archi_uscenti:
            vicini.append(arco[1])
        for vicino in vicini:
            if vicino in parziale:
                vicini.remove(vicino)
        if len(vicini) == 0:
            if len(parziale) > self._maxLen:
                self._maxLen = len(parziale)
                self._longestPath = copy.deepcopy(parziale)
            return
        for vicino in vicini:
            parziale.append(vicino)
            self._ricorsione(parziale)
            parziale.pop()

    def getBestPath(self, source):
        self._bestPath = []
        self._bestScore = 0
        parziale = [source]
        archi_uscenti = self._grafo.out_edges(source)
        vicini = []
        for arco in archi_uscenti:
            vicini.append(arco[1])
        for vicino in vicini:
            parziale.append(vicino)
            self._ricorsione2(parziale)
            parziale.pop()
        return self._bestPath, self._bestScore

    def _ricorsione2(self, parziale):
        archi_uscenti = self._grafo.out_edges(parziale[-1])
        vicini = []
        for arco in archi_uscenti:
            vicini.append(arco[1])
        for vicino in vicini:
            if vicino in parziale:
                vicini.remove(vicino)
        if len(vicini) == 0:
            if self._calcolaScore(parziale)> self._bestScore:
                self._bestScore = self._calcolaScore(parziale)
                self._bestPath = copy.deepcopy(parziale)
            return
        for vicino in vicini:
            if self._grafo[parziale[-1]][vicino]["weight"]<self._grafo[parziale[-2]][parziale[-1]]["weight"]:
                parziale.append(vicino)
                self._ricorsione2(parziale)
                parziale.pop()

    def _calcolaScore(self, listOfNodes):
        tot = 0
        for i in range(0, len(listOfNodes)-1):
            tot += self._grafo[listOfNodes[i]][listOfNodes[i+1]]["weight"]
        return tot
