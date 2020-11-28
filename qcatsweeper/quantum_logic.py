from qiskit import QuantumProgram
from enum import Enum
from qcatsweeper import qconfig

import qiskit
import math
import random
import quantumrandom as qr


class TileItems(Enum):
    BLANKS = 0

    TILE1 = 1
    TILE2 = 2
    TILE3 = 3
    TILE4 = 4
    TILE5 = 5
    TILE6 = 6
    TILE7 = 7
    TILE8 = 8

    BOMB_UNEXPLODED = 9
    BOMB_EXPLODED = 10

    #REVEAL_GROUP = 9

    GOLDEN_CAT = 11
    FLAG = 12

    POS_EVAL = 42
    NEG_EVAL = -42

    BOMB_DEFUSED = 84


real_device = False
shots = 1024

device = 'local_qasm_simulator'
if real_device:
    device = 'ibmqx4'

Q_program = QuantumProgram()


# qiskit.register(qconfig.APItoken, qconfig.config["url"])


def get_one_or_zero(grid_script, q, c, index):
    global Q_program
    # measuring qubit and finding which value has the most outcomes
    grid_script.measure(q[index], c[index])
    results = Q_program.execute(
        ["gridScript"], backend=device, shots=shots, timeout=1800)
    re = results.get_counts("gridScript")
    d1 = list(map(lambda x: (x[0], x[1], x[0].count('0')), re.items()))
    d2 = sorted(d1, key=lambda x: x[2], reverse=True)

    print(d2)
    if d2[0][1] > d2[1][1]:
        return 0
    return 1


def new_game_grid(grid_size, bomb_no=20):
    game_grid = [[TileItems.BLANKS for i in range(grid_size)] for j in range(grid_size)]

    # construct groups of numbers for tiles
    _cur = 0
    _tiles = [TileItems.TILE1, TileItems.TILE2, TileItems.TILE3, TileItems.TILE4,
              TileItems.TILE5, TileItems.TILE6, TileItems.TILE7, TileItems.TILE8]
    print(_tiles)
    #_index = [TileItems.GROUP1, TileItems.GROUP2, TileItems.GROUP3,
    #          TileItems.GROUP4, TileItems.GROUP5, TileItems.GROUP6]
    #random.shuffle(_tiles)
    #_groups = [[random.randint(0, 1) for i in range(l)] for i in range(l)]

    #for y in range(0, l, 4):
    #    for x in range(0, l, 6):
    #        for _y in range(y, y + 4):
    #            for _x in range(x, x + 6):
    #                if _groups[_y][_x] >= 1:
    #                    game_grid[_y][_x] = _index[_cur]
    #        _cur += 1

    # Quantum ANU random number generator to generate 20 bomb positions
    #bomb_xy = [int(random.randint(0, 64554)) for i in range(bomb_no * 2)]
    #bomb_xy = list(map(lambda x: x % grid_size, bomb_xy))
    # classical random number generator for debugging
    bomb_xy = [random.randint(0, grid_size-1) for i in range(bomb_no * 2)]
    bomb_xy = [bomb_xy[i:i + 2] for i in range(0, bomb_no * 2, 2)]

    for coord in bomb_xy:
        if len(coord) > 0:
            game_grid[coord[0]][coord[1]] = TileItems.BOMB_UNEXPLODED

    # golden Cat
    game_grid[random.randint(0, grid_size - 1)][random.randint(0, grid_size - 1)] = TileItems.GOLDEN_CAT

    return game_grid


def onclick(clicked_tile, num_clicks):
    """
    params:
    clicked_tile: tile type of the clicked tile
    num_click: number of times a group has been clicked
    """
    q = Q_program.create_quantum_register("q", 5)
    c = Q_program.create_classical_register("c", 5)
    gridScript = Q_program.create_circuit("gridScript", [q], [c])

    if (clicked_tile == TileItems.BOMB_UNEXPLODED):
        # hadamard gate applied to bomb qubit
        gridScript.h(q[0])

        # if there are more 1 hits then the bomb expodes and the game is lost
        if get_one_or_zero(gridScript, q, c, 0) == 1:
            return TileItems.BOMB_EXPLODED
        return TileItems.BOMB_DEFUSED

    elif (clicked_tile == TileItems.BLANKS):
        return TileItems.BLANKS


    """elif (clicked_tile == TileItems.GROUP1 or clicked_tile == TileItems.GROUP2):  # 1 click
        # half not gate applied to the 1 click number tiles
        gridScript.u3(0.5 * math.pi, 0.0, 0.0, q[1])

        # if more 1 hits then the whole tile group is revealed
        if get_one_or_zero(gridScript, q, c, 1) == 1:
            return TileItems.REVEAL_GROUP
        return TileItems.NEG_EVAL

    elif (clicked_tile == TileItems.GROUP3 or clicked_tile == TileItems.GROUP4):  # 2 clicks
        if num_clicks == 1:
            gridScript.u3(0.5 * math.pi, 0.0, 0.0, q[2])

            if get_one_or_zero(gridScript, q, c, 2) == 1:
                return TileItems.POS_EVAL
            return TileItems.NEG_EVAL

        elif num_clicks == 2:
            gridScript.u3(0.5 * math.pi, 0.0, 0.0, q[2])

            if get_one_or_zero(gridScript, q, c, 2) == 1:
                return TileItems.REVEAL_GROUP
            return TileItems.NEG_EVAL

    elif (clicked_tile == TileItems.GROUP5 or clicked_tile == TileItems.GROUP6):  # 3 clicks
        if num_clicks == 1:
            gridScript.u3(0.5 * math.pi, 0.0, 0.0, q[3])

            if get_one_or_zero(gridScript, q, c, 3) == 1:
                return TileItems.POS_EVAL
            return TileItems.NEG_EVAL

        elif num_clicks == 2:
            gridScript.u3(0.5 * math.pi, 0.0, 0.0, q[3])

            if get_one_or_zero(gridScript, q, c, 3) == 1:
                return TileItems.POS_EVAL
            return TileItems.NEG_EVAL

        elif num_clicks == 3:
            gridScript.u3(0.5 * math.pi, 0.0, 0.0, q[3])

            if get_one_or_zero(gridScript, q, c, 3) == 1:
                return TileItems.REVEAL_GROUP
            return TileItems.NEG_EVAL"""

    return None
