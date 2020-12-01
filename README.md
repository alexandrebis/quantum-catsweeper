# Quantum Cat-sweeper

This is an almost regular Minesweeper that runs on the [IBM Quantum computer](https://quantumexperience.ng.bluemix.net/qx/experience) or simulator. 

# Rules of the game:
- Click with the left mouse button to discover tiles
- The number on tiles indicates how many bombs is around the tile you clicked
- Don't explode the cats (bombs), they have 50% chance of exploding (may the quantum randomness be in you favor !)
- To win the game, find the golden kitty (who moves based on whether you reveal a tile that isn't a bomb !)

![Front Screen](https://github.com/desireevl/quantum-catsweeper/blob/master/images/mainscreen.PNG)

## Game Over
![Game Over](https://github.com/alexandrebis/quantum-catsweeper/blob/feature/flag-and-tiles/images/lost.png)

## Game Won
![Game Over](https://github.com/alexandrebis/quantum-catsweeper/blob/feature/flag-and-tiles/images/won.PNG)

# Technical Explanation

## Cat Bombs
A Hadamard gate is used on the qubit that represents the bomb and when the tile is clicked, the qubit is measured. It has a 50/50 chance of evaluating to a 1 (bomb explodes) or a 0 (bomb defuses).

## Golden Cat
The golden cat moves around based on your click. If you find it, you win 100% of the time. 

If you click on a tile that is not an exploding bomb nor a blank tile (number tile, defused cat) then the golden cat moves one space in the direction of the tile you just clicked.

If a negatively evaluated bomb is clicked, the golden cat moves one space away.

This knowledge can be used as strategy to win the game. 

# install and launching Guide

Note : The current Qiskit dependency version is a really old version = 0.5.7. To update the version, you must modify the existing code and use up-to-date equivalents. For example, QuantumProgram is deprecated, you must now separately create a circuit and launch the `execute(circuit, backend)` method. [Source](https://qiskit.org/documentation/release_notes.html)

Python 3 is needed

(Optional but strongly recommended) set up a venv with the command :
```bash
python -m venv venv
source venv/Scripts/activate
```

Install the dependencies with :
```bash
pip install -r requirements.txt
``` 

As a temporary workaround, you have to modify your qiskit dependency manually.

Go to : `\venv\lib\site-packages\qiskit\dagcircuit\` and replace all occurences of `.node[` with `._node[` in the following files :
- _dagcircuit.py
- _dagunroller.py

Launch with :
```bash
python main.py
python main.py debug # For debugging mode
```
