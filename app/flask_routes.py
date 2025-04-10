from __future__ import annotations

import operator

from flask import render_template, redirect
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flask import Flask

from .db_utils import (
    get_connection,
    destroy_connection,
    fetch_many_from_cursor,
)
from .sql_statements import SELECT_GET_GPU_DETAILS_TEMPL
from .utils import db_1res_to_dict


def index():
    return redirect('/index.html')


def index_html():
    return render_template('index.html')


def gpu_info_page(gpu_id):
    con = get_connection()
    gpu_info = db_1res_to_dict(fetch_many_from_cursor(
        SELECT_GET_GPU_DETAILS_TEMPL
        .where(r'GPU.id', operator.eq, gpu_id)
        .execute_on_dbcon(con)))
    return render_template('gpu/template.html', **{
        'gpu_id': gpu_id,
        'other_info': gpu_info,
    })


def setup_flask_app(app: Flask):
    app.route('/')(index)
    app.route('/index.html')(index_html)
    app.route('/gpu/<int:gpu_id>')(gpu_info_page)
    app.teardown_appcontext(lambda *_, **__: destroy_connection())
    return app
