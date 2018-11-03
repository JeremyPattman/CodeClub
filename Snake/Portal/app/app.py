from flask import Flask, request, render_template

squares=[
    {
	'fillStyle': '#01786F',
	'x': 100,
	'y': 100,
	'len': 10
	}
]

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def mainpage():
        return render_template('index.html', squares=squares)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
