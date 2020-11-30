from qiskit import *
from enum import Enum
from qcatsweeper import qconfig

import qiskit
import math
import random
import quantumrandom as qr


class TileItems(Enum):
    BLANKS = 0

    GROUP1 = 1
    GROUP2 = -1
    GROUP3 = 2
    GROUP4 = -2
    GROUP5 = 3
    GROUP6 = -3

    BOMB_UNEXPLODED = 7
    BOMB_EXPLODED = 8

    REVEAL_GROUP = 9

    GOLDEN_CAT = 10

    POS_EVAL = 42
    NEG_EVAL = -42

    BOMB_DEFUSED = 84


real_device = False
shots = 1024

device = Aer.get_backend('qasm_simulator')
if real_device:
    IBMQ.save_account(qconfig.APItoken)
    IBMQ.load_account()
    provider = IBMQ.get_provider(hub='ibm-q')
    device = provider.get_backend('ibmq_qasm_simulator')


# qiskit.register(qconfig.APItoken, qconfig.config["url"])


def get_one_or_zero(grid_script, q, c):

    # measuring qubit and finding which value has the most outcomes
    grid_script.measure(q, c)
    results = execute(grid_script, device, shots=shots).result()
    results_counts = results.get_counts(grid_script)
    print("results_counts", results_counts)

    if len(results_counts) == 1:
        print("return 0")
        return 0
    if results_counts['0'] > results_counts['1']:
        print("return 0")
        return 0
    print("return 1")
    return 1


def new_game_grid(l, bomb_no=20):
    game_grid = [[TileItems.BLANKS for i in range(l)] for j in range(l)]

    # construct groups of numbers for tiles
    _cur = 0
    _index = [TileItems.GROUP1, TileItems.GROUP2, TileItems.GROUP3,
              TileItems.GROUP4, TileItems.GROUP5, TileItems.GROUP6]
    random.shuffle(_index)
    _groups = [[random.randint(0, 1) for i in range(l)] for i in range(l)]

    for y in range(0, l, 4):
        for x in range(0, l, 6):
            for _y in range(y, y + 4):
                for _x in range(x, x + 6):
                    if _groups[_y][_x] >= 1:
                        game_grid[_y][_x] = _index[_cur]
            _cur += 1

    # ANU quantum random number generator to generate 20 bomb positions
    # bomb_xy = qr.get_data(data_type='uint16', array_length=bomb_no * 2)
    bomb_xy = [int(random.randint(0, 64554)) for i in range(bomb_no * 2)]
    # bomb_xy = [int(get_bit_string(16), 2) for i in range(bomb_no * 2)]
    bomb_xy = list(map(lambda x: x % l, bomb_xy))
    # classical random number generator for debugging
    # bomb_xy = [random.randint(0, l-1) for i in range(bomb_no * 2)]
    bomb_xy = [bomb_xy[i:i + 2] for i in range(0, bomb_no * 2, 2)]

    for coord in bomb_xy:
        if len(coord) > 0:
            game_grid[coord[0]][coord[1]] = TileItems.BOMB_UNEXPLODED

    # golden Cat
    game_grid[random.randint(0, l - 1)][random.randint(0, l - 1)] = TileItems.GOLDEN_CAT

    return game_grid


def onclick(clicked_tile, num_clicks):
    """
    params:
    clicked_tile: tile type of the clicked tile
    num_click: number of times a group has been clicked
    """
    q = QuantumRegister(1)
    c = ClassicalRegister(1)
    gridScript =  QuantumCircuit(q, c, name='gridScript')

    if (clicked_tile == TileItems.BOMB_UNEXPLODED):
        # hadamard gate applied to bomb qubit
        gridScript.h(q)

        # if there are more 1 hits then the bomb expodes and the game is lost
        if get_one_or_zero(gridScript, q, c) == 1:
            return TileItems.BOMB_EXPLODED
        return TileItems.BOMB_DEFUSED

    else:
        return clicked_tile
