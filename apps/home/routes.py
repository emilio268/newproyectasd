# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import Flask,render_template, request, session, Response, url_for, redirect
from flask_login import login_required
from jinja2 import TemplateNotFound
from flask_mysqldb import MySQL,MySQLdb
from apps.config import API_GENERATOR
from flask_sqlalchemy import SQLAlchemy
#from login.login import login_blueprint
from ..empleados.empleados import empleados_blueprint
from ..clientes.clientes import clientes_blueprint
from ..proyectos.proyectos import proyectos_blueprint
from ..servicios.servicios import servicios_blueprint

import json
from datetime import datetime

from flask_restx import Resource, Api

import flask
from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)
from flask_dance.contrib.github import github

from apps import db, login_manager

from apps.authentication.util import verify_pass, generate_token

api = Api(blueprint)

blueprint.register_blueprint(empleados_blueprint, url_prefix='/empleados')
blueprint.register_blueprint(clientes_blueprint, url_prefix='/clientes')
blueprint.register_blueprint(servicios_blueprint, url_prefix='/servicios')
blueprint.register_blueprint(proyectos_blueprint, url_prefix='/proyectos')


@blueprint.route('/index')
@login_required
def index():
    return render_template('Dashboard-Admin/admin_Dashboard.html', segment='index', API_GENERATOR=len(API_GENERATOR))

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment, API_GENERATOR=len(API_GENERATOR))

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None

@blueprint.route('/dashboard-proyectos')
def mostrar_dashboardproyectos():

    return render_template('/Dashboard-Admin/proyectos/index.html')

@blueprint.route('/dashboard-srv-create')
def mostrar_dashboardservicioscreate():

    return render_template('/Dashboard-Admin/servicios/create.html')

@blueprint.route('/dashboard-proy-create')
def mostrar_dashboardproycreate():

    return render_template('/Dashboard-Admin/proyectos/create.html')

@blueprint.route('/dashboard-admin')
def mostrar_dashboardadmin():
    # Realiza consultas para obtener las cantidades utilizando SQLAlchemy
    cantidad_clientes = db.session.query(db.func.count()).select_from(db.table('clientes')).scalar()
    cantidad_empleados = db.session.query(db.func.count()).select_from(db.table('empleados')).scalar()
    cantidad_proyectos = db.session.query(db.func.count()).select_from(db.table('proyectos')).scalar()
    cantidad_usuarios = cantidad_clientes + cantidad_empleados  # Calcula la cantidad total de usuarios

    # Establece estas cantidades en la sesión para usarlas en la plantilla HTML
    session['cantidad_empleados'] = cantidad_empleados
    session['cantidad_clientes'] = cantidad_clientes
    session['cantidad_proyectos'] = cantidad_proyectos
    session['cantidad_usuarios'] = cantidad_usuarios

    return render_template('Dashboard-Admin/admin_Dashboard.html', cantidad_empleados=cantidad_empleados, cantidad_clientes=cantidad_clientes, cantidad_proyectos=cantidad_proyectos, cantidad_usuarios=cantidad_usuarios)
 
@blueprint.route('/dashboard-clie')
def mostrar_dashboardclie():

    return render_template('Dashboard-Admin/clientes/index.html')

@blueprint.route('/dashboard-clie-create')
def mostrar_dashboardemplecreate():

    return render_template('/Dashboard-Admin/clientes/create.html')

@blueprint.route('/dashboard-emp')
def mostrar_dashboardemp():

    return render_template('/Dashboard-Empleado/Emple-Dashboard.html')

@blueprint.route('/dashboard-cli')
def mostrar_dashboardcli():


    return render_template('/Dashboard-Cliente/Clie-Dashboard.html')

@blueprint.route('/dashboard-emp-create')
def mostrar_dashboardempcreate():

    return render_template('/Dashboard-Admin/empleados/create.html')

@blueprint.route('/admin-chat')
def mostrar_adminchat():

    return render_template('/Dashboard-Admin/chat.html')

@blueprint.route('/admin-profile')
def mostrar_adminedit():

    return render_template('/Dashboard-Admin/administrador/edit.html')
