import random
from enum import Enum
from qcatsweeper import qconfig
from qiskit import *


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
    TILE_NUMBERS = [TILE1, TILE2, TILE3, TILE4, TILE5, TILE6, TILE7, TILE8]

    BOMB_UNEXPLODED = 9
    BOMB_EXPLODED = 10

    GOLDEN_CAT = 11
    FLAG = 12

    POS_EVAL = 42
    NEG_EVAL = -42

    BOMB_DEFUSED = 84


real_device = True
shots = 1024

if real_device:
    try:
        IBMQ.save_account(qconfig.APItoken, overwrite=True)
        IBMQ.load_account()
        provider = IBMQ.get_provider(hub='ibm-q')
        device = provider.get_backend('ibmq_qasm_simulator')
    except qiskit.providers.ibmq.api.exceptions.RequestsApiError:
        print("Could not load IBMQ account. Using local qasm_simulator.\nError : ", sys.exc_info()[1])
        device = Aer.get_backend('qasm_simulator')
else:
    device = Aer.get_backend('qasm_simulator')


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


def new_game_grid(grid_size, bomb_no=20):
    game_grid = [[TileItems.BLANKS for i in range(grid_size)] for j in range(grid_size)]

    # classical random number generator for debugging
    bomb_xy = [random.randint(0, grid_size-1) for i in range(bomb_no * 2)]
    bomb_xy = [bomb_xy[i:i + 2] for i in range(0, bomb_no * 2, 2)]
    # add Bombs
    for coord in bomb_xy:
        if len(coord) > 0:
            game_grid[coord[0]][coord[1]] = TileItems.BOMB_UNEXPLODED

    # add number Tiles
    game_grid = add_number_tiles(game_grid, grid_size)

    # add golden Cat
    game_grid[random.randint(0, grid_size - 1)][random.randint(0, grid_size - 1)] = TileItems.GOLDEN_CAT

    return game_grid


def add_number_tiles(game_grid: list, grid_size: int):
    for row in range(len(game_grid)):
        for col in range(len(game_grid[row])):
            if game_grid[row][col] != TileItems.BOMB_UNEXPLODED and game_grid[row][col] != TileItems.GOLDEN_CAT:
                number = number_of_bombs(row, col, game_grid, grid_size) # Compte les bombes autour (le "gros" du code)
                if number > 0:
                    game_grid[row][col] = TileItems['TILE' + str(number)]

    return game_grid


def number_of_bombs(row, col, game_grid, grid_size: int):
    # if  row == 0 and col == 0: #coin haut et gauche
    bombs = 0

    # On parcourt toutes les cases autours
    for y in range(row - 1, row + 2):
        for x in range(col - 1, col + 2):
            if (y >= 0) and (y < grid_size) and (x >= 0) and (x < grid_size): # Si la case existe
                if game_grid[y][x] == TileItems.BOMB_UNEXPLODED: # Si la case est une bombe
                    bombs += 1
    return bombs


def onclick(clicked_tile):
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
