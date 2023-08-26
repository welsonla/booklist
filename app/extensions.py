from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request

db = SQLAlchemy()

def result(code=1000, message="", result=None):
    """接口返回格式封装"""
    dictionary = {"returncode": code, "message": message, "result": result}
    json_data = jsonify(dictionary)
    print(f"json.output:{json_data}")
    return json_data
