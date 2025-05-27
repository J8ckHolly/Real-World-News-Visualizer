import matplotlib.pyplot as plt
import networkx as nx
import random
import math

"""
Filename: PageRankingAlgo.py

Author: Jack Holly

Date Created: 2025-01-24

Purpose:
    -Immitate the nodes(articles) and edges(cosine similarity) of the main project
    -Graph is weighted unidirectional graph
    -Run PageRanking Algorithm with a damping factor
    -Visualize Graph 
    -Run scenarios to test Algorithm's efficiency
"""

class Node:
    def __init__(self, name):
        self.name = name
        self.edges = []
        self.visits = 0

    def add_edge(self, dest_node, weight):
        self.edges.append((dest_node, weight))

    def get_edges(self):
        return self.edges

    def return_name(self):
        return self.name
    
    def is_visited(self):
        self.visits += 1
    
    def reset(self):
        self.visits = 0
    
    def __str__(self):
        print(self.return_name())
    
class WeightedGraph:
    def __init__(self):
        self.nodes = {}
        self.node_order = []
        self.G = nx.DiGraph()
        self.try_graph = True
        self.adjusted_score_value = None

    def add_node(self, name):
        if name not in self.nodes:
            self.nodes[name] = Node(name)
    
    def add_edge(self, from_node_name, to_node_name, weight):
        """Add a directed edge from one node to another with a given weight."""
        # Ensure that both nodes exist
        if from_node_name not in self.nodes:
            self.add_node(from_node_name)
        if to_node_name not in self.nodes:
            self.add_node(to_node_name)
        
        # Get the node objects
        from_node = self.nodes[from_node_name]
        to_node = self.nodes[to_node_name]
        
        # Add the edge from the from_node to the to_node with weight
        from_node.add_edge(to_node, weight)

        # Optionally, add the reverse edge for bidirectional graphs
        to_node.add_edge(from_node, weight)  # Reverse edge from to_node to from_node
        if self.try_graph:
            self.G.add_edge(from_node.return_name(), to_node.return_name(), weight = weight)
            self.G.add_edge(to_node.return_name(), from_node.return_name(), weight = weight)
    
    def get_neighbors(self, node_name):
        """Get all neighbors (outgoing edges) of the node."""
        if node_name in self.nodes:
            return self.nodes[node_name].get_edges()
        else:
            return []
    
    def get_random_node(self):
        return self.nodes[random.choice(list(self.nodes))]

    def convert_matrix_to_graph(self, matrix):
        #Add Nodes
        refrenceToArticle = len(matrix)
        for element in range(refrenceToArticle):
            self.add_node(str(element))
        for i in range(refrenceToArticle):
            for j in range(i + 1, refrenceToArticle):
                if matrix[i][j] == 0:
                    continue
                self.add_edge(str(i),str(j), matrix[i][j])
        
    def page_ranking_algorithm(self):
        currentNode = self.get_random_node()
        dampingFactor = .85
        iterations = 2000
        count = 0
        while count < iterations:
            if random.random() > dampingFactor:
                currentNode = self.get_random_node()
                currentNode.is_visited()
                count +=1
            else:
                currentNodeEdges = currentNode.get_edges()
                if (len(currentNodeEdges) == 0):
                    currentNode = self.get_random_node()
                    currentNode.is_visited()
                    count +=1
                    continue
                else:
                    nodes = []
                    weights = []
                    for node, weight in currentNode.get_edges():
                        nodes.append(node)
                        weights.append(weight)
                    
                    normalized_weights = [weight / sum(weights) for weight in weights]
                    currentNode = self.nodes[random.choices(nodes, weights=normalized_weights, k = 1)[0].return_name()]
                    currentNode.is_visited()

        #Right now do it the slow way of incrementing through and seeing what the highest value is
        #In future optomise this
        most_popular_article = max(self.nodes, key=lambda node: self.nodes[node].visits)
        print("The winner is: "+ most_popular_article)
        self.adjusted_score(self.nodes[most_popular_article], iterations)
        return most_popular_article
        
    def adjusted_score(self, Node, iterations):
        #Iteration might need to be changed for how many nodes there are?
        #Revisit the scoring
        normalizedScore = Node.visits/iterations
        self.adjusted_score_value = normalizedScore * math.log(len(self.nodes)+1)

    def return_adjusted_score(self):
        print(self.adjusted_score_value)
        return self.adjusted_score_value
    
    def return_correlation(self):
        pass
    
    def display_graph(self):
        if (not self.try_graph):
            print("Field is not on")
            return None
        else:
            # Position nodes using spring layout (you can also try others like circular_layout)
            pos = nx.spring_layout(self.G)

            # Draw the nodes and edges with labels
            nx.draw(self.G, pos, with_labels=True, node_size=300, node_color="lightblue", font_size=8)

            # Draw edge labels for weights
            #edge_labels = nx.get_edge_attributes(self.G, 'weight')
            #nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, font_size=2)

            # Show the plot
            plt.show()

"""
graph = WeightedGraph()

# Add nodes to the graph
graph.add_node("A")
graph.add_node("B")
graph.add_node("C")

# Add edges with weights
graph.add_edge("A", "B", 5)
graph.add_edge("A", "C", 10)
graph.add_edge("B", "C", 2)
graph.get_random_node()
graph.page_ranking_algorithm()
graph.return_adjusted_score()
graph.display_graph()
#graph.page_ranking_algorithm()
"""


    


