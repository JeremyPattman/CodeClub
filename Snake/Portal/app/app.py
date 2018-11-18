from flask import Flask, request, render_template
import random

# currently using <meta http-equiv="refresh" content="5"> in the html header to
# force a refresh from the client.  My look better if I use async updates instead
# https://www.shanelynn.ie/asynchronous-updates-to-a-webpage-with-flask-and-socket-io/

BLOCK_SIZE = 5
PLAY_AREA_WIDTH = 60
PLAY_AREA_HEIGHT= 30
GROW_FREQUENCY = 3


app = Flask(__name__)

################################################################################
# Code in this section is for the player AI. This will eventually sit in
# separate containers. one for each snake player.
################################################################################

# decide if the identified snake needs to move up, down, left or right for its
# next move. The whole of the current game board is passed as gameBoard and the
# snake to control is idenified by snakeID.  In the gameBoard walls are
# identified by 1.0, empty squares are identified by 0.0 and all other squares
# contain snakes. The head of a snake is n.1 and the body is n where n >= 2
# every snake has a different id represented by n.

def findHead(snakeID, gameBoard):
    width = len(gameBoard)
    height = len(gameBoard[0])

    # find the head of the snake
    for y in range(PLAY_AREA_HEIGHT):
        for x in range(PLAY_AREA_WIDTH):
            if(gameBoard[x][y] == (snakeID+0.1)):
                return x,y

    return -1,-1

def moveSnake(snakeID, gameBoard):
    # simple test algo to just move the snake
    snakeX, snakeY = findHead(snakeID,gameBoard)

    if(snakeX != -1 and snakeY != -1):
        if(gameBoard[snakeX+1][snakeY] == 0.0):
            return 1,0
        elif(gameBoard[snakeX-1][snakeY] == 0.0):
            return -1,0
        elif(gameBoard[snakeX][snakeY+1] == 0.0):
            return 0,1
        else:
            return 0,-1
    else:
        return 0,0


################################################################################
# Code in this section is for managing the game board and the players in memory
################################################################################
gameBoardMemoryMap = [[0.0 for y in range(PLAY_AREA_HEIGHT)] for x in range(PLAY_AREA_WIDTH)]
growCount = 0
snake1 = [(25,25),(26,24),(27,24),(28,24),(28,23)]
snake2 = [(30,25),(29,25),(29,26),(28,26),(28,27)]

def updateGameBoardMemoryMap():
    global growCount
    growCount = growCount + 1
    grow = False
    if growCount == GROW_FREQUENCY:
        growCount = 0;
        grow = True

    # determine how to move each snake
    xOffset, yOffset = moveSnake(2.0, gameBoardMemoryMap)
    if(xOffset!=0 or yOffset!=0):
        snake1.insert(0,(snake1[0][0]+xOffset,snake1[0][1]+yOffset))
        if not grow:
            snake1.pop()

    xOffset, yOffset = moveSnake(3.0, gameBoardMemoryMap)
    if(xOffset!=0 or yOffset!=0):
        snake2.insert(0,(snake2[0][0]+xOffset,snake2[0][1]+yOffset))
        if not grow:
            snake2.pop()

    # reset the game board memory map
    for y in range(PLAY_AREA_HEIGHT):
        for x in range(PLAY_AREA_WIDTH):
            if x==0 or x==(PLAY_AREA_WIDTH-1) or y==0 or y==(PLAY_AREA_HEIGHT-1):
                gameBoardMemoryMap[x][y] = 1.0
            else:
                gameBoardMemoryMap[x][y] = 0.0

    # add the snakes back in
    for s in range(len(snake1)):
        if s==0:
            gameBoardMemoryMap[snake1[s][0]][snake1[s][1]] = 2.1
        else:
            gameBoardMemoryMap[snake1[s][0]][snake1[s][1]] = 2.0

    for s in range(len(snake2)):
        if s==0:
            gameBoardMemoryMap[snake2[s][0]][snake2[s][1]] = 3.1
        else:
            gameBoardMemoryMap[snake2[s][0]][snake2[s][1]] = 3.0

################################################################################
# Code in this section is for converting the in-memory game board into a
# format that can be processed by Django code into a web browser visualisation
################################################################################

# add a square to the display board
def addSquare(squares,x,y,len,type):
    sq = {}
    sq.update( {'x' : x*len} )
    sq.update( {'y' : y*len} )
    sq.update( {'len' : len} )
    if type == 1.0:
        sq.update( {'fillStyle': '#000000'} )
    elif type == 2.1:
        sq.update( {'fillStyle': '#FD0E35'} )
    elif type == 2.0:
        sq.update( {'fillStyle': '#FE6F5E'} )
    elif type == 3.1:
        sq.update( {'fillStyle': '#2243B6'} )
    elif type == 3.0:
        sq.update( {'fillStyle': '#50BFE6'} )
    else:
        sq.update( {'fillStyle': '#01786F'} )

    squares.append(sq)

# create the display for the game board
def createGameBoardDisplayMap(gameBoard, squares):
    for y in range(PLAY_AREA_HEIGHT):
        for x in range(PLAY_AREA_WIDTH):
            addSquare(squares,x,y,BLOCK_SIZE,gameBoard[x][y])

# generate the display game board and that will be passed to the Django Code
# to generate the front end in browser
@app.route('/', methods=['GET', 'POST'])
def mainpage():

    updateGameBoardMemoryMap()

    displaySquares=[]
    createGameBoardDisplayMap(gameBoardMemoryMap, displaySquares)
    return render_template('index.html', squares=displaySquares)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
