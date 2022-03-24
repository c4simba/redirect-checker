from flask import Flask, redirect, url_for, Response, stream_with_context

app = Flask(__name__)


@app.route('/no_redirect_one')
def no_redirect_one():
    return 'just some data'


@app.route('/redirect_one')
def redirect_one():
    return redirect('/no_redirect_one')


@app.route('/redirect_two')
def redirect_two():
    return redirect(url_for('redirect_one'))


@app.route('/redirect_cycle')
def redirect_cycle():
    return redirect(url_for('redirect_cycle2'))


@app.route('/redirect_cycle2')
def redirect_cycle2():
    return redirect(url_for('redirect_cycle'))


@app.route('/redirect_big')
def redirect_big():
    return redirect(url_for('redirect_big2'))


@app.route('/redirect_big2')
def redirect_big2():
    def generate():
        while True:
            yield 'a'*200
    return app.response_class(stream_with_context(generate()), status=302, headers={
        'Location': url_for('redirect_big')
    })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
