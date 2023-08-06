# Slacker

Slacker is a clone/parody of the popular arcade game [Stacker], in which
you must stack blocks to the top of the screen in order to win the game.
Boxes will move back and forth at varying speeds.  Press Space
to stop the boxes and move on to the next row.  Only boxes that have
something underneath them will be stacked.  As the tower rises, the game
will make your tower thinner.  You win a minor prize at the 10th level
(the blocks change color), and if you reach the 15th level, you will win
the major prize.  Good luck!

This game and the above description was originally written by Clint
and Jennifer Herron.  I forked the game to improve the codebase,
make it more similar to the arcade game and hopefully add more features.

## Installation

Slacker can run on Python 3.7 or above.  You can install it using `pip`.

## Control

* Space: Start playing or place your stacking boxes.
* Escape or `q`: Return to intro screen or quit.
* `1` to `9`: Set the speed of the game (default: 5).
* `0`: Increase the number of blocks currently moving.

## Credits

* [Original version] by Clint "HanClinto" Herron (coding)
  and Jennifer Herron (graphics)
* [VT323 font] by Peter Hull and Jacques Le Bailly
* [Tango color palette] by the Tango Desktop Project

[Stacker]: https://en.wikipedia.org/wiki/Stacker_(arcade_game)
[Original version]: http://www.pyweek.org/e/LastMinute
[VT323 font]: https://github.com/phoikoi/VT323
[Tango color palette]: https://en.wikipedia.org/wiki/Tango_Desktop_Project#Palette
