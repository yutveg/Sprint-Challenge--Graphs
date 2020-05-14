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
# world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


# Need to keep track of last room id
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

visited = set()
traversal_graph = {}
inverse_lookup = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
current_room = world.starting_room
traversal_graph[current_room.id] = {exit: '?' for exit in current_room.get_exits()}
visited.add(current_room)
while len(visited) < 500:
    # DFT - Loop "spelunk"
    spelunk = True
    while spelunk:
        options = get_unvisited_directions(traversal_graph[current_room.id])
        if len(options) > 0:
            # Getting our direction
            dr = random.randrange(len(options))
            drx = options[dr]
            rdrx = inverse_lookup[drx]
            traversal_path.append(drx)

            # Assigning room values
            last_room = current_room
            current_room = current_room.get_room_in_direction(drx)

            # Updating our traversal graph
            traversal_graph[last_room.id][drx] = current_room.id
            traversal_graph[current_room.id] = {exit: '?' for exit in current_room.get_exits()}
            traversal_graph[current_room.id][rdrx] = last_room.id
        else:
            spelunk = False

    # BFT - Loop "traceback"
    traceback = True
    while traceback:
        print(traversal_graph)
        

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
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
