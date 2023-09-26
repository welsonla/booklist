from flask import Flask
from app import create_app
from app.models.book import Book
app = create_app('development')

