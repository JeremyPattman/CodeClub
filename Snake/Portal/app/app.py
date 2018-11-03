from flask import Flask, request, render_template




app = Flask(__name__)

def addSquare(squares, x,y,type):
    sq = {}
    sq.update( {'x' : x} )
    sq.update( {'y' : y} )
    sq.update( {'len' : 10} )
    sq.update( {'fillStyle': '#01786F'} )
    squares.append(sq)

@app.route('/', methods=['GET', 'POST'])
def mainpage():

    squares=[]
    addSquare(squares,0,0,1)
    addSquare(squares,10,0,1)
    addSquare(squares,30,0,1)

    return render_template('index.html', squares=squares)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
