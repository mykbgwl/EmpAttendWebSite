from .qr import qrgen
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import *
from .models import User, Scanned
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import os
import cv2


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Successfully!', category='Success')
                login_user(user, remember=True)
                return redirect(url_for('views.index'))
            else:
                flash('Incorrect password, try again.', category='Error')
        else:
            flash('Email does not exist.', category='Error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='Error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='Error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='Error')
        elif password1 != password2:
            flash('Passwords does not match.', category='Error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='Error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account Created!', category='Success')
            return redirect(url_for('views.index'))

    return render_template("sign_up.html", user=current_user)


@auth.route('/generate')
def generate():
    return render_template('generate.html', user=current_user)


@auth.route('/converted', methods=['POST'])
def convert():
    global tex
    tex = request.form.get('fullname')
    return render_template('converted.html', user=current_user)


@auth.route('/download')
def download():
    qrgen(tex)
    filename = tex+'.png'
    return send_file(filename, as_attachment=True)


@auth.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if request.method == 'POST':
        text = request.form.get('text')
        fullname = Scanned.query.filter_by(name=text).first()
        if fullname:
            flash('Already Present', category='Error')
        elif text == '':
            flash('First Scan the QR Code', category='Error')
        else:
            new_data = Scanned(name=text)
            db.session.add(new_data)
            db.session.commit()
            flash('Attendance Marked!', category='Success')

    return render_template("markattendance.html", user=current_user)


@auth.route('/records')
def record():
    all_records = Scanned.query.all()
    return render_template("records.html", user=current_user, records=all_records, pageTitle='All Records')
