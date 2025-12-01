import networkx as nx
import matplotlib.pyplot as plt

# matplotlib config settings
plt.rcParams['figure.subplot.left'] = 0.0    # Left margin
plt.rcParams['figure.subplot.right'] = 1.0   # Right margin  
plt.rcParams['figure.subplot.bottom'] = 0.0  # Bottom margin
plt.rcParams['figure.subplot.top'] = 0.95     # Top margin

def display_graph2(graph, coordinate, path=None, directed=False, djikstra_node=None, astar_node=None, zoom_level=1.0):
    high_nodes_djikstra = set()
    high_nodes_astar = set()
    highlight_edges_path = []
    G_display = nx.DiGraph() if directed else nx.Graph()
    color_template = {
        'dijkstra': '#6B9CFF',
        'A-star': '#9CFF6B',
        # 'dijkstra-Astar' : "#FFBC6B",
        'path':'#FF6B6B',
        'market':"#CF85C6",
        'dummy':'#D3D3D3',
        'dijkstra-market': '#6B9CFF',
        'astar-market': '#9CFF6B',
        'edge-common': "#b1b1b1",
        'edge-path' : "#ff4e4e"
    }
    
    if djikstra_node is not None:
        if isinstance(djikstra_node, (list, set)):
            high_nodes_djikstra = set(djikstra_node)
        elif isinstance(djikstra_node, dict):
            high_nodes_djikstra = set(djikstra_node.keys())
    
    if astar_node is not None:
        if isinstance(astar_node, (list, set)):
            high_nodes_astar = set(astar_node)
        elif isinstance(astar_node, dict):
            high_nodes_astar = set(astar_node.keys())
    
    if path:
        for i in range(len(path) - 1):
            highlight_edges_path.append((path[i], path[i + 1]))
    
    for source, connection in graph.items():
        for target, weight in connection.items():
            if not G_display.has_edge(source, target):
                G_display.add_edge(source, target, weight=weight)
                
    market_nodes = None
    dummy_nodes = None
    if next(iter(coordinate))[0] != "A0":
        market_nodes = list(coordinate.keys())[:15]
        dummy_nodes = list(coordinate.keys())[15:]
    else:
        market_nodes = list(coordinate.keys())
        dummy_nodes = list(coordinate.keys())
        
    dijkstra_only = high_nodes_djikstra - high_nodes_astar
    astar_only = high_nodes_astar - high_nodes_djikstra
    common_nodes = high_nodes_djikstra & high_nodes_astar
    path_nodes = set(path) if path else set()

    # Categorize nodes by type and algorithm
    dijkstra_market = [node for node in dijkstra_only if node in market_nodes]
    dijkstra_dummy = [node for node in dijkstra_only if node in dummy_nodes]
    astar_market = [node for node in astar_only if node in market_nodes]
    astar_dummy = [node for node in astar_only if node in dummy_nodes]
    common_market = [node for node in common_nodes if node in market_nodes]
    common_dummy = [node for node in common_nodes if node in dummy_nodes]
    path_market = [node for node in path_nodes if node in market_nodes]
    path_dummy = [node for node in path_nodes if node in dummy_nodes]
    
    # Regular nodes (not visited by either algorithm)
    all_highlighted = high_nodes_djikstra | high_nodes_astar | path_nodes
    regular_market_nodes = [node for node in market_nodes if node not in all_highlighted]
    regular_dummy_nodes = [node for node in dummy_nodes if node not in all_highlighted]
    
    normalized_path_edges = []
    for edge in highlight_edges_path:
        normalized_path_edges.append(edge)
        normalized_path_edges.append((edge[1], edge[0]))
        
    edge_labels = nx.get_edge_attributes(G_display, "weight")
    regular_edges = [edge for edge in G_display.edges() if edge not in normalized_path_edges]
    actual_path_edges = [edge for edge in normalized_path_edges if G_display.has_edge(edge[0], edge[1])]
   
    fig, ax = plt.subplots(figsize=(18, 15))
    plt.axis("off")
    
    # Draw nodes with initial sizes
    base_size = 100 * zoom_level
    regular_dummy_size = base_size
    regular_market_size = base_size * 2
    algorithm_size = base_size * 1.5
    path_size = base_size * 2
    start_end_size = base_size * 3
        
    # Draw Regular Nodes
    nx.draw_networkx_nodes(
        G_display, coordinate, nodelist=regular_dummy_nodes,
        node_size=regular_dummy_size, node_color=color_template['dummy'], alpha=0.7,
    )
    nx.draw_networkx_nodes(
        G_display, coordinate, nodelist=regular_market_nodes,
        node_size=regular_market_size, node_color=color_template['market'], alpha=0.9,
    )

    # Draw Common Nodes (Yellow - visited by both)
    """
        Remove due to redundant of djikstra and a-star overlapping
        all a-star node has alread included in djikstra
    """
    # nx.draw_networkx_nodes(
    #     G_display, coordinate, nodelist=common_dummy,
    #     node_size=150, node_color=color_template['dijkstra-Astar'], alpha=1.0,  # Yellow
    # )
    # nx.draw_networkx_nodes(
    #     G_display, coordinate, nodelist=common_market,
    #     node_size=350, node_color=color_template['dijkstra-Astar'], alpha=1.0,
    # )
    
    # Draw Dijkstra-only Nodes (Blue)
    nx.draw_networkx_nodes(
        G_display, coordinate, nodelist=dijkstra_dummy,
        node_size=algorithm_size, node_color=color_template['dijkstra'], alpha=1.0,  # Light Blue
    )
    nx.draw_networkx_nodes(
        G_display, coordinate, nodelist=dijkstra_market,
        node_size=algorithm_size*1.5, node_color=color_template['dijkstra-market'], alpha=1.0,
    )
    
    # Draw A*-only Nodes (Green)
    nx.draw_networkx_nodes(
        G_display, coordinate, nodelist=high_nodes_astar,
        node_size=algorithm_size, node_color=color_template['A-star'], alpha=1.0,  # Light Green
    )
    nx.draw_networkx_nodes(
        G_display, coordinate, nodelist=astar_market,
        node_size=algorithm_size*1.5, node_color=color_template['astar-market'], alpha=1.0,
    )
    
    # Draw Path Nodes (Red - final path)
    nx.draw_networkx_nodes(
        G_display, coordinate, nodelist=path_dummy,
        node_size=path_size, node_color=color_template['path'], alpha=1.0,  # Red
    )
    nx.draw_networkx_nodes(
        G_display, coordinate, nodelist=path_market,
        node_size=path_size*1.5, node_color=color_template['path'], alpha=1.0,
    )
    
    if path and len(path) > 0:
        first_last_path_node = [path[0], path[-1]]
        nx.draw_networkx_nodes(
            G_display, coordinate, nodelist=first_last_path_node,
            node_size=start_end_size, node_color=color_template['edge-path'], alpha=1.0,
        )
    
    nx.draw_networkx_edges(
        G_display, coordinate, edgelist=regular_edges, 
        alpha=0.4, edge_color=color_template['edge-common'], width=1.0
    )
    
    nx.draw_networkx_edges(
        G_display, coordinate, edgelist=actual_path_edges, 
        alpha=0.9, edge_color=color_template['edge-path'], width=2.0
    )
    
    nx.draw_networkx_labels(
        G_display, coordinate, font_size=6*( zoom_level/2.5 if zoom_level != 1.0 else 1), font_family="sans-serif"
    )

    nx.draw_networkx_edge_labels(
        G_display, coordinate, edge_labels=edge_labels, 
        font_size=3, alpha=0.8
    )
    
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color_template['dijkstra'], markersize=10, label='Dijkstra'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color_template['A-star'], markersize=10, label='A*'),
        # plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color_template['dijkstra-Astar'], markersize=10, label='Both Algorithm'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color_template['path'], markersize=10, label='Final Path'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color_template['market'], markersize=10, label='Regular Market'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color_template['dummy'], markersize=10, label='Regular Dummy')
    ]
    plt.legend(handles=legend_elements, loc='upper right')
    

        
    # Add statistics to title
    dijkstra_count = len(high_nodes_djikstra)
    astar_count = len(high_nodes_astar)
    common_count = len(common_nodes)
    
    # Print statistics
    if path != None:
        print(f"\n=== Algorithm Comparison Statistics ===")
        print(f"Dijkstra visited nodes: {dijkstra_count}")
        print(f"A* visited nodes: {astar_count}")
        print(f"Common nodes (visited by both): {common_count}")
        print(f"Final path length: {len(path) if path else 0}")
    
    plt.title("A* and Djikstra Graph Comparison")
    plt.show()