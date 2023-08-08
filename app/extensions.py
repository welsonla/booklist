from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request

db = SQLAlchemy()


def result(code=1000, message="", data={}):
    dict = {"code": code, "message": message, "data": data}
    return jsonify(dict)
