import sys
import math
import picos as pic
import networkx as nx
import itertools
import cvxopt
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import write_dot, graphviz_layout

class Carpool:
    def __init__(self, people):
        self.people = people
        self.G = nx.DiGraph()
        self.days = ['M', 'T', 'W', 'R', 'F']
        self.daysDict = {}
        for person in people:
            for day in person.days:
                self.daysDict[day] = self.daysDict.get(day, 0) + 1
        self.create_network()
        pos = graphviz_layout(self.G, prog='dot')     
        edge_labels = nx.get_edge_attributes(self.G, 'capacity')
        nx.draw(self.G, pos)
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels, font_size=8)
        nx.draw_networkx_labels(self.G, pos, font_size=10)
        
        plt.show() 

    def create_network(self):
        '''Builds up the network needed for solving the badminton elimination
        problem as a network flows problem & stores it in self.G. Returns a
        dictionary of saturated edges that maps team pairs to the amount of
        additional games they have against each other.

        teamID: ID of team that we want to check if it is eliminated
        return: dictionary of saturated edges that maps team pairs to
        the amount of additional games they have against each other
        '''

        saturated_edges = {}

        self.G.add_node("Source")
        self.G.add_node("Sink")
        

        for day in self.days:
            self.G.add_node(day)
            self.G.add_edge(day, "Sink", capacity=1, flow=0)
        

        for person in self.people:
            self.G.add_node(person)
            for day in person.days:
                self.G.add_edge(person, day, capacity=1, flow=0)
            capacity = math.ceil(self.getResponibility(person))
            self.G.add_edge("Source", person, capacity=capacity, flow=0)

        return saturated_edges

    def network_flows(self):
        '''Uses network flows to determine if the team with given team ID
        has been eliminated. You can feel free to use the built in networkx
        maximum flow function or the maximum flow function you implemented as
        part of the in class implementation activity.

        saturated_edges: dictionary of saturated edges that maps team pairs to
        the amount of additional games they have against each other
        return: True if team is eliminated, False otherwise
        '''

        flow_value, flow_dict = nx.maximum_flow(self.G, "Source", "Sink")
        print(flow_dict)
        G2 = self.dictToNx(flow_dict)
        pos = graphviz_layout(G2, prog='dot')     
        edge_labels = nx.get_edge_attributes(G2, 'flow')
        nx.draw(G2, pos)
        nx.draw_networkx_edge_labels(G2, pos, edge_labels, font_size=8)
        nx.draw_networkx_labels(G2, pos, font_size=10)
        plt.show()
        if flow_value != 5:
            return False

        return True

    def getResponibility(self, person):
        total = 0
        for day in person.days:
            total += 1 / self.daysDict[day]
        return total
            
    def dictToNx(self, flow_dict):
        G2 = nx.DiGraph()
        for key in flow_dict.keys():
            G2.add_node(key)
        for key in flow_dict.keys():
            for destKey in flow_dict[key]:
                if flow_dict[key][destKey] > 0:
                    G2.add_edge(key, destKey, flow=flow_dict[key][destKey])
        return G2


class Person:
    def __init__(self, ID, days):
        self.ID = ID
        self.days = days
    
    def __str__(self):
        return "Person " + str(self.ID)


if __name__ == '__main__':
    person1 = Person(1, ["M", "T", "W"])
    person2 = Person(2, ["M", "W"])
    person3 = Person(3, ["M", "T", "W", "R", "F"])
    person4 = Person(4, ["T", "W", "R", "F"])
    people = [person1, person2, person3, person4]

    car = Carpool(people)
    print("Solvable?: " + str(car.network_flows()))