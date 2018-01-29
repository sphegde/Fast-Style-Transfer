import os
from flask import Flask, request, redirect, url_for, flash, send_file, render_template
from werkzeug.utils import secure_filename
from transform_video import process_video
from evaluate import ffwd_to_img

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'static'
CHECKPOINT_FOLDER = 'ckpt'
IMAGE_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
VIDEO_EXTENSIONS = set(['mp4'])
ALLOWED_EXTENSIONS = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['CHECKPOINT_FOLDER'] = CHECKPOINT_FOLDER


def allowed_file(filename, extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in extensions


def process_file(filename, chk):
    abs_in_filename = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), app.config['UPLOAD_FOLDER'], filename)
    abs_out_filename = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), app.config['PROCESSED_FOLDER'], filename)
    abs_chk_filename = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), app.config['CHECKPOINT_FOLDER'], chk)
    if os.path.exists(abs_out_filename):
        os.remove(abs_out_filename)
    if allowed_file(filename, VIDEO_EXTENSIONS):
        process_video(abs_in_filename, abs_chk_filename, abs_out_filename)
    if allowed_file(filename, IMAGE_EXTENSIONS):
        ffwd_to_img(abs_in_filename, abs_out_filename, abs_chk_filename)
    return redirect('/static/'+filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        chk = request.form['transfer'] + '.ckpt'
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)
            path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), app.config['UPLOAD_FOLDER'], filename)
            if os.path.exists(path):
                os.remove(path)
            file.save(path)
            return process_file(filename, chk)

    return render_template('index.html')


if __name__ == '__main__':
    app.run()
