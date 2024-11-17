import getopt, sys
from State import State
import random
import math
import pandas as pd

# parse command lines
fileName = sys.argv[1]

# create initial and ending states
numberOfStacks = -1
numberOfBlocks = -1
numberOfMoves = -1
initialGrid = []
goalGrid = []

# read in the file 
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


data = { 'iteration': 0, 'heur_score' : 0, 'deltaE': math.nan}
df = pd.DataFrame(data, index=[0])


initialState = State(0, None, initialGrid)
goalState = State(0, None, goalGrid)



# start Simulated Annealing
finishedState = None
currentState = initialState


t = 100000
tempThreshold = 0.0001

# loop while not empty
i = 0
while True:
    # iterate
    i += 1

    # check if reached a goal state
    if currentState.is_goal_state(goalState):
        print("Success! iter:" + str(i) + ", depth: " + str(currentState.get_level()))
        # currentState.print_solution_path()
        finishedState = currentState
        break
    
    # half temperature every 1000 iterations
    if i == 1000:
        t /= 2
        print("Halfing t to be " + str(t))
        i = 0

    # if temperature is too low, break
    if t < tempThreshold:
        print("Reached threshold")
        finishedState = currentState
        break

    # get the next random state
    allChildren = currentState.get_all_children(numberOfBlocks+1)
    nextRandomState = random.choice(allChildren)
    deltaE = currentState.get_heuristic_score(goalState) - nextRandomState.get_heuristic_score(goalState)
    # print("delta e: " + str(deltaE))

    # next state is better than current
    if deltaE > 0:
        currentState = nextRandomState
    else:
        # choose state based on probability
        probability = math.e**(deltaE / t)
        if random.random() <= probability:
            print("At Temperature " + str(t) + ", Choosing worse state by probability " + str(probability))


    data = { 'iteration' : i, 'heur_score': currentState.get_heuristic_score(goalState), 'deltaE': deltaE }
    df.loc[len(df)] = data




# print out results
print(currentState.print_solution_path())
print("statistics: " + fileName + " method SimulatedAnnealing planlen " + str(currentState.get_level()) + " iters " + str(i))


print(df)


