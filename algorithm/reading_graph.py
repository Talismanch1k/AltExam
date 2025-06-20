import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from config import FNAME

def reading_file():
    ff = open(FNAME)
    inp = ff.readlines()
    n,m = list(map(int,inp[0].split()))
    
    vertexes = set()                    # словарь вершин
    edges_dict = {}                     # словарь ребер
    edges_set = set()                   # множество ребер

    for i in range(m):
        u, v, height = list(map(int, inp[i+1].split()))
        u = str(u)
        v = str(v)
        if (u,v) not in edges_dict.keys():
            edges_dict[(u,v)] = height      # ключ - ребро, значение - его вес
        else:
            edges_dict[(u,v)] = min(height, edges_dict[(u,v)])
        edges_set.add((u,v))
        vertexes |= {u,v}   
    root = str(int(inp[-1]))   
    ff.close()
    return n,root,vertexes,edges_dict,edges_set


def reading_console():
    n,m = list(map(int, input().split()))
    
    vertexes = set()                    # словарь вершин
    edges_dict = {}                     # словарь ребер
    edges_set = set()                   # множество ребер

    for i in range(m):
        u, v, height = list(map(int, input().split()))
        if (u,v) not in edges_dict.keys():
            edges_dict[(u,v)] = height      # ключ - ребро, значение - его вес
        else:
            edges_dict[(u,v)] = min(height, edges_dict[(u,v)])
        edges_set.add((u,v))
        vertexes |= {u,v}
    root = int(input())    
    return n,root,vertexes,edges_dict,edges_set
