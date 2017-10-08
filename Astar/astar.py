import math

# size_x = 150
# size_y = 150
# visited = []
# target = [50, 10]
# start = [80, 70]

# select the element from the open_set with smallest f_score
def get_min(open_set, f_score):
    min_value = float('inf')
    result = None
    for x in open_set:
        if f_score[x] < min_value:
            result = x
            min_value = f_score[x]
    return result

# the esitimate of distance between x and y is
# the Euclidean distance
def heuristic_estimate_of_distance(x, y):
    return math.sqrt((y[0] - x[0])**2 + (y[1] - x[1])**2)

# generate the path from start to the end
def reconstruct_path(came_from, start, end):
    path = [end]
    while path[-1] != start:
        path.append(came_from[path[-1]])
    path.reverse()
    return path 

# the A* search method 
def A_star(size_x, size_y, block_size, visited, target, start):
    # initiate the closed_set, open_set, came_from list, score lists
    # put the start to the open_set to begin with

    closed_set = set()
    open_set = set()
    open_set.add(start)

    came_from = {}

    g_score = {}
    h_score = {}
    f_score = {}

    # the g, h, f scores of start
    # g will be 0 since it is from start to start
    g_score[start] = 0
    h_score[start] = heuristic_estimate_of_distance(start, target)
    f_score[start] = g_score[start] + h_score[start] 

    # begin the search loop
    while len(open_set) != 0:
        # take the element with smallest f_score from open_set
        x = get_min(open_set, f_score)
        # if target found, return the path from start to target
        if x == target:
            return reconstruct_path(came_from, start, target)

        # put the chosen element to the closed_set from open_set
        open_set.remove(x)
        closed_set.add(x)

        # get the 4 cells of the element chosen
        # these are the cells to search
        new_options = []
        new_options.append((x[0] + block_size, x[1]))
        new_options.append((x[0] - block_size, x[1]))
        new_options.append((x[0], x[1] + block_size))
        new_options.append((x[0], x[1] - block_size))

        # check each one of the cells to search
        for y in new_options:
            # if the cell is: checked, outside the board, part of the snake
            # ingore the cell
            if y in closed_set or y[0] < 0 or y[1] < 0 or y[0] >= size_x or y[1] >= size_y or list(y) in visited:
                continue
            # since each move of the snake is one step,
            # the cell g_score will be its father's g_score + 1
            tetative_g_score = g_score[x] + 1

            # if cell is not checked before, put it into the open_set, assume it is good
            if y not in open_set:
                open_set.add(y)
                tetative_is_better = True
            # if cell is checked but with better g_score, still good 
            elif tetative_g_score < g_score[y]:
                tetative_is_better = True
            # otherwise, it is bad choice
            else:
                tetative_is_better = False
            
            # only focus on the good choices
            # set the father of the cell
            # update the scores
            if tetative_is_better is True:
                came_from[y] = x
                g_score[y] = tetative_g_score
                h_score[y] = heuristic_estimate_of_distance(y, target)
                f_score[y] =  g_score[y] + h_score[y] 
    return None


if __name__ == "__main__":
    print(A_star(size_x, size_y, 10, visited, tuple(target), tuple(start)))
