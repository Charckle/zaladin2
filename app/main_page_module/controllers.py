import json

# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify, send_file, Response, abort


from app import app
from app.pylavor import Pylavor

#import os
import re
import os
import io
import pathlib
import datetime



# Define the blueprint: 'auth', set its url prefix: app.url/auth
main_page_module = Blueprint('main_page_module', __name__, url_prefix='/')


# Set the route and accepted methods
@main_page_module.route('/', methods=['GET'])
def index():
    

    return render_template("main_page_module/index.html")
