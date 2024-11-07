# onyx

A simple implementation of the Onyx board game created by @DancingGrumpyCat.


## Rules

Onyx is played on a board with spaces connected by edges. Each player uses two colors of pieces, and the objective is to control the most territory with both colors.


## Turns

On your turn, you may place up to 2 pieces. You may only place pieces on a space if that space is legal. If you place 0 pieces, you have passed, which we will reference later. If you place 1 piece, it may be of either of your colors. If you place 2 pieces, either place two pieces of the *same* color on the *same* space (creating a stack of pieces) or two pieces of *different* colors on two *different* spaces. You can't place two pieces of the same color on two different spaces.


### Move Legality

A move is only legal if it is neither occupied nor surrounded. A space is occupied if it contains at least one piece. A space is surrounded depending on the piece to be placed there—if its neighboring spaces contain at least three pieces that are not that piece's color, it is surrounded.


### Suffocation

After placing pieces for your turn, if you surround any pieces, suffocate them (remove them from the board). Multiple pieces can be suffocated, including those of your colors, but no piece that has just been placed can be suffocated.


#### Suffocation Examples

Key:
- · is an empty space
- a lowercase letter of {w, b, y, p} is a single white, black, yellow, or purple piece
- an uppercase letter of {w, b, y, p} is a stack of white, black, yellow, or purple pieces
- round brackets surround the piece(s) just placed

```
   w         ·
  / \    -> / \ 
(B)- b     B - b
```
```
   w         w
  / \    -> / \ 
 B - w     · - w
  \ /    -> \ /
  (w)        w
```
```
   w         w
  / \    -> / \ 
 Y - w     · - w
  \ /    -> \ /
  (w)        w
```
```
   w         ·
  / \    -> / \ 
(B)- y     B - ·
```
```
  (w)        w
  / \    -> / \ 
 B -(y)    · - y
```


## End of the game

After you have passed at least once, if your opponent passes, the game ends and goes to scoring.


### Scoring

Before scoring begins, asynchronously, each player may remove any of their stacks of pieces. Removing stacks may increase your score due to the following rules.

Each player scores a combination of their colors' scores, and the second player scores an additional 5 points. Score once for the color with the greater score and twice for the color with the lesser score—so if you were the second player and your color's scores were 25 and 21, your score would be 25 * 1 + 21 * 2 + 5 = 72.

Each color scores 1 point for every space that it occupies or controls.

The player with the higher score wins.


### Occupation

A non-empty space is occupied by a color if at least one piece of that color is on the space.


### Control

An empty space is controlled by a color if there is a contiguous set of empty spaces connecting to a space occupied by that color.

