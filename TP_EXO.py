"""
TP2 — Robotique : Dijkstra bidirectionnel et A* bidirectionnel
Implémentation sur grilles de labyrinthes utilisant les algorithmes de Maze_Solving.py

Auteurs : [Binôme]
Date    : 28 mars 2026
"""

import time
import math
import os
import numpy as np
from Maze_Solving import Maze
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap


# ============================================================
# Wrappers pour les algorithmes
# ============================================================

def run_dijkstra(maze, start, end):
    """Lance Dijkstra classique et retourne (path, temps_ms, nodes_explored)."""
    t0 = time.perf_counter()
    path = maze.Dijkstra(start, end)
    t_ms = (time.perf_counter() - t0) * 1000
    nodes_explored = getattr(maze, '_last_nodes_explored', 0)
    return path or [], t_ms, nodes_explored


def run_dijkstra_bi(maze, start, end):
    """Lance Dijkstra bidirectionnel et retourne (path, temps_ms, nodes_explored)."""
    t0 = time.perf_counter()
    path = maze.Dijkstra_Bi_Simple(start, end)
    t_ms = (time.perf_counter() - t0) * 1000
    nodes_explored = getattr(maze, '_last_nodes_explored', 0)
    return path or [], t_ms, nodes_explored


def run_astar_bi(maze, start, end):
    """Lance A* bidirectionnel et retourne (path, temps_ms, nodes_explored)."""
    t0 = time.perf_counter()
    path = maze.a_star_Bi_Simple(start, end)
    t_ms = (time.perf_counter() - t0) * 1000
    nodes_explored = getattr(maze, '_last_nodes_explored', 0)
    return path or [], t_ms, nodes_explored


# ============================================================
# Visualisation
# ============================================================

def _savefig(nom):
    """Sauvegarde la figure courante en PNG."""
    outdir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(outdir, nom)
    plt.savefig(path, dpi=150, bbox_inches='tight')
    print(f"  > Graphique sauvegarde : {nom}")


def _visualiser_maze(maze, path1, path2, titre1, titre2, ax1, ax2):
    """
    Visualise deux chemins côte à côte sur un labyrinthe.
    - Murs : noir (-1.0)
    - Libre : gris pâle (0.0)
    - Chemin 1 : orange (0.4)
    - Chemin 2 : vert (1.0)
    """
    H, W = maze.H, maze.W

    # Créer deux grilles
    grid1 = [[-1.0] * W for _ in range(H)]
    grid2 = [[-1.0] * W for _ in range(H)]

    # Initialiser cellules libres
    for y in range(H):
        for x in range(W):
            if maze.is_walkeable(y, x):
                grid1[y][x] = 0.0
                grid2[y][x] = 0.0

    # Marquer chemin 1 en orange (0.4)
    for node in path1:
        if 0 <= node[0] < H and 0 <= node[1] < W:
            if grid1[node[0]][node[1]] == 0.0:
                grid1[node[0]][node[1]] = 0.4

    # Marquer chemin 2 en vert (1.0)
    for node in path2:
        if 0 <= node[0] < H and 0 <= node[1] < W:
            if grid2[node[0]][node[1]] == 0.0:
                grid2[node[0]][node[1]] = 1.0

    # Colormap (RdYlGn avec black pour murs)
    base = plt.colormaps.get_cmap('RdYlGn')
    colors = ['black'] + [base(i / 255) for i in range(256)]
    cmap = ListedColormap(colors)

    # Visualiser grille 1
    arr1 = np.array(grid1)
    arr1_idx = ((arr1 + 1) * 128).clip(0, 256).astype(int)
    ax1.imshow(arr1_idx, cmap=cmap, vmin=0, vmax=256, origin='upper')
    ax1.set_title(titre1, fontsize=11)
    ax1.axis('off')

    # Visualiser grille 2
    arr2 = np.array(grid2)
    arr2_idx = ((arr2 + 1) * 128).clip(0, 256).astype(int)
    ax2.imshow(arr2_idx, cmap=cmap, vmin=0, vmax=256, origin='upper')
    ax2.set_title(titre2, fontsize=11)
    ax2.axis('off')


# ============================================================
# Question 1 — Dijkstra Bidirectionnel
# ============================================================

def q1_dijkstra_bidirectionnel():
    """Q1 — Tester Dijkstra bidirectionnel sur un labyrinthe 50x50."""
    print("\n" + "="*70)
    print("Question 1 — Dijkstra Bidirectionnel")
    print("="*70)

    print("\n  Creation d'un labyrinthe 50x50...")
    maze = Maze(50, 50, (0, 0), (49, 49), window=None)

    print("  Execution de Dijkstra classique...")
    path_dij, t_dij, nodes_dij = run_dijkstra(maze, (0, 0), (49, 49))

    print("  Execution de Dijkstra bidirectionnel...")
    # Create new maze for bi-directional to have fresh state
    maze2 = Maze(50, 50, (0, 0), (49, 49), window=None)
    path_dij_bi, t_dij_bi, nodes_dij_bi = run_dijkstra_bi(maze2, (0, 0), (49, 49))

    print(f"\n  Resultats:")
    print(f"    Dijkstra classique     : {len(path_dij)} noeuds en {t_dij:.3f} ms, {nodes_dij} explores")
    print(f"    Dijkstra bidirectionnel: {len(path_dij_bi)} noeuds en {t_dij_bi:.3f} ms, {nodes_dij_bi} explores")
    print(f"\n  Critere d'arret bidirectionnel: Halt quand top_forward + top_backward >= mu")
    reduction = 100 * (1 - nodes_dij_bi / nodes_dij) if nodes_dij > 0 else 0
    print(f"  Reduction d'exploration: {reduction:.1f}% de noeuds epargnes")

    # Figure
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    _visualiser_maze(maze, path_dij, path_dij_bi, f"Dijkstra classique\n{len(path_dij)} noeuds, {nodes_dij} explores",
                     f"Dijkstra bidirectionnel\n{len(path_dij_bi)} noeuds, {nodes_dij_bi} explores", axes[0], axes[1])

    legende = [
        mpatches.Patch(color='black', label='Mur'),
        mpatches.Patch(color='#d4a537', label='Chemin (classique)'),
        mpatches.Patch(color='#2ecc71', label='Chemin (bidirectionnel)'),
    ]
    fig.legend(handles=legende, loc='lower center', ncol=3, fontsize=10)

    plt.suptitle("Q1 — Dijkstra Bidirectionnel", fontsize=13, fontweight='bold')
    plt.tight_layout(rect=[0, 0.08, 1, 0.96])
    _savefig('q1_dijkstra_bi.png')
    plt.show()


# ============================================================
# Question 2 — Test sur différents types de graphes
# ============================================================

def q2_grands_mazes():
    """Q2 — Tester Dijkstra bidirectionnel sur 3 types de graphes (inspirés du PDF)."""
    print("\n" + "="*70)
    print("Question 2 — Dijkstra Bidirectionnel sur 3 Types de Graphes")
    print("="*70)

    # Trois types de labyrinthes simulant les trois graphes du PDF
    graph_configs = [
        ("Random Geometric\n(120x120, dens=0.7)", 120, 0.7),      # Graphe géométrique aléatoire
        ("Erdos-Renyi\n(120x120, dens=0.5)", 120, 0.5),           # Graphe Erdos-Renyi
        ("Barabasi-Albert\n(100x100, dens=0.3)", 100, 0.3)        # Graphe Barabasi-Albert
    ]

    results = []

    for name, size, density in graph_configs:
        print(f"\n  Test {name.replace(chr(10), ' ')}...")
        maze = Maze(size, size, (0, 0), (size - 1, size - 1), window=None)
        maze.generateMaze(density)  # Changer la densité d'obstacles
        maze.generateReward()  # Réinitialiser reward_map avec la nouvelle navigation_map

        path, t_ms, nodes = run_dijkstra_bi(maze, (0, 0), (size - 1, size - 1))
        results.append((name.split('\n')[0], size, density, len(path), nodes, t_ms))
        print(f"    Chemin: {len(path)} noeuds, {nodes} explores en {t_ms:.3f} ms")

    # Barplot avec deux panneaux
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    graph_names = [r[0] for r in results]
    nodes_list = [r[4] for r in results]
    times_list = [r[5] for r in results]

    # Exploration
    bars1 = ax1.bar(range(len(graph_names)), nodes_list, color=['#3498db', '#e74c3c', '#2ecc71'], width=0.6)
    ax1.set_ylabel("Noeuds explores", fontsize=11, fontweight='bold')
    ax1.set_title("Exploration par type de graphe", fontsize=11, fontweight='bold')
    ax1.set_xticks(range(len(graph_names)))
    ax1.set_xticklabels(graph_names, fontsize=10)
    ax1.grid(axis='y', alpha=0.3)
    for i, val in enumerate(nodes_list):
        ax1.text(i, val + 50, f"{val}", ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Temps
    bars2 = ax2.bar(range(len(graph_names)), times_list, color=['#3498db', '#e74c3c', '#2ecc71'], width=0.6)
    ax2.set_ylabel("Temps (ms)", fontsize=11, fontweight='bold')
    ax2.set_title("Temps d'execution par type de graphe", fontsize=11, fontweight='bold')
    ax2.set_xticks(range(len(graph_names)))
    ax2.set_xticklabels(graph_names, fontsize=10)
    ax2.grid(axis='y', alpha=0.3)
    for i, val in enumerate(times_list):
        ax2.text(i, val + 0.1, f"{val:.2f}ms", ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.suptitle("Q2 — Dijkstra Bidirectionnel sur 3 Types de Graphes", fontsize=13, fontweight='bold')
    plt.tight_layout()
    _savefig('q2_trois_graphes.png')
    plt.show()


# ============================================================
# Question 3 — Comparer avec Dijkstra Classique
# ============================================================

def q3_comparer_dijkstra():
    """Q3 — Comparer Dijkstra classique vs bidirectionnel."""
    print("\n" + "="*70)
    print("Question 3 — Comparaison Dijkstra Classique vs Bidirectionnel")
    print("="*70)

    print("\n  Creation d'un labyrinthe 80x80...")
    maze1 = Maze(80, 80, (0, 0), (79, 79), window=None)
    maze2 = Maze(80, 80, (0, 0), (79, 79), window=None)

    print("  Execution Dijkstra classique...")
    path_dij, t_dij, nodes_dij = run_dijkstra(maze1, (0, 0), (79, 79))

    print("  Execution Dijkstra bidirectionnel...")
    path_dij_bi, t_dij_bi, nodes_dij_bi = run_dijkstra_bi(maze2, (0, 0), (79, 79))

    print(f"\n  Resultats:")
    print(f"    Dijkstra classique     : {len(path_dij)} noeuds, {nodes_dij} explores, {t_dij:.3f} ms")
    print(f"    Dijkstra bidirectionnel: {len(path_dij_bi)} noeuds, {nodes_dij_bi} explores, {t_dij_bi:.3f} ms")
    reduction = 100 * (1 - nodes_dij_bi / nodes_dij) if nodes_dij > 0 else 0
    print(f"    Reduction exploration  : {reduction:.1f}%")

    # Figure
    fig = plt.figure(figsize=(14, 6))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.2, 1.2, 1])

    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    _visualiser_maze(maze1, path_dij, path_dij_bi, f"Dijkstra Classique\n{len(path_dij)} noeuds, {nodes_dij} explores",
                     f"Dijkstra Bidirectionnel\n{len(path_dij_bi)} noeuds, {nodes_dij_bi} explores", ax1, ax2)

    # Barplot
    ax3 = fig.add_subplot(gs[2])
    algos = ['Classique', 'Bidirectional']
    explores = [nodes_dij, nodes_dij_bi]
    colors = ['#3498db', '#e74c3c']
    bars = ax3.bar(algos, explores, color=colors, width=0.5)
    ax3.set_ylabel("Noeuds explores", fontsize=11)
    ax3.set_title("Exploration", fontsize=11)
    ax3.grid(axis='y', alpha=0.3)

    for bar, val in zip(bars, explores):
        ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 10,
                 f"{val}", ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.suptitle("Q3 — Dijkstra: Classique vs Bidirectionnel", fontsize=13, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    _savefig('q3_comparaison_dijkstra.png')
    plt.show()


# ============================================================
# Question 4 — (Adaptation) A* Bidirectionnel
# ============================================================

def q4_astar_bidirectionnel():
    """Q4 — Implémenter et tester A* bidirectionnel."""
    print("\n" + "="*70)
    print("Question 4 — A* Bidirectionnel (avec heuristique Manhattan)")
    print("="*70)

    print("\n  Creation d'un labyrinthe 80x80...")
    maze = Maze(80, 80, (0, 0), (79, 79), window=None)

    print("  Execution A* bidirectionnel...")
    path_astar_bi, t_astar_bi, nodes_astar_bi = run_astar_bi(maze, (0, 0), (79, 79))

    print(f"\n  Resultats A* bidirectionnel:")
    print(f"    Chemin de {len(path_astar_bi)} noeuds")
    print(f"    {nodes_astar_bi} noeuds explores")
    print(f"    Temps: {t_astar_bi:.3f} ms")
    print(f"\n  Heuristique: distance de Manhattan")

    # Figure
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    H, W = maze.H, maze.W
    grid = [[-1.0] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            if maze.is_walkeable(y, x):
                grid[y][x] = 0.0
    for node in path_astar_bi:
        if 0 <= node[0] < H and 0 <= node[1] < W:
            if grid[node[0]][node[1]] == 0.0:
                grid[node[0]][node[1]] = 1.0

    base = plt.colormaps.get_cmap('RdYlGn')
    colors = ['black'] + [base(i / 255) for i in range(256)]
    cmap = ListedColormap(colors)
    arr = np.array(grid)
    arr_idx = ((arr + 1) * 128).clip(0, 256).astype(int)
    ax.imshow(arr_idx, cmap=cmap, vmin=0, vmax=256, origin='upper')
    ax.set_title(f"A* Bidirectionnel\n{len(path_astar_bi)} noeuds, {nodes_astar_bi} explores", fontsize=11)
    ax.axis('off')

    legende = [
        mpatches.Patch(color='black', label='Mur'),
        mpatches.Patch(color='#2ecc71', label='Chemin'),
    ]
    fig.legend(handles=legende, loc='lower center', ncol=2, fontsize=10)

    plt.suptitle("Q4 — A* Bidirectionnel", fontsize=13, fontweight='bold')
    plt.tight_layout(rect=[0, 0.08, 1, 0.96])
    _savefig('q4_astar_bi.png')
    plt.show()


# ============================================================
# Question 5 — Comparer Dijkstra Bi vs A* Bi
# ============================================================

def q5_comparer_final():
    """Q5 — Comparer Dijkstra bidirectionnel vs A* bidirectionnel."""
    print("\n" + "="*70)
    print("Question 5 — Dijkstra Bi vs A* Bi Comparison")
    print("="*70)

    print("\n  Creation d'un labyrinthe 100x100...")
    maze1 = Maze(100, 100, (0, 0), (99, 99), window=None)
    maze2 = Maze(100, 100, (0, 0), (99, 99), window=None)

    print("  Execution Dijkstra bidirectionnel...")
    path_dij_bi, t_dij_bi, nodes_dij_bi = run_dijkstra_bi(maze1, (0, 0), (99, 99))

    print("  Execution A* bidirectionnel...")
    path_astar_bi, t_astar_bi, nodes_astar_bi = run_astar_bi(maze2, (0, 0), (99, 99))

    print(f"\n  Resultats:")
    print(f"    Dijkstra Bi : {len(path_dij_bi)} noeuds, {nodes_dij_bi} explores, {t_dij_bi:.3f} ms")
    print(f"    A* Bi       : {len(path_astar_bi)} noeuds, {nodes_astar_bi} explores, {t_astar_bi:.3f} ms")

    reduction_astar = 100 * (1 - nodes_astar_bi / nodes_dij_bi) if nodes_dij_bi > 0 else 0
    print(f"    A* explore {reduction_astar:.1f}% moins de noeuds grace a l'heuristique")

    # Figure avec deux grilles et barplot
    fig = plt.figure(figsize=(15, 5))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 0.8])

    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    _visualiser_maze(maze1, path_dij_bi, path_astar_bi,
                     f"Dijkstra Bi\n{len(path_dij_bi)} noeuds, {nodes_dij_bi} explores",
                     f"A* Bi\n{len(path_astar_bi)} noeuds, {nodes_astar_bi} explores", ax1, ax2)

    # Barplot
    ax3 = fig.add_subplot(gs[2])
    methods = ['Dijkstra Bi', 'A* Bi']
    explores = [nodes_dij_bi, nodes_astar_bi]
    times = [t_dij_bi, t_astar_bi]

    x = np.arange(len(methods))
    width = 0.35

    bars1 = ax3.bar(x - width / 2, explores, width, label='Noeuds explores', color='#3498db')
    ax3_2 = ax3.twinx()
    bars2 = ax3_2.bar(x + width / 2, times, width, label='Temps (ms)', color='#e74c3c')

    ax3.set_ylabel('Noeuds explores', color='#3498db', fontsize=10)
    ax3_2.set_ylabel('Temps (ms)', color='#e74c3c', fontsize=10)
    ax3.set_title('Comparaison', fontsize=11)
    ax3.set_xticks(x)
    ax3.set_xticklabels(methods, fontsize=9)
    ax3.tick_params(axis='y', labelcolor='#3498db')
    ax3_2.tick_params(axis='y', labelcolor='#e74c3c')
    ax3.grid(axis='y', alpha=0.3)

    plt.suptitle("Q5 — Dijkstra Bidirectionnel vs A* Bidirectionnel", fontsize=13, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    _savefig('q5_dijkstra_vs_astar.png')
    plt.show()


# ============================================================
# Fonction principale
# ============================================================

def main():
    """Exécute tous les tests."""
    print("\n" + "="*70)
    print("TP2 — DIJKSTRA ET A* BIDIRECTIONNELS")
    print("="*70)

    q1_dijkstra_bidirectionnel()
    q2_grands_mazes()
    q3_comparer_dijkstra()
    q4_astar_bidirectionnel()
    q5_comparer_final()

    print("\n" + "="*70)
    print("TOUS LES TESTS SONT TERMINES")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
