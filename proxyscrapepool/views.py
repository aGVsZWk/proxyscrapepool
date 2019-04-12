# -*- coding: utf-8 -*-
# author: Luke
from flask import request, render_template, session, flash, redirect, url_for

from proxyscrapepool import app
from .tasks import  send_async_email_task, get_proxy_task
from flask_mail import Message

@app.route('/')
def index():
    return "<h1>index</h1>"

@app.route('/mail', methods=['GET', 'POST'])
def send_mail():
    if request.method == 'GET':
        return render_template('email.html', email=session.get('email', ''))
    email = request.form['email']
    session['email'] = email

    # send the email
    msg = Message('Hello from Flask',
                  recipients=[request.form['email']])
    msg.body = 'This is a test email sent from a background Celery task.'
    if request.form['submit'] == 'Send':
        # send right away
        send_async_email_task.delay(msg)
        flash('Sending email to {0}'.format(email))
    else:
        # send in one minute
        send_async_email_task.apply_async(args=[msg], countdown=60)
        flash('An email will be sent to {0} in one minute'.format(email))
    return redirect(url_for('send_mail'))


@app.route('/start_proxy')
def proxy_start():
    get_proxy_task.apply_async(countdown=60)
    return "<h1>启动成功</h1>"