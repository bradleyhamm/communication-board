from flask import Flask
app = Flask(__name__)

from database import Database
import views
import commands
