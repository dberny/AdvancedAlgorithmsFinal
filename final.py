import sys
import math
import picos as pic
import networkx as nx
import itertools
import cvxopt

class Carpool:
    def __init__(self, filename):
        self.people = {}
        self.G = nx.DiGraph()
        self.days = ['M', 'T', 'W', 'R', 'F']
        self.daysDict = {}
        for person in people:
            for day in person.days():
                daysDict[day] = daysDict.get(day, 0) + 1

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

        G.add_node("Source")
        G.add_node("Sink")
        people = self.people.keys()

        for day in self.days:
            G.add_node(day)
            G.add_edge(day, "Sink", {"capacity":1, "flow":0})
        

        for person in people:
            G.add_node(person)
            for day in person.days:
                G.add_edge(person, day, {"capacity":1, "flow":0})
            capacity = math.ceil(self.getResponibility(person))
            G.add_edge(person, "Source", {"capacity":capacity, "flow":0})

        return saturated_edges

    def network_flows(self, saturated_edges):
        '''Uses network flows to determine if the team with given team ID
        has been eliminated. You can feel free to use the built in networkx
        maximum flow function or the maximum flow function you implemented as
        part of the in class implementation activity.

        saturated_edges: dictionary of saturated edges that maps team pairs to
        the amount of additional games they have against each other
        return: True if team is eliminated, False otherwise
        '''

        #TODO: implement this

        return False

    def getResponibility(self, person):
        total = 0
        for day in person.days:
            total += 1 / self.daysDict[day]
        return total
            


class Person:
    def __init__(self, ID, days):
        self.ID = ID
        self.days = days


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        division = Division(filename)
        for (ID, team) in division.teams.items():
            print(f'{team.name}: Eliminated? {division.is_eliminated(team.ID, "Linear Programming")}')
    else:
        print("To run this code, please specify an input file name. Example: python badminton_elimination.py teams2.txt.")