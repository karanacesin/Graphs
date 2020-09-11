from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "Graphs/projects/adventure/maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
prev_dir = {'n':'s', 's':'n', 'w':'e', 'e':'w'}
seen = {}


def dft(current, prev = None):

    while len(seen) < len(room_graph):
        room = current
        exits = {}
        room_exits = player.current_room.get_exits()

        if room not in seen:
         
            for exit in room_exits:
                exits[exit] = '?'
                seen[room] = exits
        else:
            exits = seen[room]

        if prev is not None:
            direction = traversal_path[-1]
            seen[room][prev_dir[direction]] = prev
            seen[prev][direction] = room


        if '?' in seen[room].values():
            not_seen = [exit for exit in room_exits if exit == '?']

            if len(not_seen) != 0:
                travels = random.choice(list(not_seen))
                traversal_path.append(travels)
                player.travel(travels)

                dft(player.current_room.id, room)

        else:
            last_room = bfs(room)

            if last_room:
                cur_room = last_room[0]

                while len(last_room) > 1:
                    for direction in seen[last_room[0]]:
                        if seen[last_room[0]][direction] == last_room[1]:
                            traversal_path.append(direction)
                            player.travel(direction)
                            cur_room = last_room.pop()
                            break
                
                dft(player.current_room.id, cur_room)



def bfs(start):
    q = [[start]]
    visited = set()

    while len(q) > 0:
        path = q.pop(0)
        cur_room = path[-1]

        if cur_room not in visited:
            visited.add(cur_room)

            if '?' in seen[cur_room].values():
                return path

            for direction in seen[cur_room].values():
                new_path = list(path)
                new_path.append(direction)
                q.append(new_path)

dft(player.current_room.id)
print(f'PATH: {traversal_path}')


# TRAVERSAL TEST
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
