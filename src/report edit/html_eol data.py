from flask import Flask, send_from_directory, render_template
import os
from collections import defaultdict
import logging
from logging.handlers import RotatingFileHandler



app = Flask(__name__, template_folder='templates',static_folder='')

def get_image_files(path):
    abs_path = os.path.abspath(path)
    image_files = []
    for root, dirs, files in os.walk(abs_path):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.png'):
                image_files.append(os.path.join(root, file).replace('\\', '/'))
    return image_files




@app.route('/')
def image_gallery():
    abs_path = 'C:/Project/EMR3/EOL bench Test results/EOL data processing/Results'
    image_files = get_image_files(abs_path)
    image_dict = defaultdict(list)
    for file in image_files:
        category = os.path.split(os.path.dirname(file))[-1]
        rel_path = os.path.relpath(file, abs_path).replace('\\', '/')
        image_dict[category].append(rel_path)
    return render_template('image_gallery.html', image_dict=image_dict)

if __name__ == '__main__':
    app.run()

if not os.path.exists('logs'):
    os.mkdir('logs')

if not app.debug:
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('App startup')