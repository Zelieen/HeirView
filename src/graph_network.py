import networkx as nx
from tree import Tree
from chart import Chart


def tree_to_graph(tree: Tree) -> nx.DiGraph:
    """Converts Heirview tree to networkx DiGraph."""

    G = nx.DiGraph()
    for p in tree.persons.values():
        G.add_node(p._ID, name=p.given_name)
        if p.mother:
            G.add_edge(p._ID, p.mother, desig="mother")
        if p.father:
            G.add_edge(p._ID, p.father, desig="father")
        if p.children:
            G.add_edges_from([(p._ID, c) for c in p.children], desig="child")

    print("DiGraph constructed")
    print(list(G.nodes(data=True)))
    print(list(G.edges(data=True)))

    return G

def chart_to_graph(tree: Tree) -> nx.DiGraph:
    """Converts Heirview chart to networkx DiGraph."""

    G = nx.DiGraph()
    t = tree.get_ancestors_for_chart(-1,1)
    for p in t:
        pers = tree.persons[p.person_ID]
        G.add_node(p.person_ID, name=pers.given_name, generation=p.gen)
        if pers.mother:
            G.add_edge(pers._ID, pers.mother, desig="mother")
        if pers.father:
            G.add_edge(pers._ID, pers.father, desig="father")
        #if pers.children:
        #    G.add_edges_from([(pers._ID, c) for c in pers.children], desig="child")

    print("DiGraph constructed")
    print(list(G.nodes(data=True)))
    print(list(G.edges(data=True)))

    return G