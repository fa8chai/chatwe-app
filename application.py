import os

from flask import session ,Flask,render_template,request,redirect,url_for
from flask_socketio import SocketIO, emit, join_room, leave_room,send
from datetime import datetime
from flask_session import Session
from sqlalchemy import or_


# Import table definitions.
from models import *


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Tell Flask what SQLAlchemy databas to use.
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"]  = '2490ca01db99e615cdd002ff'
app.config['SESSION_TYPE'] = 'filesystem'

db.init_app(app)



Session(app)







@app.route("/",methods=['POST','GET'])
def index():
    db.create_all()
    if 'username' in session :
        username = session['username']
        user = Users.query.filter_by(name = username).first()
        joind_channels = user.channels
        return render_template('index.html',username=username,channels=joind_channels)
    return redirect(url_for('login'))




@app.route('/search',methods=['POST','GET'])
def search():
    if 'username' in session :
        if request.method == 'POST':
            name = request.form.get('name')
            name = "%"+name+"%"
            channels = Channels.query.filter(Channels.name.like(name)).all()
            return render_template('search.html',username=session['username'],channels=channels)
        else :
            return render_template('search.html',username=session['username'],channels=Channels.query.all())     
    return redirect(url_for('login'))





@app.route('/create',methods=['POST','GET'])
def create():
    if 'username' in session :
        if request.method == 'POST':
            now = datetime.now()
            cha = request.form.get('cha')
            desc = request.form.get('desc')
            dt_string = now.strftime("%m/%d")
            user = session['username']

            if Channels.query.filter_by(name = cha).first() :
                return render_template('create.html',username=session['username'],error='channel exist!',channel=cha)
            else :
                channel = Channels(name=cha,desc=desc,time=dt_string,user=user)
                db.session.add(channel)
                db.session.commit()
                return redirect(url_for('chatroom',chat=cha))
        return render_template('create.html',username=session['username'])
    return redirect(url_for('login'))

    






@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        if Users.query.filter(and_(Users.name == name, Users.email == email)).first():
            session['username'] = name
            return redirect(url_for('index'))

        else: 
             
             if Users.query.filter_by(email = email).first():
                 return render_template('login.html',error='this email adress associated with another user')
             user = Users(name=name,email=email)
             db.session.add(user)
             db.session.commit()
             print(user)
             print(user.email)
             session['username'] = user.name
             return redirect(url_for('index'))

    elif request.method == 'GET' :
        if 'username' in session :
            return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('login'))


@app.route('/delete-my-account')
def delete():
    if 'username' in session:
        username = session['username']
        user = Users.query.filter_by(name=username).first()
        print(user)
        db.session.delete(user)
        db.session.commit()
        session.pop('username',None)
        
    return redirect(url_for('index'))
    
       

@app.route('/chatroom/<chat>',methods=['GET'])
def chatroom(chat):
    if 'username' in session:
        channel = Channels.query.filter_by(name = chat).first()
        if channel :
            for user in channel.users:
                if session['username'] == user.name :
                    return render_template('chatroom.html', yes = 'yes' ,channel=Channels.query.filter_by(name = chat).first(),username=session['username'],messages= Channels.query.filter_by(name = chat).first().messages)
            return render_template('chatroom.html',channel=Channels.query.filter_by(name = chat).first(),username=session['username'],messages= Channels.query.filter_by(name = chat).first().messages)
        return render_template('error.html',error="no channel!",username=session['username'])
    return render_template('login.html')



@app.route('/chatroom/<chat>/details')
def details(chat):
    if 'username' in session:
        channel = Channels.query.filter_by(name = chat).first()
        users = channel.users
        users_list = channel.users
        users_count = len(users_list)
        print(users_count)
        return render_template('details.html',users_count=users_count,channel=channel,users=users,username=session['username'])
       
    return render_template('login.html')





@socketio.on('add message')
def message(data):
    print(data)
    now = datetime.now()
    dt_string = now.strftime("%I:%M %p %m-%d")
    message = data['message']
    room = data['channel']
    username = session['username']
    # database info

    channel_id = Channels.query.filter_by(name = room).first().id
    user_id = Users.query.filter_by(name = username).first().id
    # add message to database
    
    data = Messages(message=message,time=dt_string,channel_id=channel_id,user_id=user_id)
    db.session.add(data)
    db.session.commit()
    
    print('hi')
    print(message)
    emit('broadcast message',{'message':message,'dt_string':dt_string,'username':session['username']} ,broadcast=True)
    
    



@socketio.on('join')
def on_join(data):
    
    username = data['username']
    user = Users.query.filter_by(name=username).first()
    room = data['channel']
    datac = Channels.query.filter_by(name = room ).first()
    datac.users.append(user)
    db.session.add(datac)
    db.session.commit()
    join_room(room)
    emit('status',{'msg': username + ' has enterd the room'},broadcast=True)



@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['channel']
    user = Users.query.filter_by(name=username).first()
    datac = Channels.query.filter_by(name = room ).first()
    datac.users.remove(user)
    db.session.add(datac)
    db.session.commit()
    leave_room(room)
    emit('left',{'msg': username + ' has left the room'},broadcast=True)
