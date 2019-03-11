import os
from flask import Flask, render_template, request, make_response, url_for, redirect, session, flash, abort
app = Flask(__name__)
# Mengamankan gambarnya
from werkzeug.utils import secure_filename
app.secret_key = 'ABID_GANTENG123456789'

# INDEX nya (http://127.0.0.1:5000)
@app.route('/')
def index():
    return render_template('index.html')

# Belajar web statis
@app.route('/profile')
def profile():
    return "Anda ada di halaman Profile"

# Belajar web dinamis
@app.route('/profile/<username>')
def show_profile(username):
    return render_template('profile.html', username=username)

#vBelajar metode POST
@app.route('/word', methods=['GET', 'POST'])
def word():
    if request.method == 'POST':
        return request.form['word']
    return render_template('word.html')

# Belajar Methode GET
# http://127.0.0.1:5000/search?search=abid
@app.route('/search')
def search():
    search = request.args.get('search')
    return render_template('index.html', search=search)

# Belajar cookie
@app.route('/getcookie')
def getcookie():
    email = request.cookies.get('email_user')
    return 'Email yang telah kamu input adalah '+email

# Belajar Session
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        username = session['username']
        return redirect(url_for('show_profile', username=username))
    if request.method == 'POST':
        # Belajar Abort
        # untuk apa? agar memberikan info Page Error
        if request.form['email'] == '':
            abort(401)
        if request.form['password'] == '':
            abort(401)
        resp = make_response('EMAIL KAMU ADALAH ' + request.form['email'])
        resp.set_cookie('email_user', request.form['email'])
        session['username'] = request.form['email']
        # Belajar Flash
        # Flash itu apa? pesan singkat atau panjang yang hanya berlaku 1x (biasanya digunakan untuk info)
        flash('Berhasil Login', 'Success')
        return resp
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.errorhandler(401)
def page_not_authenticated(e):
    return render_template('401.html'), 401

# Upload Gambar
ALLOWED_EXTENTION = set(['png', 'jpeg', 'jpg', 'gif', 'svg'])
# Tentuin dimana user boleh upload filenya
app.config['UPLOAD_FOLDER'] = 'uploads'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENTION

@app.route('/uploadfile', methods=['POST', 'GET'])
def uploadfile():
    if request.method == 'POST':

        file = request.files['file']

        if 'file' not in request.files:
            return redirect(request.url)
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'] + filename))
            return 'file berhasil di save di '+ filename
    return render_template('upload.html')