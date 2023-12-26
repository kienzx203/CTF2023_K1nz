from flask import Flask, render_template_string

app = Flask(__name__)


@app.route('/')
def hello():
    # Định nghĩa một chuỗi template
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Template String Example</title>
    </head>
    <body>
        <h1>Hello, {{''.attr('hhclasshh'.replace('h','_')).__mro__[1].__subclasses__()}}!</h1>
    </body>
    </html>
    """

    # Sử dụng render_template_string để hiển thị template
    return render_template_string(template)


if __name__ == '__main__':
    app.run(port=8000)
