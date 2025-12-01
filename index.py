from A_star_graph import Graph, create_random_pos, create_limited_graph_optimized
import graph_data
import display_graph
import time
import math

header_size = 40

graph_default = Graph(
    create_limited_graph_optimized(graph_data.default_pos), graph_data.default_pos
)
graph_200_pos = create_random_pos(200, graph_data.default_pos)
graph_200 = Graph(create_limited_graph_optimized(graph_200_pos), graph_200_pos)
graph_big_pos = create_random_pos(1000, graph_data.default_pos)
big_graph = Graph(create_limited_graph_optimized(graph_big_pos), graph_big_pos)


def default_display(graph, source="PNJ", target="JMB"):
    global header_size
    print(f"from {graph_data.pos_alias[source]} to {graph_data.pos_alias[target]}")
    print(f"{" A-star Algorithm ":=^{header_size}}")
    path, distance, node_astar = graph.shortest_path(source, target, True)
    print(f"Path : {path}\ndistance:{distance}")
    print(f"visited nodes: {len(node_astar)}")
    print(f"{" Djikstra Algorithm ":=^{header_size}}")
    path, distance, node_djikstra = graph.shortest_path(source, target, True, "djikstra")
    print(f"Path : {path}\ndistance:{distance}")
    print(f"visited nodes: {len(node_djikstra)}")
    display_graph.display_graph2(
        graph.vertex, graph.coordinate, path, False, node_djikstra, node_astar, 1
    )

def display_default_coordinate():
    for key, value in graph_data.default_pos.items():
        print(
            f"Code : {key:<5} | Pasar {graph_data.pos_alias[key]:<15} | coordinate : {value[0]}x, {value[1]}y"
        )

def menu_choice_point(graph):
    choice = "0"
    print("1. Use default source and target")
    print("2. Search for target and source")
    choice = input("input choice: ")
    match choice:
        case "1":
            default_display(graph)
        case "2":
            display_default_coordinate()
            if len(graph.vertex) > 15:
                keys = list(graph.coordinate.keys())
                print(
                    f"input random position from {keys[15]} - {keys[-1]} Max number : {math.ceil((len(keys)-15)/26)}"
                )
            source = input("enter source : ")
            target = input("enter target : ")
            default_display(graph, source, target)

def recreate_big_graph(pos=1000):
    global graph_big_pos, big_graph
    choice = '0'
    match choice:
        case'1':
            graph_big_pos = create_random_pos(pos, graph_data.default_pos)
            big_graph = Graph(create_limited_graph_optimized(graph_big_pos), graph_big_pos)
        case'2':
            print("vertex more than 5000 is not recomended, O(n^2 + nlogn) algorithm")
            pos = int(input("enter number of vertex"))
            graph_big_pos = create_random_pos(pos, graph_data.default_pos)
            big_graph = Graph(create_limited_graph_optimized(graph_big_pos), graph_big_pos)

def recreate_graph():
    global graph_default, graph_200_pos, graph_200
    choice = "0"
    print(f"{" RE CREATE GRAPH ":=^{header_size}}")
    print("1. default graph")
    print("2. 200 point graph")
    print("3. BIG GUY graph")
    choice = input("input choice : ")
    match choice:
        case '1':
            graph_default = Graph(
                create_limited_graph_optimized(graph_data.default_pos),
                graph_data.default_pos,
            )
        case '2':
            graph_200_pos = create_random_pos(200, graph_data.default_pos)
            graph_200 = Graph(create_limited_graph_optimized(graph_200_pos), graph_200_pos)
        case '3':
            recreate_big_graph()

if __name__ == "__main__":
    choice = "0"
    menu = [
        "1. Look default graph",
        "2. Djikstra and A-star default graph",
        "3. Djikstra and A-star 200V",
        "4. Djikstra and A-star 1000V",
        "5. re-create graph",
    ]
    while choice != "4":
        print(f"{" MENU ":=^{header_size}}")
        for _, val in enumerate(menu):
            print(val)
        choice = input("input choice : ")
        match choice:
            case "1":
                display_graph.display_graph2(
                    graph_default.vertex, graph_data.default_pos
                )
            case "2":
                menu_choice_point(graph_default)
            case "3":
                menu_choice_point(graph_200)
            case "4":
                menu_choice_point(big_graph)
            case "5":
                recreate_graph()
