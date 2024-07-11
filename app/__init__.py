# Import flask and template operators
from flask import Flask, render_template, jsonify
from os import path, mkdir, environ 
import logging
from logging.handlers import RotatingFileHandler
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Directory to save the GIFs
GIF_DIR = 'app/static'

    
# URL of the GIF to fetch
GIF_URL = 'https://meteo.arso.gov.si/uploads/probase/www/observ/radar/si0-rm-anim.gif'
# File to store the latest GIF path and update time
LATEST_GIF_INFO = 'latest_gif.txt'    
GIF_SUCCESS = [False]

# Define the WSGI application object
app = Flask(__name__)

def fetch_gif():
    try:
        session = requests.Session()
        retries = Retry(total=6, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))

        response = session.get(GIF_URL, timeout=10)
        response.raise_for_status()
        
        gif_path = path.join(GIF_DIR, 'latest.gif')
        
        with open(gif_path, 'wb') as gif_file:
            gif_file.write(response.content)
        with open(LATEST_GIF_INFO, 'w') as info_file:
            update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            info_file.write(f"{gif_path},{update_time}")
        app.logger.info(f"Fetched new GIF at {datetime.now()}")
        
        GIF_SUCCESS[0] = True
    except requests.RequestException as e:
        app.logger.debug(f"Failed to fetch GIF: {e}")
        
        # Check if there is an existing GIF
        if path.exists(LATEST_GIF_INFO):
            with open(LATEST_GIF_INFO, 'r') as info_file:
                gif_path, update_time = info_file.read().split(',')
            app.logger.debug(f"Displaying old GIF last updated at {update_time}")
            
            GIF_SUCCESS[0] = False
        else:
            app.logger.debug('No previous GIF available to display.')
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_gif, 'interval', minutes=10)
scheduler.start()


# Configurations
if environ.get('ENVCONFIG', "DEV") != 'PROD':
    app.config.from_object("config.DevelopmentConfig")
else:
    app.config.from_object("config.ProductionConfig")


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Import a module / component using its blueprint handler variable (mod_auth)
from app.main_page_module.controllers import main_page_module as main_module

# Register blueprint(s)
app.register_blueprint(main_module)
# app.register_blueprint(xyz_module)
# ..



def get_version():
    try:
        with open('VERSION') as f:
            lines = f.readlines()
            return lines[0]    
    except FileNotFoundError:
        app.logger.error(f"Version file not found")            
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")

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

app.logger.info("__________      .__              .___.__         ________  ")
app.logger.info("\____    /____  |  | _____     __| _/|__| ____   \_____  \ ")
app.logger.info("  /     /\__  \ |  | \__  \   / __ | |  |/    \   /  ____/ ")
app.logger.info(" /     /_ / __ \|  |__/ __ \_/ /_/ | |  |   |  \ /       \ ")
app.logger.info("/_______ (____  /____(____  /\____ | |__|___|  / \_______ \ ")
app.logger.info("        \/    \/          \/      \/         \/          \/")
app.logger.info("-"*10)
app.logger.info("Andrej Zubin, 11.7.2024")
app.logger.info(f"Version: {get_version()}")    
app.logger.info("-"*10)

fetch_gif()