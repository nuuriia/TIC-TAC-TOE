"""
Author: Jose L Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Text handling of a simple tic-tac-toe-like board, 2021.
Intended for Grau en Intel-ligencia Artificial, Programacio i Algorismes 1.
"""

# Import initialization of the separately programmed abstract board:
from abs_board_bot import set_board_up

# Prepare board:
# this will set up all stones as unplayed, select a first stone to play,
# and obtain functions to handle them as follows:
#   the call stones() allows one to loop on all stones,
#   the call select_st(i, j) marks as selected the stone at these coordinates,
#   the call move_st(i, j) 
#     if the square at these coordinates is free, moves the selected  
#     stone there, changes player, unselects the stone and checks for 
#     end of game; otherwise, does nothing, leaving the stone selected;
#     returns: bool "stone still selected", next player (may be the same), 
#     and bool "end of game"
#   the call to draw_txt(end) prints a text-based version of the board

botanswer=input('Select number of players (1 or 2): ')
bot= True if botanswer=='1' else False

stones, select_st, move_st, draw_txt, move_random_st, select_random_st= set_board_up(bot)

# set_board_up() already selects a first stone
stone_selected = True
# Loop until game ends
end = False
draw_txt(False)
curr_player=0

while not end:
    while not stone_selected:
        if bot and curr_player==1:
            i,j=select_random_st()
        else:
            i,j=input('Select sonte coordinates: ').split()
        stone_selected = select_st(int(i), int(j))
    while stone_selected and not end:
        if bot and curr_player==1:
            i,j=move_random_st()
        else:
            i,j =input('Select destination coordinates: ').split()
        stone_selected, curr_player, end = move_st(int(i), int(j))  
        draw_txt(end)
        if bot and curr_player==0:
            print('Bot has moved to', i, j)

# Wait for the user to look at the screen before ending the program.
input('\nGame over.')









