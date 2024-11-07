# onyx

A simple implementation of the Onyx board game created by @DancingGrumpyCat.


## Rules

Onyx is played on a board with spaces connected by edges. Each player uses two colors of pieces, and the objective is to control the most territory with both colors.


## Turns

On your turn, you may place up to 2 pieces. You may only place pieces on a space if the space is both empty and not surrounded. If you place 0 pieces, you have passed, which we will reference later. If you place 1 piece, it may be of either of your colors. If you place 2 pieces, either place two pieces of the *same* color on the *same* space (creating a stack of pieces), or two pieces of *different* colors on two *different* spaces. You can't place two pieces of the same color on two different spaces.


### Move Legality

A move is only legal if it is empty and not surrounded. A space is empty if it does not contain any pieces. A space is surrounded depending on the color of the piece to be placed there—if its neighboring spaces contain at least three pieces that are not that color, it is surrounded.


### Suffocation

After placing pieces for your turn, if you surround any pieces, suffocate them (remove them from the board). Multiple pieces can be suffocated, including those of your colors, but no piece that has just been placed can be suffocated.


## End of the game

After you have passed at least once, if your opponent passes, the game ends and goes to scoring.


### Scoring

Before scoring begins, asynchronously, each player may remove any of their stacks of pieces. Removing stacks may increase your score due to the following rules.

Each player scores a combination of their colors' scores, and the second player scores an additional 5 points. Score once for the color with the greater score and twice for the color with the lesser score.

#### Scoring a color

Each color scores 1 point for every space occupied or controlled by that color.


### Occupation

A non-empty space is occupied by a color if at least one piece of that color is on the space.


### Control

An empty space is controlled by a color if there is a contiguous set of empty spaces connecting to a space occupied by that color.

