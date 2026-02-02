from UI.view import View
from model.model import Model
import flet as ft
import datetime

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def set_dates(self):
        first, last = self._model.get_date_range()

        self._view.dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view.dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp2.current_date = datetime.date(last.year, last.month, last.day)

    def populate_dd(self):
        categorie = self._model.get_category()
        self._view.dd_category.options.clear()

        for category in categorie:
            self._view.dd_category.options.append(ft.dropdown.Option(category[0]))

        self._view.page.update()


    def handle_crea_grafo(self, e):
        category = self._view.dd_category.value
        data_inizio = self._view.dp1.value
        data_fine = self._view.dp2.value

        if category is None:
            self._view.show_alert("seleziona una categoria")
            return
        if data_inizio is None:
            self._view.show_alert("selezione inizio")
            return
        if data_fine is None:
            self._view.show_alert("selezione fine")
            return
        if data_inizio > data_fine:
            self._view.show_alert("la fine non può essere prima dell'inizio")
            return

        self._model.build_graph(category, data_inizio, data_fine)
        n_nodi = self._model.get_num_nodes()
        n_archi = self._model.get_num_edges()

        self._view.txt_risultato.controls.clear()
        self._view.txt_risultato.controls.append(ft.Text(f"in totale ci sono {n_nodi} nodi e {n_archi} archi"))
        self._view.page.update()

    def handle_best_prodotti(self, e):
        top5 = self._model.handle_best_prodotti()
        self._view.txt_risultato.controls.clear()
        self._view.txt_risultato.controls.append(ft.Text("Top 5 Prodotti (Uscenti - Entranti):"))

        for p in top5:
            # p[0] è l'oggetto prodotto (o la tupla ID, Nome), p[1] è il bilancio
            # Assumendo che il nodo sia una tupla (ID, Nome)
            self._view.txt_risultato.controls.append(
                ft.Text(f"Prodotto: {p[0][1]} - Bilancio: {p[1]}")
            )
        self._view.page.update()

    def handle_cerca_cammino(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO
