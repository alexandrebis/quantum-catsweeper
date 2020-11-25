# Quantum Cat-sweeper

This is a super simple game loosely based on Minesweeper Flags and runs on the [IBM Quantum computer](https://quantumexperience.ng.bluemix.net/qx/experience) or simulator. 

# Rules of the game:
- Don't explode the cat (bombs)
- The tile numbers indicate the number of times you need to click on the same colour to reveal the whole group
- If a tile has an ! at the end that means quantum probability was not in your favour and that tile click does not count
- To win the game, find the golden kitty (who moves based on whether you reveal a ! or normal tile)

![Front Screen](https://github.com/desireevl/quantum-catsweeper/blob/master/images/mainscreen.PNG)

## Game Page
![Game Screen](https://github.com/desireevl/quantum-catsweeper/blob/master/images/playin.PNG)

## Game Over
![Game Over](https://github.com/desireevl/quantum-catsweeper/blob/master/images/lost.png)

# How to play

You click with the left arrow.

# Explanation
The placement of the bombs are determined using the [ANU Quantum Random Number Generator](https://qrng.anu.edu.au/). A Hadamard gate is used on the qubit that represents the bomb and when the tile is clicked, the qubit is measured. It has a 50/50 chance of evaluating to a 1 (bomb explodes) or a 0 (bomb defuses).

A half NOT gate is applied to each qubit representing a number tile. For example: if you reveal a purple 3 tile, you need to click two more purple 3 tiles before the whole purple section reveals. For each click there is a 50/50 chance of the qubit evaluating to a 1 or 0. If out of the 1024 shots, more of them are 1, then your click counts and you only need to find one more purple tile before the whole group reveals. If there are more 0's, then your click does not count and you still need two more clicks of a purple tile to reveal the group. 

The golden cat moves around based on your click. If you find it you win 100% of the time. If you reveal a tile with a positive (not !) or neutral evaluation (defused bombs, blank tiles) then the cat moves one space in the direction of the tile you just clicked. If a negatively evaluated tile is clicked the golden cat moves one space away. This knowledge can be used as strategy to win the game. 

# Installation and launching Guide

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


# Changelog

## Last Version

### Changes

Commented the `qiskit.register()` method
Changed the order of initialization of window
Move `images` location
Lowered the sound and disabled the loop of the main music
Changed `LEFT_KEY_BUTTON` to `LEFT_KEY`, then to `LEFT_MOUSE_BUTTON` because why use the left arrow?
Replace quantum random by regular random and remove it from requirements
Set `pyxel.mouse(True)` to see the cursor
Remove IBMQ dependencies as it is not used
Set last working numpy version
Update README

### Changes ideas

Use one of the IBM Quantum backends
Use a more recent version of Qiskit
Implement real minesweeper logic
Correctly size the window