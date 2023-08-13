from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request
import json
from sqlalchemy.orm import class_mapper

db = SQLAlchemy()


def result(code=1000, message="", result=None):
    dictionary = {"returncode": code, "message": message, "result": result}
    json_data = jsonify(dictionary)
    print(f"json.output:{json_data}")
    return json_data



def sqlalchemy_to_json(obj):
    # 获取对象的属性映射器
    mapper = class_mapper(obj.__class__)
    # 获取对象的所有列属性
    columns = [column.key for column in mapper.columns]
    # 创建一个字典，用于存储属性名和对应的值
    data = {}
    # 遍历对象的所有列属性
    for column in columns:
        # 通过属性名获取属性值
        value = getattr(obj, column)
        # 将属性名和对应的值添加到字典中
        data[column] = value
    # 将字典转换为JSON字符串
    json_data = json.dumps(data)
    return json_data