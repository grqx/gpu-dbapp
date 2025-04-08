from __future__ import annotations
from flask import render_template, redirect
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flask import Flask


def index():
    return redirect('/index.html')


def index_html():
    return render_template('index.html')


def gpu_info_page(gpu_id):
    return render_template('gpu/template.html', **{
        'gpu_id': gpu_id,
        'gpu_name': '<Unavailable>',
        # TODO: more
    })


def setup_flask_app(app: Flask):
    app.route('/')(index)
    app.route('/index.html')(index_html)
    app.route('/gpu/<int:gpu_id>')(gpu_info_page)
    return app
