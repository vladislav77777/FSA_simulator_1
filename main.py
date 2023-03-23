dictionary = {}
adj_list = {}  # create empty adjacency list
adj_list_directed = {}
adj_list_undirected = {}

# Vladislav Grigorev
def inputData():
    global dictionary
    with open("fsa.txt", "r") as f:
        for i in range(5):
            inp = f.readline().strip()
            equal = inp.find("=")
            if inp[:equal] not in dictionary:
                dictionary[inp[:equal]] = []
            for ss in inp[equal + 2:len(inp) - 1].split(","):
                dictionary[inp[:equal]].append(ss)


def createAdjLists():
    global adj_list_undirected, adj_list, adj_list_directed
    for tran in dictionary["trans"]:
        a, t, b = tran.split(">")
        if a not in adj_list:
            adj_list[a] = []
        adj_list[a].append([t, b])
    for j in adj_list:
        if j not in adj_list_directed:
            adj_list_directed[j] = []
        if j not in adj_list_undirected:
            adj_list_undirected[j] = []
        for i in adj_list[j]:
            adj_list_directed[j].append(i[1])
            if i[1] not in adj_list_undirected:
                adj_list_undirected[i[1]] = []
            if i[1] == j:
                adj_list_undirected[j].append(i[1])
                continue
            adj_list_undirected[j].append(i[1])
            adj_list_undirected[i[1]].append(j)
    adj_list_undirected = {i: set(adj_list_undirected[i]) for i in adj_list_undirected}


def checkErrors():
    global dictionary, adj_list

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
                f.write(f"E1: A state {elem} is not in the set of states\n")
            exit(0)
    for elem in dictionary["fin.st"]:
        if elem not in dictionary["states"] and elem != "":
            with open("result.txt", "w") as f:
                f.write("Error:\n")
                f.write(f"E1: A state {elem} is not in the set of states\n")
            exit(0)
    for elem in adj_list:
        if elem not in dictionary["states"]:
            with open("result.txt", "w") as f:
                f.write("Error:\n")
                f.write(f"E1: A state {elem} is not in the set of states\n")
            exit(0)
    for elem in adj_list:
        for state2 in adj_list[elem]:
            if state2[1] not in dictionary["states"]:
                with open("result.txt", "w") as f:
                    f.write("Error:\n")
                    f.write(f"E1: A state {state2[1]} is not in the set of states\n")
                exit(0)

    for elem in adj_list:
        for tr in adj_list[elem]:
            if tr[0] not in dictionary["alpha"]:
                with open("result.txt", "w") as f:
                    f.write("Error:\n")
                    f.write(f"E3: A transition {tr[0]} is not represented in the alphabet")
                exit(0)


def dfs(now):
    visited[now] = comp  # mark current node as visited
    # visit all neighbors that haven't been visited yet
    for neighbor in adj_list_undirected[now]:
        if not visited[neighbor]:
            dfs(neighbor)


def dfsDirected(now, t):
    if now == t:
        return True
    visited[now] = True  # mark current node as visited
    # visit all neighbors that haven't been visited yet
    for neighbor in adj_list_directed[now]:
        if not visited[neighbor]:
            if dfsDirected(neighbor, t):
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
        dfs(i)
        comp += 1
for i in visited:
    if visited[i] > 1:
        with open("result.txt", "w") as f:
            f.write("Error:\n")
            f.write("E2: Some states are disjoint")
        exit(0)

warnings = []
if dictionary["fin.st"][0] == "":
    warnings.append("W1: Accepting state is not defined")

visited = {i: False for i in dictionary["states"]}  # create list to track visited nodes
init = dictionary["init.st"][0]
# start DFS from every unvisited node
for i in dictionary["states"]:
    if not dfsDirected(init, i):
        warnings.append("W2: Some states are not reachable from the initial state")

for i in adj_list:
    for j in range(len(adj_list[i]) - 1):
        if adj_list[i][j][0] == adj_list[i][j + 1][0]:
            warnings.append("W3: FSA is nondeterministic")

if len(warnings) == 0:
    with open("result.txt", "w") as f:
        f.write("FSA is complete\n")
else:
    with open("result.txt", "w") as f:
        f.write("FSA is incomplete\n")
        f.write("Warning:\n")
        for war in warnings:
            f.write(war)
            f.write("\n")
