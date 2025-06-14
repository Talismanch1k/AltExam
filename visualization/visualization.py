import networkx as nx
import os
import matplotlib.pyplot as plt
import numpy as np
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from config import VIZ_DIR, VIZ_MODE



step_counter = 0

def ensure_viz_dir():
    """Создаёт папку viz, если она не существует."""
    if not os.path.exists(VIZ_DIR):
        os.makedirs(VIZ_DIR)

def draw_graph(vertexes: set, edges_dict: dict, root: int,  
               min_edges: dict = None, cycle: set = None, 
               mst_edges: set = None, stage: str = "graph"):
    """Рисует граф и сохраняет изображение в папке viz, отображая однонаправленные дуги.
    
    Args:
        vertexes: Множество вершин.
        edges_dict: Словарь рёбер с весами {(u, v): weight}.
        root: Корневая вершина.
        min_edges: Словарь минимальных входящих рёбер {v: (u, weight)}.
        cycle: Множество вершин цикла (для подсветки синим).
        mst_edges: Множество рёбер остовного дерева (для подсветки красным).
        stage: Описание этапа для имени файла.
    """
    global step_counter
    ensure_viz_dir()
    #print(edges_dict.items())
    G = nx.DiGraph()
    # Добавляем вершины
    G.add_nodes_from(vertexes)
    # Добавляем рёбра с весами
    for (u, v), weight in edges_dict.items():
        G.add_edge(u, v, weight=weight)
    
    # Определяем цвета и толщину рёбер
    edge_colors = []
    edge_widths = []
    for u, v in G.edges():
        if mst_edges and (u, v) in mst_edges:
            edge_colors.append('r')  # Рёбра остова — красные
            edge_widths.append(2.5)  # Увеличенная толщина
        elif min_edges and (u, v) in [(min_edges[to][0], to) for to in min_edges]:
            edge_colors.append('r')  # Минимальные рёбра — красные
            edge_widths.append(2.5)  # Увеличенная толщина
        elif cycle is not None and min_edges and (u, v) in [(min_edges[to][0], to) for to in cycle if to in min_edges]:
            edge_colors.append('b')  # Рёбра цикла — синие
            edge_widths.append(1.0)  # Стандартная толщина
        else:
            edge_colors.append('k')  # Обычные рёбра — чёрные
            edge_widths.append(1.0)  # Стандартная толщина
    
    # Определяем цвета вершин
    node_colors = ['y' if v == root else 'b' if cycle is not None and v in cycle else 'lightblue' for v in G.nodes()]
    
    # Рисуем граф
    plt.figure(figsize=(10, 8))  # Увеличиваем размер изображения
    pos = nx.spring_layout(G, seed=100, k=0.25)  # Увеличиваем расстояние между вершинами с помощью k
    
    # Рисуем вершины
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=300)
    
    # Рисуем рёбра с кривизной для двунаправленных дуг
    if VIZ_MODE == '1':
        edge_styles = []
        for u, v in G.edges():
            # Если есть обратное ребро (v, u), добавляем кривизну
            if G.has_edge(v, u):
                edge_styles.append('arc3,rad=0.2')  # Положительная кривизна
            else:
                edge_styles.append('arc3,rad=0')  # Прямая стрелка
        
        # Рисуем рёбра с индивидуальной толщиной
        for (u, v), style, color, width in zip(G.edges(), edge_styles, edge_colors, edge_widths):
            nx.draw_networkx_edges(
                G, pos, edgelist=[(u, v)], edge_color=color, width=width,
                arrows=True, connectionstyle=style, arrowsize=15
            )
        
        # Рисуем метки рёбер с небольшим смещением для двунаправленных дуг
        edge_labels = nx.get_edge_attributes(G, 'weight')
        for (u, v), weight in edge_labels.items():
            # Если есть обратное ребро, смещаем метку
            
            #offset = -0.1 if (v,u) in already_drawing else 0.1
            # Вычисляем позицию метки со смещением
            
            #x = (pos[u][0] + pos[v][0]) / 2
            #y = (pos[u][1] + pos[v][1]) / 2
            if G.has_edge(v, u):
                x = pos[v][0]+(pos[u][0]-pos[v][0])*0.1
                y = pos[v][1]+(pos[u][1]-pos[v][1])*0.1
            else:
                x = (pos[u][0] + pos[v][0]) / 2
                y = (pos[u][1] + pos[v][1]) / 2
            
            
            plt.text(x, y, weight, fontsize=8, ha='center', va='center', 
                     bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    elif VIZ_MODE=='2':
        edge_styles = []
        curved_edges = {}
        for u, v in G.edges():
            # Если есть обратное ребро (v, u), добавляем кривизну
            if G.has_edge(v, u):
                edge_styles.append('arc3,rad=0.2')  # Положительная кривизна
                curved_edges[(u, v)] = 0.2
            else:
                edge_styles.append('arc3,rad=0')  # Прямая стрелка
                curved_edges[(u, v)] = 0
        
        for (u, v), style, color, width in zip(G.edges(), edge_styles, edge_colors, edge_widths):
            nx.draw_networkx_edges(
                G, pos, edgelist=[(u, v)], edge_color=color, width=width,
                arrows=True, connectionstyle=style, arrowsize=15
            )
        

        edge_labels = nx.get_edge_attributes(G, 'weight')
        
        straight_edges = {(u, v): w for (u, v), w in edge_labels.items() if not G.has_edge(v, u)}
        
        if straight_edges:
            nx.draw_networkx_edge_labels(
                G, pos,
                edge_labels=straight_edges,
                font_size=8,
                label_pos=0.5,
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
            )
        
        # Вручную размещаем метки для изогнутых рёбер с точным позиционированием
        for (u, v), weight in edge_labels.items():
            if G.has_edge(v, u):  # Если это изогнутое ребро
                # Позиции вершин
                x1, y1 = pos[u]
                x2, y2 = pos[v]
                
                # Вычисляем среднюю точку между вершинами
                xm = (x1 + x2) / 2
                ym = (y1 + y2) / 2
                
                # Вычисляем перпендикулярный вектор
                dx = x2 - x1
                dy = y2 - y1
                length = (dx**2 + dy**2)**0.5
                nx_vec = -dy / length
                ny_vec = dx / length
                
                # Радиус кривизны (должен соответствовать connectionstyle="arc3,rad=0.2")
                rad = 0.20
                
                # Контрольная точка кривой Безье (соответствует arc3,rad=0.2)
                # Эмпирически подобранный множитель 0.7 для лучшего соответствия визуальной кривой
                cx = xm + rad * length * 0.7 * nx_vec
                cy = ym + rad * length * 0.7 * ny_vec
                
                # Параметр t определяет позицию на кривой (0.5 = середина)
                t = 0.5
                
                # Точка на квадратичной кривой Безье
                # B(t) = (1-t)²P₀ + 2(1-t)tP₁ + t²P₂
                label_x = (1-t)**2 * x1 + 2*(1-t)*t * cx + t**2 * x2
                label_y = (1-t)**2 * y1 + 2*(1-t)*t * cy + t**2 * y2
                
                plt.text(label_x, label_y, weight, fontsize=8, ha='center', va='center', 
                         bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))  
                
    nx.draw_networkx_labels(G, pos, font_size=12)
    

    filename = os.path.join(VIZ_DIR, f"step_{step_counter:03d}_{stage}.png")
    plt.savefig(filename, format='png', bbox_inches='tight')
    plt.close()
    
    step_counter += 1