from __future__ import annotations
from flask import render_template, redirect
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flask import Flask


def index():
    return redirect('/index.html')


def index_html():
    return render_template('index.html')


def setup_flask_app(app: Flask):
    app.route('/')(index)
    app.route('/index.html')(index_html)
    return app
