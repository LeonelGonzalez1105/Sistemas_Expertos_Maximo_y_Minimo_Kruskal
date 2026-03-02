import networkx as nx
import matplotlib.pyplot as plt

class UnionFind:
    def __init__(self, nodos):
        self.parent = {nodo: nodo for nodo in nodos}
    
    def find(self, item):
        if self.parent[item] == item:
            return item
        return self.find(self.parent[item])
    
    def union(self, set1, set2):
        root1 = self.find(set1)
        root2 = self.find(set2)
        if root1 != root2:
            self.parent[root1] = root2
            return True 
        return False 


def kruskal_logica_urbana(grafo_dict, modo_maximo=False):
    aristas = []
    nodos = list(grafo_dict.keys())
    
    for u in grafo_dict:
        for v, peso in grafo_dict[u].items():
            if u < v: 
                aristas.append((u, v, peso))
    
    aristas.sort(key=lambda x: x[2], reverse=modo_maximo)
    
    uf = UnionFind(nodos)
    mst_aristas = []
    costo_total = 0
    
    tipo = "MAXIMA CAPACIDAD DE CARGA" if modo_maximo else "MINIMA DISTANCIA (Combustible)"
    print(f"\n--- ANALISIS DE RUTA URBANA (Modo: {tipo}) ---")
    print(f"{'Tramo':<25} | {'Valor':<5} | {'Estado'}")
    print("-" * 55)
    
    for u, v, peso in aristas:
        if uf.union(u, v):
            print(f"{u}-{v:<18} | {peso:<5} | Incluido en ruta")
            mst_aristas.append((u, v))
            costo_total += peso
        else:
            print(f"{u}-{v:<18} | {peso:<5} | Excluido (Ruta alterna)")
            
    return mst_aristas, costo_total

def graficar_mapa_logistico(grafo_dict, aristas_res, costo, modo_maximo):
    G = nx.Graph()
    for u, vecinos in grafo_dict.items():
        for v, peso in vecinos.items():
            G.add_edge(u, v, weight=peso)
            
    pos = nx.spring_layout(G, seed=20)
    plt.figure(figsize=(12, 8))
    
    nx.draw_networkx_nodes(G, pos, node_size=1300, node_color='#EEEEEE')
    nx.draw_networkx_edges(G, pos, width=1, alpha=0.2, edge_color='black', style='dotted')
    nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')
    
    color_ruta = '#E67E22' if modo_maximo else '#27AE60' 
    titulo = "Prioridad: Capacidad Pesada" if modo_maximo else "Prioridad: Ahorro de Energia"
    
    # Dibujar ruta optima
    nx.draw_networkx_nodes(G, pos, nodelist=[n for edge in aristas_res for n in edge], node_size=1300, node_color=color_ruta, alpha=0.4)
    nx.draw_networkx_edges(G, pos, edgelist=aristas_res, width=4, edge_color=color_ruta)
    
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)
    
    plt.title(f"Planificacion Logistica: {titulo}\nCosto Operativo Total: {costo}", fontsize=12)
    plt.axis('off')
    
    plt.savefig(f"logistica_{'max' if modo_maximo else 'min'}.png")
    plt.show()


mapa_logistico = {
    'Almacen_Central': {'Punto_A': 7, 'Punto_B': 5},
    'Punto_A': {'Almacen_Central': 7, 'Zona_Norte': 12, 'Punto_B': 9},
    'Punto_B': {'Almacen_Central': 5, 'Punto_A': 9, 'Zona_Sur': 15, 'Centro_Distribucion': 6},
    'Zona_Norte': {'Punto_A': 12, 'Puerto_Carga': 20, 'Zona_Sur': 10},
    'Zona_Sur': {'Punto_B': 15, 'Zona_Norte': 10, 'Puerto_Carga': 8},
    'Centro_Distribucion': {'Punto_B': 6, 'Puerto_Carga': 11},
    'Puerto_Carga': {'Zona_Norte': 20, 'Zona_Sur': 8, 'Centro_Distribucion': 11}
}

if __name__ == "__main__":
    while True:
        print("\n" + "="*50)
        print(" GESTOR DE RUTAS LOGISTICAS (KRUSKAL)")
        print("="*50)
        print("1. Generar ruta de MINIMO consumo (Kilometros)")
        print("2. Generar ruta de MAXIMA resistencia (Tonelaje)")
        print("3. Salir")
        
        opcion = input("\nSeleccione modo de operacion (1/2/3): ")
        
        if opcion == '3':
            print("Finalizando sistema logistico.")
            break
            
        elif opcion in ['1', '2']:
            es_maximo = (opcion == '2')
            ruta, costo_final = kruskal_logica_urbana(mapa_logistico, es_maximo)
            
            print(f"\nCalculo finalizado. Valor total del trayecto: {costo_final}")
            graficar_mapa_logistico(mapa_logistico, ruta, costo_final, es_maximo)
            
        else:
            print("Opcion no reconocida.")