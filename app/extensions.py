from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request
from flask_msearch import Search
from jieba.analyse import ChineseAnalyzer
from flask_marshmallow import Marshmallow

db = SQLAlchemy()

ma = Marshmallow()

search = Search(analyzer=ChineseAnalyzer())

# 日期格式
date_style = '%Y-%m-%d %H:%M:%S'

def result(code=1000, message="", result=None):
    """接口返回格式封装"""
    dictionary = {"returncode": code, "message": message, "result": result}
    json_data = jsonify(dictionary)
    # print(f"json.output:{json_data}")
    return json_data
