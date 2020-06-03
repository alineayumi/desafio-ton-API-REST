from datetime import datetime, date
from flask.views import MethodView
from app.resources.authentication import requires_auth, check_scopes
from flask import current_app
from .helper import (doSomething)
from flask_jwt import jwt_required, current_identity
from flask import jsonify
from flask import render_template, request, make_response, redirect, flash
from app import db
from app.database import AppClients, Employees


class HealthCheck(MethodView):
    def get(self):
        current_app.logger.info("mock logg")
        return {"mensagem": "ola"}


class MockEndpoint(MethodView):
    @jwt_required()
    @check_scopes(scopes=["sales"])
    def get(self):

        current_app.logger.info("mock logg")
        return jsonify({"now": datetime.now(), "today": date.today(), "identity": {"id": current_identity.id}})

class Home(MethodView):
    def get(self):
        return render_template("public/home.html")

class Dashboard(MethodView):
    def get(self):
        employees = Employees.query.all()
        return render_template("admin/dashboard.html", employees=employees)
    def post(self):
        return ""

class Login(MethodView):
    def get(self):
        return render_template("public/login.html")

    def post(self):

        username = request.form["username"]
        password = request.form["password"]

        # token = jwt.encode

        print("key created!")
        return redirect("/new-api/sign-up")
    

class SignUp(MethodView):
    def get(self):
        return render_template("public/sign-up.html")

    def post(self):

        username = request.form["username"]
        password = request.form["password"]

        exists = db.session.query(AppClients.id).filter_by(name=username).scalar() is not None

        if exists:
            print("username already exists")
            return redirect("/new-api/sign-up")
        a = AppClients(username, password)
        db.session.add(a)
        db.session.commit()
        print("new account created!")
        return redirect("/new-api/sign-up")

class Add(MethodView):
    def get(self):
        employees = Employees.query.all()
        return render_template("admin/add.html", employees=employees)

    def post(self):
        name = request.form["name"]
        age = request.form["age"]
        position = request.form["position"]

        exists = db.session.query(Employees.id).filter_by(name=name, age=age, position=position).scalar() is not None
        if exists:
            print("this person already exists")
            return redirect("/new-api/admin/add")
        a = Employees(name, age, position)
        db.session.add(a)
        db.session.commit()
        print("new worker created!")
        return redirect("/new-api/admin/add")

class Edit(MethodView):

    def get(self):
        employees = Employees.query.all()
        return render_template("admin/edit.html", employees=employees)

    def post(self):
        id = request.form["id"]
        employee = db.session.query(Employees).filter_by(id=id).scalar()
        name = employee.name
        age = employee.age
        position = employee.position
        employees = Employees.query.all()
        return render_template("admin/edit.html", id_ = id, name_=name, age_=age, position_=position, employees=employees)

    def put(self):

        name = request.form["name"]
        age = request.form["age"]
        position = request.form["position"]
        print(name, age, position)

        employee = db.session.query(Employees).filter_by(id=2).update(dict(name=name))
        db.session.commit()

        employees = Employees.query.all()

        return render_template("admin/edit.html", employees=employees)

class Delete(MethodView):
    def delete(self):
        return ""