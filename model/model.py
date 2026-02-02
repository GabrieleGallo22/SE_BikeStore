import networkx as nx

from database.dao import DAO

class Model:


    def get_category(self):
        return DAO.get_category()

    def get_date_range(self):
        return DAO.get_date_range()

    def get_product(self, category):
        return DAO.get_product(category)

    def get_product_in_category(self, category, first, last):
        return DAO.get_product_in_category(category, first, last)

    def __init__(self):
        self._grafo = nx.DiGraph()
        self._nodes = []
        self._edges = []

    def build_graph(self, category, first, last):
        self._grafo.clear()

        self._nodes = DAO.get_product(category)
        self._grafo.add_nodes_from(self._nodes)

        vendite = DAO.get_product_in_category(category, first, last)

        idMap = {row[0]: row[2] for row in vendite}

        for u in self._nodes:
            for v in self._nodes:
                if u != v:
                    peso_u = idMap.get(u[0], 0)
                    peso_v = idMap.get(v[0], 0)
                    if peso_u > 0 and peso_v > 0:
                        peso = peso_u + peso_v
                        if peso_u > peso_v:
                            self._grafo.add_edge(u, v, weight=peso)
                        elif peso_u < peso_v:
                            self._grafo.add_edge(v, u, weight=peso_u)
                        else:
                            self._grafo.add_edge(u, v, weight=peso_u)
                            self._grafo.add_edge(v, u, weight=peso_v)

    def handle_best_prodotti(self):

        risultati = []
        for n in self._grafo.nodes:
            pesi_uscenti = self._grafo.out_degree(n, weight="weight")
            pesi_entranti = self._grafo.in_degree(n, weight="weight")

            bilancio = pesi_uscenti - pesi_entranti
            risultati.append((n,bilancio))

        risultati.sort(key=lambda x: x[1], reverse=True)
        return risultati[:5]

    def get_num_nodes(self):
        return self._grafo.number_of_nodes()
    def get_num_edges(self):
        return self._grafo.number_of_edges()


if __name__ == '__main__':
    m = Model()
    m.build_graph("Road bikes", '2016-01-01 00:00:00', '2018-12-28 00:00:00')  # <--- Metti un valore che esiste nel DB!

    # Ti dice quanti sono e ti fa vedere il primo per controllare se è giusto
    print(f"archi totali: {len(m._grafo.edges)}")
    print(f"Primo arco: {list(m._grafo.edges)[0]}")