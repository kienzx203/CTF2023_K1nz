from flask import Flask, request, render_template
import advocate
import requests

app = Flask(__name__)
flag = open('flag.txt', 'r').read()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        r = requests.get(url)
        return render_template('index.html', result=r.text)
    return render_template('index.html')


@app.route('/flag')
def flag_page():
    if request.remote_addr == '127.0.0.1':
        return render_template('flag.html', FLAG=flag)

    else:
        return render_template('403.html'), 403


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1337)
