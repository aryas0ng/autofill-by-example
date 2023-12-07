from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, flash
from flask_login import login_required, current_user
from . import db
import json
from werkzeug.utils import secure_filename
import os
from .model import File
from .helper import helper
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
      save_location = os.path.join('website/input', new_filename)
      output_location = os.path.join('website/output', new_filename)
      userfile.save(save_location)
      output = helper(save_location)
      # flash('No valid function found for you autofill task!', category='error')
      # return render_template("home.html", user=current_user)
      if output == None:
        flash('No valid function found for you autofill task!', category='error')
        return render_template("home.html", user=current_user)
      output.to_csv(output_location, index=False, header = False)
      file = File.query.filter_by(file_path=new_filename).first()
      if not file:
        new_file = File(file_path=new_filename, user_id=current_user.id)  #providing the schema for the note 
        db.session.add(new_file) #adding the note to the database 
        db.session.commit()
        flash('File successfully filled!', category='success')
      else:
        flash('File successfully updated!', category='success')
      # return send_from_directory('output', output_file)
  return render_template("home.html", user=current_user)

@views.route('/website/output/<filename>')
def output(filename):
    return send_from_directory('output', filename)