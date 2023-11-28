from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory
from flask_login import login_required, current_user
from . import db
import json
from werkzeug.utils import secure_filename
import os
#import the processing function to here

ALLOWED_EXTENSIONS = set(['csv'])
views = Blueprint('views', __name__)

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
  if request.method == "POST":
    userfile = request.files['file']
    if userfile and allowed_file(userfile.filename):
      filename = secure_filename(userfile.filename)
      new_filename = f'{filename.split(".")[0]}_{"filled"}.csv'
      save_location = os.path.join('input', new_filename)
      userfile.save(save_location)
      #call the process function here
      output_file = "" #place holer
      return send_from_directory('output', output_file)
    return redirect(url_for('output'))
  return render_template("home.html", user=current_user)
 
@views.route('/output')
def output():
  return render_template("output.html", files=os.listdir('output'))

@views.route('/output/<filename>')
def download(filename):
  return send_from_directory('output', filename)