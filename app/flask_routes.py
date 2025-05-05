from __future__ import annotations

import operator

from flask import render_template, redirect
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flask import Flask

from .db_utils import (
    get_connection,
    destroy_connection,
    fetch_all_from_cursor,
    fetch_many_from_cursor,
)
from .sql_statements import (
    SELECT_ARCH_INFO,
    SELECT_GET_GPU_DETAILS_TEMPL,
    SELECT_GPU_DETAILS_WITH_ID_TEMPL,
    SELECT_MANU_INFO,
)
from .utils import db_1res_to_dict, foreach_apply_db_header


def index():
    return redirect('/index.html')


def index_html():
    return render_template('/template.html', gpus=foreach_apply_db_header(
        fetch_all_from_cursor(
            SELECT_GPU_DETAILS_WITH_ID_TEMPL
            .execute_on_dbcon(get_connection()))))


def gpu_info_page(gpu_id):
    gpu_info = db_1res_to_dict(fetch_many_from_cursor(
        SELECT_GET_GPU_DETAILS_TEMPL
        .where(r'GPU.id', operator.eq, gpu_id)
        .execute_on_dbcon(get_connection())))
    return render_template('gpu/template.html', **{
        'gpu_id': gpu_id,
        'other_info': gpu_info,
    })


def manufacturer_info(manu_id):
    con = get_connection()
    manu_info = db_1res_to_dict(fetch_many_from_cursor(
        SELECT_MANU_INFO
        .where(r'Manufacturer.manufacturer_id', operator.eq, manu_id)
        .execute_on_dbcon(con)))
    return render_template('manufacturer/template.html', **manu_info, gpus=(
        foreach_apply_db_header(fetch_all_from_cursor(
            SELECT_GET_GPU_DETAILS_TEMPL
            .where(r'Manufacturer.manufacturer_id', operator.eq, manu_id)
            .execute_on_dbcon(con)))))


def arch_info(arch_id):
    con = get_connection()
    select_arch = (r'Architecture.arch_id', operator.eq, arch_id)
    arch_info = db_1res_to_dict(fetch_many_from_cursor(
        SELECT_ARCH_INFO
        .where(*select_arch)
        .execute_on_dbcon(con)))
    return render_template('arch/template.html', **arch_info, gpus=(
        foreach_apply_db_header(fetch_all_from_cursor(
            SELECT_GPU_DETAILS_WITH_ID_TEMPL
            .where(*select_arch)
            .execute_on_dbcon(con)
        ))))


def setup_flask_app(app: Flask):
    app.route('/')(index)
    app.route('/index.html')(index_html)
    app.route('/gpu/<int:gpu_id>')(gpu_info_page)
    app.route('/manufacturer/<int:manu_id>')(manufacturer_info)
    app.route('/arch/<int:arch_id>')(arch_info)
    app.teardown_appcontext(lambda *_, **__: destroy_connection())
    return app
