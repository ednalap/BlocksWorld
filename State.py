class State:
    def __init__(self, level: int, parent: 'State' = None, grid: list[list[str]] = []):
        self.level = level
        self.parent = parent
        self.visited = False
        self.grid = []
        for i, row in enumerate(grid):
            currList = []
            for j, col in enumerate(row):
                currList.append(col)
            self.grid.append(currList)

    def get_all_children(self, maxStackHeight: int) -> list['State']:
        # all possible moves come from looking at all stacks, and if they have a block, try moving it to all the other stacks with room
        allChildren = []
        
        # loop through all stacks
        for i, firstStack in enumerate(self.grid):
            # if stack is not empty
            if len(firstStack) > 0:
                # loop through stacks again to see if they are at the max stack height
                for j, secondStack in enumerate(self.grid):
                    if i == j:
                        continue

                    if len(secondStack) < maxStackHeight:
                        # create a new state with the level + 1, self as the parent, and same grid
                        # TODO: self.get_grid() is passing by reference
                        
                        newState = State(self.get_level() + 1, self, self.get_grid())
                        # execute the move from row to col
                        newState.execute_move(i, j)
                        allChildren.append(newState)

        return allChildren

    def is_goal_state(self, other: 'State'):
        # assert that the number of stacks are the same
        if (len(self.get_grid()) != len(other.get_grid())):
            return False
        
        # loop through self's grid, asserting lengths and the chars are the same as the other 
        for i, row in enumerate(self.get_grid()):
            # check length of self's row and the solution's row are the same
            if (len(row) != len(other.get_grid()[i])):
                return False
            
            for j, col in enumerate(row):
                if (col != other.get_grid()[i][j]):
                    return False
                
        # if we make it through the previous checks, then we are at a goal solution
        return True
    
    # move block on top of first stack to second stack
    # used to create children states
    def execute_move(self, i: int, j: int):
        # grab block to move and pop from first stack
        blockTomove = self.get_grid()[i][-1]
        self.get_grid()[i] = self.get_grid()[i][:-1]

        # add to second stack
        self.get_grid()[j] += blockTomove

    def __str__(self):
        toReturn = ">>>>>>>>>>\n"
        for i, row in enumerate(self.get_grid()):
            for j, col in enumerate(row):
                toReturn += col + " "
            toReturn += "\n"
        toReturn += ">>>>>>>>>>"
        return toReturn.strip()
    
    def get_grid_string_representation(self):
        toReturn = ""
        for i, row in enumerate(self.get_grid()):
            if(len(row) == 0):
                toReturn += "EMPTY"
            for j, col in enumerate(row):
                toReturn += col + " "
            toReturn += "\n"
        return toReturn.strip()
    
    def print_solution_path(self):
        if self.level == 0:
            print("move " + str(self.level + 1))
            print(self)
            return
        
        self.get_parent().print_solution_path()
        # print self path
        print("move " + str(self.level + 1))
        print(self)

    # heuristic:    if the block is in the correct place, then return 0
    #               if the block is in the correct stack and wrong place, then return number of blocks between the correct and incorrect place 
    #               if the block is in the wrong stack and wrong place, then return number of blocks on top of the wrong stack + number of blocks needed to remove on the corrects tack 

    def get_heuristic_score(self, goalState) -> int:
        totalScore = 0
        # go through each block for self
        for i, row in enumerate(self.get_grid()):
            for j, col in enumerate(row):
                if (self.is_block_out_of_place(col, goalState)):
                    totalScore += 1
                if (self.is_block_underneath_correct(col, goalState)):
                    totalScore += 1
                if (self.is_second_block_underneath_correct(col, goalState)):
                    totalScore += 1
        # print("TOTAL SCORE: " + str(totalScore))
        return totalScore + self.get_level()
    
    def is_block_out_of_place(self, blockToTest, goalState):
        selfStackNumber = 0
        goalStackNumber = 0
        selfPositionBottom = 0
        goalPositionBottom = 0

        # get stack in self that contains the block
        for i, row in enumerate(self.get_grid()):
            if blockToTest in row:
                # get the number of blocks on top
                selfStackNumber = i
                selfPositionBottom = len(row[:row.index(blockToTest)])
        # get stack in goal that contains the block
        for i, row in enumerate(goalState.get_grid()):
            if blockToTest in row:
                goalStackNumber = i
                goalPositionBottom = len(row[:row.index(blockToTest)])

        return not (selfStackNumber == goalStackNumber and selfPositionBottom == goalPositionBottom)
    
    def is_block_underneath_correct(self, blockToTest, goalState):
        selfStackNumber = 0
        goalStackNumber = 0
        selfBlockUnderneath = "BOTTOM"
        goalBlockUnderneath = "BOTTOM"

        # get stack in self that contains the block
        for i, row in enumerate(self.get_grid()):
            if blockToTest in row:
                # get the number of blocks on top
                selfStackNumber = i
                selfPositionBottom = len(row[:row.index(blockToTest)])

                # if a block underneath exists, save
                if not row.index(blockToTest) == 0:
                    selfBlockUnderneath = row[row.index(blockToTest) - 1]


        # get stack in goal that contains the block
        for i, row in enumerate(goalState.get_grid()):
            if blockToTest in row:
                goalStackNumber = i
                goalPositionBottom = len(row[:row.index(blockToTest)])

                # if a block underneath exists, save
                if not row.index(blockToTest) == 0:
                    goalBlockUnderneath = row[row.index(blockToTest) - 1]

        return not (selfBlockUnderneath == goalBlockUnderneath)
    
    def is_second_block_underneath_correct(self, blockToTest, goalState):
        selfStackNumber = 0
        goalStackNumber = 0
        selfBlockUnderneath = "BOTTOM"
        goalBlockUnderneath = "BOTTOM"

        # get stack in self that contains the block
        for i, row in enumerate(self.get_grid()):
            if blockToTest in row:
                # get the number of blocks on top
                selfStackNumber = i
                selfPositionBottom = len(row[:row.index(blockToTest)])

                # if a block underneath exists, save
                if row.index(blockToTest) > 2:
                    selfBlockUnderneath = row[row.index(blockToTest) - 2]


        # get stack in goal that contains the block
        for i, row in enumerate(goalState.get_grid()):
            if blockToTest in row:
                goalStackNumber = i
                goalPositionBottom = len(row[:row.index(blockToTest)])

                # if a block underneath exists, save
                if row.index(blockToTest) > 2:
                    goalBlockUnderneath = row[row.index(blockToTest) - 2]

        return not (selfBlockUnderneath == goalBlockUnderneath)



    def get_number_of_displacements(self, blockToTest, goalState):
        selfStackNumber = 0
        goalStackNumber = 0
        selfPositionBottom = 0
        goalPositionBottom = 0
        selfStackDisplacement = 0
        goalStackDisplacement = 0

        # get stack in self that contains the block
        for i, row in enumerate(self.get_grid()):
            if blockToTest in row:
                # get the number of blocks on top
                selfStackNumber = i
                selfStackDisplacement = len(row[row.index(blockToTest):])
                selfPositionBottom = len(row[:row.index(blockToTest)])

        # get stack in goal that contains the block
        for i, row in enumerate(goalState.get_grid()):
            if blockToTest in row:
                goalStackNumber = i
                goalStackDisplacement = len(row[row.index(blockToTest):])
                goalPositionBottom = len(row[:row.index(blockToTest)])

        if selfStackNumber == goalStackNumber and selfStackDisplacement == goalStackDisplacement:
            return 0
        if (selfStackNumber == goalStackNumber):
            return abs(selfStackDisplacement - goalPositionBottom)
        return (selfStackDisplacement + goalStackDisplacement)

    def get_level(self) -> int:
        return self.level
    
    def set_level(self, level: int):
        self.level = level

    def get_parent(self) -> 'State':
        return self.parent
    
    def set_parent(self, parent: 'State'): 
        return self.parent
    
    def get_grid(self) -> list[str]:
        return self.grid
    
    def set_grid(self, grid):
        self.grid = grid

    def mark_visited(self):
        self.visited = True
    
    def is_visited(self) -> bool:
        return self.visited
    
    def __lt__(self, other):
        return False