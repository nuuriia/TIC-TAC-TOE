"""
Author: Jose L Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Headers for functions in abstract board for simple tic-tac-toe-like games, 2021.
Intended for Grau en Intel-ligencia Artificial, Programacio i Algorismes 1.
I would prefer to do everything in terms of object-oriented programming though.
"""

# Import: 
# color GRAY; PLAYER_COLOR, NO_PLAYER
# board dimension BSIZ
import random
from constants import PLAYER_COLOR, BSIZ, NO_PLAYER, GRAY, ST_PLAYER, GAME_MODE

# Data structure for stones
from collections import namedtuple

Stone = namedtuple('Stone', ('x', 'y', 'color'))


def set_board_up(bot):
    'Init stones and board, prepare functions to provide, act as their closure'

    # init board and game data here
    board=[[' ' for _ in range(BSIZ)] for _ in range(BSIZ)]
    player1=input('Name player 1: ')
    if bot:
        player2='Bot'
    else:
        player2=input('Name player 2: ')
    curr_player=0 #player1=0 player2=1
    num_stones=0
    last_stone_selected=['','']
    last_stone_played=['','']

    def stones():
        "return iterable with the stones already played"
        return [Stone(x, y, PLAYER_COLOR[board[x][y]])for x in range(BSIZ) for y in range(BSIZ) if board[x][y] != ' ']


    def select_st(i, j):
        '''
        Select stone that current player intends to move. 
        Player must select a stone of his own.
        To be called only after all stones played.
        Report success by returning a boolean;
        '''
        nonlocal last_stone_selected
        
        if board[i][j]==curr_player:
            last_stone_selected=[i,j]
            return True
        else:
            print('You cannot select this stone')
            return False

    def end():
        'Test whether there are 3 aligned stones'
        i=last_stone_played[0]
        j=last_stone_played[1]
        
        #mirem la fila
        count=0
        for x in range(1,BSIZ):
            if board[i][j-x]==curr_player:
                count+=1
        if count==BSIZ-1:
            return True
        #mirem la columna
        count=0
        for x in range(1,BSIZ):
            if board[i-x][j]==curr_player:
                count+=1
        if count==BSIZ-1:
            return True
        #mirem una diagonal
        count=0
        for x in range(BSIZ):
            if board[x][x]==curr_player:
                count+=1
        if count==BSIZ:
            return True
        #mirem l'altre diagonal
        count=0
        for x in range(BSIZ):
            if board[x][BSIZ-1-x]==curr_player:
                count+=1
        if count==BSIZ:
            return True

        return False

    def move_st(i, j):
        '''If valid square, move there selected stone and unselect it,
        then check for end of game, then select new stone for next
        player unless all stones already played;
        if square not valid, do nothing and keep selected stone.
        Return 3 values: bool indicating whether a stone is
        already selected, current player, and boolean indicating
        the end of the game.
        '''
        nonlocal curr_player, num_stones, last_stone_selected, last_stone_played
        if board[i][j]==' ':
            board[i][j]=curr_player
            num_stones+=1
            if num_stones>=ST_PLAYER*2:
                if last_stone_selected==['','']:
                    last_stone_played=[i,j]
                    win=end()
                    curr_player=0 if curr_player==1 else 1
                    return False, curr_player, win    
                x=last_stone_selected[0]
                y=last_stone_selected[1]
                board[x][y]=' '
                num_stones-=1
                last_stone_played=[i,j]
                win=end()
                curr_player=0 if curr_player==1 else 1
                return False, curr_player, win
            last_stone_played=[i,j]
            win=end()
            curr_player=0 if curr_player==1 else 1
            return True, curr_player, win
        else:
            print('This square is not valid')
            return True, curr_player, False




    def draw_txt(end = False):
        'Use ASCII characters to draw the board.'
        print('—'+'————'*BSIZ)
        for i in range(BSIZ):
            print('| ', end='')
            for j in range(BSIZ):
                print(symbol(board[i][j])+' | ',end='')
            print('')
            print('—'+'————'*BSIZ)
        if end==True:
            if GAME_MODE=='CLASSIC':
                print(player1 if curr_player==1 else player2,'has won!! :)')
            elif GAME_MODE=='MISERY':
                print(player2 if curr_player==1 else player1,'has won!! :)')

    def symbol(player):
        if player==0:
            return 'X'
        elif player==1:
            return 'O'
        else:
            return ' '
        
    def move_random_st():
        nonlocal last_stone_played, curr_player
        empty_square=[]
        for i in range(BSIZ):
            for j in range(BSIZ):
                if board[i][j]==' ':
                    empty_square+=[[i,j]]

        for [i,j] in empty_square:
            board[i][j]=1
            last_stone_played=[i,j]
            if end():
                board[i][j]=' '
                return i,j
            board[i][j]=' '
        for [i,j] in empty_square:
            board[i][j]=0
            last_stone_played=[i,j]
            curr_player=0
            if end():
                board[i][j]=' '
                curr_player=1
                return i,j
            curr_player=1
            board[i][j]=' '

        square=random.choice(empty_square)
        return square
    
    def select_random_st():
        nonlocal last_stone_played, curr_player
        empty_square=[]
        for i in range(BSIZ):
            for j in range(BSIZ):
                if board[i][j]==' ':
                    empty_square+=[[i,j]]
        bot_stones=[]
        for i in range(BSIZ):
            for j in range(BSIZ):
                if board[i][j]==1:
                    bot_stones+=[[i,j]]
        
        for [i,j] in empty_square:
            board[i][j]=1
            last_stone_played=[i,j]
            if end():
                for [x,y] in bot_stones:
                    board[x][y]=' '
                    if end():
                        board[x][y]=1
                        board[i][j]=' '
                        return x,y
                    board[x][y]=1
                board[i][j]=' '              
            board[i][j]=' '
        critical_st=[]
        for [i,j] in bot_stones:
            board[i][j]=0
            last_stone_played=[i,j]
            curr_player=0
            if end():
                critical_st+=[[i,j]]
            curr_player=1
            board[i][j]=1
        bot_stones=[i for i in bot_stones if i not in critical_st]
        
        stone=random.choice(bot_stones)
        return stone
       
    # return these 4 functions to make them available to the main program
    return stones, select_st, move_st, draw_txt, move_random_st, select_random_st

