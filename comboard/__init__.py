from flask import Flask
comboard_app = Flask(__name__)

import comboard.config
import comboard.views
import comboard.commands
