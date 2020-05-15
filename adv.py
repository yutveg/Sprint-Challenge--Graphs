from room import Room
from player import Player
from world import World
from util import Stack, Queue
import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []



def convert_path_directionals(path):
    directions = []
    # convert path to directionals n/s/w/e
    for index in range(len(path) - 1):
        room_id = path[index].id
        for key, value in traversal_graph[room_id].items():
            if value == path[index + 1]:
                directions.append(key)
    return directions

def get_unvisited_directions(room_directions):
    options = []
    for key, value in room_directions.items():
        if value == '?':
            options.append(key)
    return options

def get_visited_directions(room_directions):
    options = []
    for key, value in room_directions.items():
        if value != '?':
            options.append(key)
    return options

traversal_graph = {}
inverse_lookup = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
current_room = world.starting_room
traversal_graph[current_room.id] = {exit: '?' for exit in current_room.get_exits()}
while len(traversal_graph) < 500:
    # DFT - Loop "spelunk"
    spelunk = True
    while spelunk:
        options = get_unvisited_directions(traversal_graph[current_room.id])
        if len(options) > 0:
            # Getting our direction and counter direction
            dr = random.randrange(len(options))
            drx = options[dr]
            rdrx = inverse_lookup[drx]
            traversal_path.append(drx)

            # Assigning room values
            last_room = current_room
            current_room = current_room.get_room_in_direction(drx)

            # Updating our traversal graph
            traversal_graph[last_room.id][drx] = current_room
            traversal_graph[current_room.id] = {exit: '?' for exit in current_room.get_exits()}
            traversal_graph[current_room.id][rdrx] = last_room
        else:
            spelunk = False

    # BFT - Loop "traceback"
    q = Queue()
    q.enqueue([current_room])
    traceback = True
    while traceback:
        if len(traversal_graph) == 500: break
        # dequeue first path
        path = q.dequeue()
        # check if we found a room with unexplored area
        if len(get_unvisited_directions(traversal_graph[path[-1].id])) > 0:
            directions = convert_path_directionals(path)
            # append new direction inputs to traversal path
            for entry in directions:
                    traversal_path.append(entry)
            current_room = path[-1]
            traceback = False

        for key, value in traversal_graph[path[-1].id].items():
            if traceback == False: break

            new_path = list(path)
            new_path.append(value)
            q.enqueue(new_path)

            # check if we found a room with unexplored area
            if len(get_unvisited_directions(traversal_graph[value.id])) > 0:
                directions = convert_path_directionals(new_path)
                # append new direction inputs to traversal path
                for entry in directions:
                    traversal_path.append(entry)
                current_room = new_path[-1]
                traceback = False


        
print(traversal_path)
# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")





#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
