import getopt, sys
from State import State
from queue import PriorityQueue

# parse command lines
# DEFAULT VALUES
fileName = sys.argv[1]
maxIterations = 1000000

# drop first arg (name of code file) and second (name of input file)
argumentList = sys.argv[2:]

options = "if:"
long_options = ["MAX_ITERS", "FILE"]

try: 
    arguments, values = getopt.getopt(argumentList, options, long_options)

    for currentArgument, currentValue in arguments:
        if currentArgument in ("-i", "--MAX_ITERS"):
            maxIterations = currentValue
        elif currentArgument in ("-f", "--FILE"):
            fileName = currentValue

except getopt.error as e:
    print(str(e))

# create initial and ending states
numberOfStacks = -1
numberOfBlocks = -1
numberOfMoves = -1
initialGrid = []
goalGrid = []

with open(fileName, "r") as file:
    numberOfStacks, numberOfBlocks, numberOfMoves = [int(x) for x in next(file).split()]
    # skip a divider 
    line = file.readline()
    for y in range(numberOfStacks):
        line = file.readline()
        initialGrid.append(line.strip())

    # skip a divider
    line = file.readline()
    for y in range(numberOfStacks):
        line = file.readline()
        goalGrid.append(line.strip())
        
# print("numberOfStacks", numberOfStacks)
# print("numberOfBlocks", numberOfBlocks)
# print("numberOfMoves", numberOfMoves)
# print("Initial")
# print(initialGrid)
# print("Goal")
# print(goalGrid)

initialState = State(0, None, initialGrid)
goalState = State(0, None, goalGrid)

# start BFS iteration
maxQueueLength = 1
stateQueue = PriorityQueue()
stateQueue.put((1, initialState))
visitedStates = []
finishedState = None

# loop while not empty
i = 0
while stateQueue:
    # print(i)
    # grab state, mark as visited, ensure its a state that has not been checked
    currentState = stateQueue.get()[1]
    currentState.get_heuristic_score(goalState)

    print("***")
    print(currentState)
    print("***")

    i += 1
    if currentState.get_grid_string_representation() in visitedStates:
        continue
    visitedStates.append(currentState.get_grid_string_representation())
    currentState.mark_visited()

    # update queue length 
    if maxQueueLength < stateQueue.qsize():
        maxQueueLength = stateQueue.qsize()

    # check if reached a goal state
    if currentState.is_goal_state(goalState):
        print("Success! iter:" + str(i) + ", depth: " + str(currentState.get_level()) + ", max queue size: " + str(maxQueueLength))
        currentState.print_solution_path()
        finishedState = currentState
        break
    
    # check if max iterations reached
    if i > maxIterations:
        print("Max iterations")
        exit()

    # add all the children to queue
    allChildren = currentState.get_all_children(numberOfBlocks+1)
    for j in range(len(allChildren)):
        currentChildScore = allChildren[j].get_heuristic_score(goalState)
        stateQueue.put((currentChildScore, allChildren[j]))
        # stateQueue.append(allChildren[j])

# print out results
print("statistics: " + fileName + " method BFS planlen " + str(currentState.get_level()) + " iters " + str(i) + " maxq " + str(maxQueueLength))
