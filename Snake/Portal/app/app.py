from flask import Flask, request, render_template
import random

# currently using <meta http-equiv="refresh" content="5"> in the html header to
# force a refresh from the client.  My look better if I use async updates instead
# https://www.shanelynn.ie/asynchronous-updates-to-a-webpage-with-flask-and-socket-io/

BLOCK_SIZE = 5
PLAY_AREA_WIDTH = 60
PLAY_AREA_HEIGHT= 30

app = Flask(__name__)

gameBoardMemoryMap = [[0.0 for y in range(PLAY_AREA_HEIGHT)] for x in range(PLAY_AREA_WIDTH)]


# manage the memory map for the game board and the pieces on it
def createGameBoardMemoryMap():
    for y in range(PLAY_AREA_HEIGHT):
        for x in range(PLAY_AREA_WIDTH):
            if x==0 or x==(PLAY_AREA_WIDTH-1) or y==0 or y==(PLAY_AREA_HEIGHT-1):
                gameBoardMemoryMap[x][y] = 1.0
            elif random.randint(0,2) == 0:
                gameBoardMemoryMap[x][y] = 2.0
            else:
                gameBoardMemoryMap[x][y] = 0.0

# add a square to the display board
def addSquare(squares,x,y,len,type):
    sq = {}
    sq.update( {'x' : x*len} )
    sq.update( {'y' : y*len} )
    sq.update( {'len' : len} )
    if type == 1:
        sq.update( {'fillStyle': '#BF4F51'} )
    elif type == 2.0:
        sq.update( {'fillStyle': '#FFEB00'} )
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

    displaySquares=[]
    createGameBoardMemoryMap()
    createGameBoardDisplayMap(gameBoardMemoryMap, displaySquares)
    return render_template('index.html', squares=displaySquares)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
