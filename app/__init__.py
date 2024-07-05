# Import flask and template operators
from flask import Flask, render_template, jsonify
from os import path, mkdir, environ 
import logging
from logging.handlers import RotatingFileHandler


# Define the WSGI application object
app = Flask(__name__)


# Configurations
if environ.get('ENVCONFIG', "DEV") != 'PROD':
    app.config.from_object("config.DevelopmentConfig")
else:
    app.config.from_object("config.ProductionConfig")


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/health')
def static_file():
    if check_database_active():
        return jsonify(status="healthy"), 200
    else:
        return jsonify(status="not healthy"), 500




# Import a module / component using its blueprint handler variable (mod_auth)
from app.main_page_module.controllers import main_page_module as main_module

# Register blueprint(s)
app.register_blueprint(main_module)
# app.register_blueprint(xyz_module)
# ..


# activate logging

if not path.exists('logs'):
    mkdir('logs')
file_handler = RotatingFileHandler('logs/error.log', maxBytes=10240,
                                   backupCount=5)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.DEBUG)
app.logger.info('Application startup')
