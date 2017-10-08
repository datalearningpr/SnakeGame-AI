import queue

# size_x = 150
# size_y = 150
# visited = []
# target = [50, 10]
# start = [80, 70]

# based on the parent list to generate the path from start to the end
def getTrace(parent, start, end):
    path = [end]
    while path[-1] != start:
        path.append(parent[str(path[-1])])
    path.reverse()
    return path

# the BFS method to get the path from start to target
# since the BFS is one of the basic search method
# will not add detail comments to this fucntion
def bfs(size_x, size_y, block_size, visited, target, start):

    options = queue.Queue(maxsize = 0)
    options.put(start)

    parent = {}
    while options.empty() is False:
        visit = options.get()        
     
        if visit == target:
            break
        elif visit in visited:
            pass
        else:
            new_options = []
            new_options.append([visit[0] + block_size, visit[1]])
            new_options.append([visit[0] - block_size, visit[1]])
            new_options.append([visit[0], visit[1] + block_size])
            new_options.append([visit[0], visit[1] - block_size])

            visited.append(visit)
            
            for i in new_options:
                if i[0] < 0 or i[1] < 0 or i[0] >= size_x or i[1] >= size_y or i in visited:
                    pass
                else:
                    parent[str(i)] = visit
                    options.put(i)
    
    final_path = getTrace(parent, start, target)
    return final_path



