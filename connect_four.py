import numpy as np
import pygame
import sys
import math
BLUE=(0,0,255)
BLACK=(0,0,0)
RED=(255,0,0)
YELLOW=(255,255,0)
ROW_COUNT=6
COL_COUNT=7
def create_board():
    board=np.zeros((ROW_COUNT,COL_COUNT))
    return board

def drop_piece(board,row,col,piece):
    board[row][col]=piece

def is_valid(board,col):
    return board[ROW_COUNT-1][col]==0

def get_next_open_row(board,col):
    for r in range(ROW_COUNT):
        if board[r][col]==0:
            return r
def print_board(board):
    print(np.flip(board,0)) #flips the board along 0 axis
def check_win(board, piece):
    for r in range(ROW_COUNT):
        for c in range(COL_COUNT):
            # Check for horizontal win
            if c + 3 < COL_COUNT and board[r][c] == board[r][c + 1] == board[r][c + 2] == board[r][c + 3] == piece:
                return True
            # Check for vertical win
            if r + 3 < ROW_COUNT and board[r][c] == board[r + 1][c] == board[r + 2][c] == board[r + 3][c] == piece:
                return True
            # Check for diagonal win (positive slope)
            if c + 3 < COL_COUNT and r + 3 < ROW_COUNT and board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] == board[r + 3][c + 3] == piece:
                return True
            # Check for diagonal win (negative slope)
            if c + 3 < COL_COUNT and r - 3 >= 0 and board[r][c] == board[r - 1][c + 1] == board[r - 2][c + 2] == board[r - 3][c + 3] == piece:
                return True
    return False

def draw_board(board):
    for r in range(ROW_COUNT):
        for c in range(COL_COUNT):
            pygame.draw.rect(screen,BLUE,(c*SQUARESIZE,(r+1)*SQUARESIZE,SQUARESIZE,SQUARESIZE))
            pygame.draw.circle(screen,BLACK,(int(c*SQUARESIZE+SQUARESIZE/2),int((r+1)*SQUARESIZE+SQUARESIZE/2)),RADIUS)
    for r in range(ROW_COUNT):
        for c in range(COL_COUNT):
            if board[r][c]==1:
                pygame.draw.circle(screen,RED,(int(c*SQUARESIZE+SQUARESIZE/2),height-int(r*SQUARESIZE+SQUARESIZE/2)),RADIUS)
            elif board[r][c]==2:
                pygame.draw.circle(screen,YELLOW,(int(c*SQUARESIZE+SQUARESIZE/2),height-int(r*SQUARESIZE+SQUARESIZE/2)),RADIUS)         
    pygame.display.update()

board=create_board()
game_over=False
turn=0

pygame.init()

SQUARESIZE=100

RADIUS=int(SQUARESIZE/2 - 5)

width=COL_COUNT*SQUARESIZE
height=(ROW_COUNT+1)*SQUARESIZE

size=(width,height)

screen=pygame.display.set_mode(size)

draw_board(board)
FONT=pygame.font.SysFont("monospace",75)
pygame.display.update()

while not game_over:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        if event.type==pygame.MOUSEMOTION:
            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE))
            posx=event.pos[0]
            if turn==0:
                pygame.draw.circle(screen,RED,(posx,int(SQUARESIZE/2)),RADIUS)
            if turn==1:
                pygame.draw.circle(screen,YELLOW,(posx,int(SQUARESIZE/2)),RADIUS)
            pygame.display.update()
        if event.type==pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE))
            if turn==0:
                posx=event.pos[0]
                col=int(math.floor(posx/SQUARESIZE))
                if is_valid(board,col):
                    row=get_next_open_row(board,col)
                    drop_piece(board,row,col,1)
                    if check_win(board,1):
                        label=FONT.render("Player 1 wins!!! Congrats!!!",1,RED)
                        screen.blit(label,(40,10))
                        game_over=True
            else:
                posx=event.pos[0]
                col=int(math.floor(posx/SQUARESIZE))
                if is_valid(board,col):
                    row=get_next_open_row(board,col)
                    drop_piece(board,row,col,2)
                    if check_win(board,2):
                        label=FONT.render("Player 2 wins!!! Congrats!!!",1,YELLOW)
                        screen.blit(label,(40,10))
                        game_over=True
            turn=1-turn
            print_board(board) 
            draw_board(board)
            if game_over:
                pygame.time.wait(3500)