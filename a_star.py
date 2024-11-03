import heapq
warehouse = [
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],#0
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 0],#1
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],#2
    [0, 0, 0, 0, 1, 0, 1, 0, 1, 0],#3
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0],#4
    [0, 0, 0, 1, 0, 1, 0, 0, 1, 0],#5
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],#6
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],#7
    [0, 0, 1, 0, 1, 0, 1, 0, 0, 0],#8
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 0] #9
]

# Define the start and end points
start = (0, 0)
end = (7, 9)

# Possible moves (right, left, down, up)
moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# Heuristic function (Manhattan distance)
def heuristic(cell, goal):
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

# A* Algorithm
def a_star(warehouse, start, end):
    rows, cols = len(warehouse), len(warehouse[0])
    open_list = []
    heapq.heappush(open_list, (0, start))  # Push the starting point with f(n) = 0
    came_from = {}  # To reconstruct the path
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_list:
        # Pop the cell with the lowest f_score
        current_f, current = heapq.heappop(open_list)
        
        # If we reach the end point, reconstruct the path
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for move in moves:
            neighbor = (current[0] + move[0], current[1] + move[1])

            # Check boundaries and obstacles
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and warehouse[neighbor[0]][neighbor[1]] == 0:
                tentative_g_score = g_score[current] + 1  # Each move costs 1
                
                # Only update if a better path is found
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None  # Return None if there is no path