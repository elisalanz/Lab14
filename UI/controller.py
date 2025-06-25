import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._selectedNode = None


    def fillDDStores(self):
        storesId = self._model.getAllStoreId()
        for id in storesId:
            self._view._ddStore.options.append(ft.dropdown.Option(id))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        store_id = self._view._ddStore.value
        if store_id is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, selezionare uno store dal menu.", color = "red"))
            self._view.update_page()
            return
        k = self._view._txtIntK.value
        if k == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, inserire un numero massimo di giorni.", color="red"))
            self._view.update_page()
            return
        try:
            kInt = int(k)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, inserire un numero intero.", color="red"))
            self._view.update_page()
            return
        if kInt <= 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, inserire un numero intero maggiore di 0.", color="red"))
            self._view.update_page()
            return
        self._model.buildGraph(store_id, kInt)
        self._fillDDNode()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        nNodi, nArchi = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nNodi}\nNumero di archi: {nArchi}"))
        self._view.update_page()

    def _fillDDNode(self):
        self._view._ddNode.options.clear()
        self._selectedNode = None
        nodes = self._model.getAllNodes()
        for node in nodes:
            self._view._ddNode.options.append(ft.dropdown.Option(data = node, text = node.order_id, on_click=self._readDDNode))
        self._view.update_page()

    def _readDDNode(self, e):
        if e.control.data is None:
            self._selectedNode = None
        else:
            self._selectedNode = e.control.data

    def handleCerca(self, e):
        if self._selectedNode is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, selezionare un nodo dal menu.", color="red"))
            self._view.update_page()
            return
        self._view.txt_result.controls.append(ft.Text(f"Nodo di partenza: {self._selectedNode.order_id}"))
        percorso = self._model.getLongestPath(self._selectedNode)
        for nodo in percorso:
            self._view.txt_result.controls.append(ft.Text(f"{nodo.order_id}"))
        self._view.update_page()


    def handleRicorsione(self, e):
        if self._selectedNode is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, selezionare un nodo dal menu.", color="red"))
            self._view.update_page()
            return
        percorso, score = self._model.getBestPath(self._selectedNode)
        self._view.txt_result.controls.append(ft.Text(f"Percorso ottimo da {self._selectedNode.order_id} creato con score = {score}"))
        for nodo in percorso:
            self._view.txt_result.controls.append(ft.Text(f"{nodo.order_id}"))
        self._view.update_page()

