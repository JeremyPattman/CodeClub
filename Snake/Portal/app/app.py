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
    sq.update( {'fillStyle': '#01786F'} )
    squares.append(sq)

def createPlayArea(squares):
    for y in range(PLAY_AREA_HEIGHT):
        for x in range(PLAY_AREA_WIDTH):
            addSquare(squares,x,y,BLOCK_SIZE,1)

@app.route('/', methods=['GET', 'POST'])
def mainpage():

    squares=[]
    createPlayArea(squares)

    return render_template('index.html', squares=squares)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
