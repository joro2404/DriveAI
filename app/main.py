from flask import Flask, render_template, request, redirect, url_for, Blueprint


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/drivers')
def drivers():
    return render_template('drivers.html')

@main.route('/statistics')
def statistics():
    return render_template('statistics.html')

if __name__ == '__main__':
    main.app.run()