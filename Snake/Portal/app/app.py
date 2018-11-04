from flask import Flask, request, render_template

BLOCK_SIZE = 5
PLAY_AREA_WIDTH = 60
PLAY_AREA_HEIGHT= 30

app = Flask(__name__)

def addSquare(squares,x,y,len,type):
    sq = {}
    sq.update( {'x' : x*len} )
    sq.update( {'y' : y*len} )
    sq.update( {'len' : len} )
    if type == 1:
        sq.update( {'fillStyle': '#BF4F51'} )
    else:
        sq.update( {'fillStyle': '#01786F'} )

    squares.append(sq)

def createPlayArea(squares):
    for y in range(PLAY_AREA_HEIGHT):
        for x in range(PLAY_AREA_WIDTH):
            if x==0 or x==(PLAY_AREA_WIDTH-1) or y==0 or y==(PLAY_AREA_HEIGHT-1):
                addSquare(squares,x,y,BLOCK_SIZE,1)
            else:
                addSquare(squares,x,y,BLOCK_SIZE,0)

@app.route('/', methods=['GET', 'POST'])
def mainpage():

    displaySquares=[]
    createPlayArea(displaySquares)

    return render_template('index.html', squares=displaySquares)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
