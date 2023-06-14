#  Author:           Jorge Santos
#  Title:            Family tree
#  Course:           4883
#  Semester:         Summer 2023
# 
#  Description:
#        This code will read in randomly generated family tree data that is in json format. It will create a DOT code file. THat can be copy and pasted into graphviz to make a family tree. The genders have different background colors. Each generation is put in a subgraph and have "rank" set to "same".
#
#  Files: TBD
import json
import graphviz

dot = graphviz.Digraph(comment='Family tree', node_attr={'shape': 'box', 'style' : 'filled'})
#a list of different shapes in graphviz
shapes = ["circle","triangle","diamond","pentagon", "hexagon","septagon","octagon" ]
#will create the nodes
def processJson():
    with open('family.json') as f:
        data = json.load(f)
    
    #variable generations keeps track of the current gen being traversed
    generations = set(person["generation"] for person in data)

#loop that goes thru each generation and puts the family members
#in a subgraph with based on their generation
    for generation in generations:
      
      with dot.subgraph(name='cluster_gen{}'.format(generation)) as subgraph:
        individuals = [person for person in data if person["generation"] == generation]

        for person in individuals:
            gender = person["gender"]
            #check for the gender, and give each gender a different color
            if gender == "M":
                subgraph.node(str(person["#pid"]), str(person["name"])
 + "\\n" + str(person["byear"]) + "-" + str(person["dyear"])  , fillcolor = "lightblue", shape = shapes[generation])
            else:
                 subgraph.node(str(person["#pid"]),str(person["name"])
 + "\\n" + str(person["byear"]) + "-" + str(person["dyear"])  , fillcolor = "pink", shape = shapes[generation])
        
        for person in individuals:
            parent = person["parentNodeId"]
            spouse = person["spouseId"]
            if parent != spouse and parent is not None:
                subgraph.edge(str(parent), str(person["#pid"]))

#creates the edges between married couples     
def spouseJson():
    with open('family.json') as f:
        data = json.load(f)

    # checks if a person has a spouse and creates an edge between spouses
    for person in data:
        spouse = person["spouseId"]
        if spouse is not None:
            dot.edge(str(person["#pid"]), str(spouse), constraint= 'false',  arrowhead = "none", label = "married", color = "red" )


if __name__ == "__main__":
    processJson()
    spouseJson()
    
print(dot.source)

with open('stupid.dot', 'w') as f:
    f.write(dot.source)
