# Vladislav Grigorev
# 09.03.2023
import re  # for regular expression

dictionary = {}  # we keep al our data in dictionary
adj_list = {}  # create empty adjacency list
adj_list_directed = {}  # for directed graphs
adj_list_undirected = {}  # for undirected graphs


# input fsa data
def inputData():
    global dictionary
    with open("fsa.txt", "r") as f:
        for i in range(5):  # fill in fields states, alpha, initial, finite states, and transitions
            inp = f.readline().strip()
            equal = inp.find("=")
            if inp[:equal] not in dictionary:
                dictionary[inp[:equal]] = []
            for ss in inp[equal + 2:len(inp) - 1].split(","):
                dictionary[inp[:equal]].append(ss)


# creating adjustment lists for storing our graph
def createAdjLists():
    global adj_list_undirected, adj_list, adj_list_directed
    # create adjacency lists from transitions
    for tran in dictionary["trans"]:
        a, t, b = tran.split(">")
        # add transition to adjacency list for start state a
        if a not in adj_list:
            adj_list[a] = []
        adj_list[a].append([t, b])
    # create directed and undirected adjacency lists from adjacency list
    for j in adj_list:
        # initialize directed and undirected adjacency lists for state j
        if j not in adj_list_directed:
            adj_list_directed[j] = []
        if j not in adj_list_undirected:
            adj_list_undirected[j] = []
        # for each transition from state j
        for i in adj_list[j]:
            # add destination state to directed adjacency list for state j
            adj_list_directed[j].append(i[1])
            if i[1] not in adj_list_undirected:
                adj_list_undirected[i[1]] = []
            # add destination state to undirected adjacency list for state j
            if i[1] == j:
                adj_list_undirected[j].append(i[1])
                continue
            adj_list_undirected[j].append(i[1])
            adj_list_undirected[i[1]].append(j)

    adj_list_undirected = {i: set(adj_list_undirected[i]) for i in adj_list_undirected}


"""=======================================================================
   Checking for errors:
    1. Any state name does not satisfy condition (Latin letters, numbers) - E5
    2. Any alphbet name does not satisfy conditions (Latin letters, numbers, underscore sign) - E5
    4. Any final state name is not present in the states - E1
    5. More than one initial state - E5
    6. No initial state - E4
    7. Initial state is not present in the states - E1
    8. States in transition are not present in states - E1 
    9. Letter in transition is not present in alphabet - E3
    10. FSA has disjoint state(s) - E2
==========================================================================="""


def checkErrors():
    global dictionary, adj_list

    # check for various errors in states
    def check_state_name(state_name):
        pattern = re.compile('[^a-zA-Z0-9]')
        if pattern.search(state_name):
            return True
        else:
            return False

    # check for various errors in alphabet
    def check_alphabet_name(alphabet_name):
        pattern = re.compile('[^a-zA-Z0-9_]')
        if pattern.search(alphabet_name):
            return True
        else:
            return False

    # check for invalid state names
    for state in dictionary["states"]:
        if check_state_name(state):
            with open("result.txt", "w") as f:
                f.write("Error:\n")
                f.write("E5: Input file is malformed\n")
            exit(0)

    # check for invalid alphabet symbols
    for alpha in dictionary["alpha"]:
        if check_alphabet_name(alpha):
            with open("result.txt", "w") as f:
                f.write("Error:\n")
                f.write("E5: Input file is malformed\n")
            exit(0)

    # check for undefined initial state
    if dictionary["init.st"][0] == "":
        with open("result.txt", "w") as f:
            f.write("Error:\n")
            f.write("E4: Initial state is not defined\n")
        exit(0)

    if len(dictionary["init.st"]) > 1:
        with open("result.txt", "w") as f:
            f.write("Error:\n")
            f.write("E5: Input file is malformed\n")
        exit(0)

    for elem in dictionary["init.st"]:
        if elem not in dictionary["states"] and elem != "":
            with open("result.txt", "w") as f:
                f.write("Error:\n")
                f.write(f"E1: A state '{elem}' is not in the set of states\n")
            exit(0)
    for elem in dictionary["fin.st"]:
        if elem not in dictionary["states"] and elem != "":
            with open("result.txt", "w") as f:
                f.write("Error:\n")
                f.write(f"E1: A state '{elem}' is not in the set of states\n")
            exit(0)
    for elem in adj_list:
        if elem not in dictionary["states"]:
            with open("result.txt", "w") as f:
                f.write("Error:\n")
                f.write(f"E1: A state '{elem}' is not in the set of states\n")
            exit(0)
    for elem in adj_list:
        for state2 in adj_list[elem]:
            if state2[1] not in dictionary["states"]:
                with open("result.txt", "w") as f:
                    f.write("Error:\n")
                    f.write(f"E1: A state '{state2[1]}' is not in the set of states\n")
                exit(0)

    for elem in adj_list:
        for tr in adj_list[elem]:
            if tr[0] not in dictionary["alpha"]:
                with open("result.txt", "w") as f:
                    f.write("Error:\n")
                    f.write(f"E3: A transition '{tr[0]}' is not represented in the alphabet\n")
                exit(0)


"""============== DFS ====================================
Define a depth-first search function for undirected graphs
    We check for the disjoint states.
==========================================================="""


def dfs(now, visited):
    global adj_list_undirected, comp
    visited[now] = comp  # mark current node as visited
    # visit all neighbors that haven't been visited yet
    if now in adj_list_undirected:
        for neighbor in adj_list_undirected[now]:
            if not visited[neighbor]:
                dfs(neighbor, visited)


"""============== DFS 2 ===================================
Define a depth-first search function for undirected graphs
    We check whether some states are not reachable from the initial state.
==========================================================="""


def dfsDirected(now, t, visited):
    global adj_list_directed, comp
    if now == t:
        return True
    visited[now] = True  # mark current node as visited
    # visit all neighbors that haven't been visited yet
    if now in adj_list_directed:
        for neighbor in adj_list_directed[now]:
            if not visited[neighbor]:
                if dfsDirected(neighbor, t, visited):
                    return True
    return False


inputData()
createAdjLists()
checkErrors()

visited = {i: False for i in dictionary["states"]}  # create list to track visited nodes
comp = 1
# start DFS from every unvisited node
for i in dictionary["states"]:
    if not visited[i]:
        dfs(i, visited)
        comp += 1
for i in visited:
    if visited[i] > 1:
        with open("result.txt", "w") as f:
            f.write("Error:\n")
            f.write("E2: Some states are disjoint\n")
        exit(0)

warnings = []  # creating list for warnings
if dictionary["fin.st"][0] == "":
    warnings.append("W1: Accepting state is not defined")

visited = {i: False for i in dictionary["states"]}  # create list to track visited nodes
init = dictionary["init.st"][0]
# start DFS from every unvisited node
for i in dictionary["states"]:
    if not dfsDirected(init, i, visited):
        warnings.append("W2: Some states are not reachable from the initial state")

for i in adj_list:
    for j in range(len(adj_list[i]) - 1):
        if adj_list[i][j][0] == adj_list[i][j + 1][0]:
            warnings.append("W3: FSA is nondeterministic")

isComplete = True  # checking for completeness of the FSA
for i in adj_list:
    trs = []
    for j in adj_list[i]:
        trs.append(j[0])
    if set(trs) != set(dictionary["alpha"]):
        isComplete = False

with open("result.txt", "w") as f:  # write out the result
    if isComplete:
        f.write("FSA is complete\n")
    else:
        f.write("FSA is incomplete\n")
    if len(warnings) != 0:
        f.write("Warning:\n")
        for war in warnings:
            f.write(war)
            f.write("\n")
