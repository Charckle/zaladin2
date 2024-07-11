import json

# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify, \
                  send_file, Response, abort, send_from_directory


from app import app, GIF_DIR, GIF_URL, LATEST_GIF_INFO, GIF_SUCCESS
from app.pylavor import Pylavor

#import os
import re
import os
import io
import pathlib
import datetime


# Define the blueprint: 'auth', set its url prefix: app.url/auth
main_page_module = Blueprint('main_page_module', __name__, url_prefix='/')


@main_page_module.route('/', methods=['GET'])
def index():
    if os.path.exists(LATEST_GIF_INFO):
        with open(LATEST_GIF_INFO, 'r') as info_file:
            gif_path, update_time = info_file.read().split(',')
        gif_filename = os.path.basename(gif_path)
        return render_template('main_page_module/index.html', gif_filename=gif_filename, update_time=update_time, 
                               GIF_SUCCESS=GIF_SUCCESS)
    else:
        return "No GIF available at the moment."

@app.route('/gifs/<path:filename>')
def serve_gif(filename):
    return send_from_directory(GIF_DIR, filename)
