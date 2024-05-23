import os
import re

from flask import Flask, render_template, request, redirect, url_for, make_response
from flask import session
from flask_login import LoginManager, login_user, login_required, current_user, UserMixin
import sqlite3
from tools import DatabaseWorker, make_hash, check_hash, logging
from datetime import datetime, timedelta
from flask import g


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime=timedelta(minutes=30)

# db_name="project4"
# db_connection=DatabaseWorker("project4")
# result=db_connection.search(query="SELECT * FROM users", multiple=True)
# for row in result:
#     print(row[1])

@app.route('/')
def hello_world():  # put application's code here
    db_connection = DatabaseWorker("project4")
    print(logging())
    if logging():
        user_id = session['user_id']
        print(f"session_id{user_id}")
        posts = db_connection.search(query='SELECT * FROM posts', multiple=True)
        post_data = []
        for post in posts:
            post_id = post[0]
            post_user_name=db_connection.search(query=f"SELECT username FROM users WHERE id = {r[3]}")
            like_number = db_connection.search(query=f"SELECT COUNT(*) FROM likes WHERE post_id={post_id}", multiple=False)[0]
            user_like_with = db_connection.search(
                query=f"SELECT * from likes where post_id={post_id} and user_id={user_id}", multiple=False)
            liked = user_like_with is not None  # True: if liked, False: if not liked
            post = list(post)  # make post as a list
            post.append(like_number)  # add number of likes to a list of post
            post.append(post_user_name[0])
            post.append(liked)
            post_data.append(post)  # add post to post_data
        print(f"login condition{logging()}")
        db_connection.close()
        return render_template('main.html', posts=post_data, logging=logging())

    else:  # not logging
        results = db_connection.search(query='SELECT * FROM posts', multiple=True)
        post_data = []
        for r in results:
            post_user_name=db_connection.search(query=f"SELECT username FROM users WHERE id = {r[3]}")
            print(post_user_name[0])
            post_id = r[0]
            like_number = \
            db_connection.search(query=f"SELECT COUNT(*) FROM likes WHERE post_id={post_id}", multiple=False)[0]
            r = list(r)  # タプルをリストに変換
            r.append(like_number)  # 各投稿にいいねの数を追加する
            r.append(post_user_name[0])
            post_data.append(r)
            print(post_user_name[0])


        db_connection.close()
        return render_template('main.html', posts=post_data, logging=logging())


@app.errorhandler(404)
def page_not_found(e):
    return render_template('not_found.html')

@app.route('/login', methods=['GET','POST'])
def login():
    db_connection = DatabaseWorker("project4")
    if request.method=='POST':
        uname=request.form.get('uname')
        password=request.form.get('psw')
        #Check database for user, then compare hash for the password
        results=db_connection.search(query="""SELECT * FROM users""", multiple=True)
        for row in results:
            print(row)
            signature=row[2] #hash text
            hash_text=f"name{uname}, pass{password}"
            valid=check_hash(hashed_text=signature, text=hash_text)
            if valid:
                user_id = row[0]
                session['user_id'] = user_id
                return redirect(url_for('main'))
    db_connection.close()
    return render_template('login.html')


@app.route('/register', methods=['GET','POST'])
def register():
    db_connection = DatabaseWorker("project4")
    if request.method=='POST':
        uname=request.form.get('uname')
        email=request.form.get('email')
        match = re.match('[A-Za-z0-9._+]+@[A-Za-z]+.[A-Za-z]', email)
        password = request.form.get('psw')
        conf_password = request.form.get('psw_conf')

        valid = True
        user_err=False
        email_err=False
        psw_err=False
        psw_cnf_err = False
        if match == None:
            email_err=True
            valid=False
        if len(password)<8:
            psw_err=True
            valid = False
        if password!=conf_password:
            psw_cnf_err=True
            valid = False

        hash_text=f"name{uname}, pass{password}"
        hash=make_hash(hash_text)
        users_table = db_connection.search(query="SELECT * FROM users", multiple=True)

        for row in users_table:
            if row[0]==uname:
                user_err=True
                print("the user name already exist")
                valid=False
        if valid:
            query = f"""INSERT INTO users (username,password,email)
            values ('{uname}','{hash}','{email}');
            """
            db_connection.run_query(query=query)
            db_connection.close()
            return redirect(url_for('login'))

        db_connection.close()
        return render_template('register.html', email_err=email_err, psw_err=psw_err, psw_cnf_err=psw_cnf_err,user_err=user_err,)
    db_connection.close()
    return render_template('register.html')

@app.route('/forget_pass_email', methods=['GET','POST'])

@app.route('//reset_pass', methods=['GET','POST'])
def reset_pass():
    if logging():
        user_id = session['user_id']
        if request.method == "POST":
            new_comment=request.form.get('comment_text')
            db_connection.run_query(f"UPDATE comments set comment='{new_comment}' where id={comment_id}")
            db_connection.close()
            return redirect(url_for('login'))

    return render_template('reset_pass.html')

@app.route('/logout')
def logout():
    if session['user_id']:
        user_id = session['user_id']
        print(f"logout/session_id{user_id}")
    session.pop('user_id',None)
    return redirect(url_for('main'))

@app.route('/main/<int:post_id>', methods=['GET','POST'])
def view_detail(post_id):
    db_connection = DatabaseWorker("project4")
    if logging():
        user_id = session['user_id']
        print(f"user_id {user_id}")
        post = db_connection.search(query=f"SELECT * FROM posts where id = {post_id}", multiple=False)
        comments=db_connection.search(query=f"SELECT * FROM comments where post_id={post_id}", multiple=True)
        comment_data=[]
        for comment in comments:
            commenter_id=comment[3]
            my_comment=False
            if commenter_id==user_id:
                my_comment= True
            comment=list(comment)
            comment.append(my_comment)
            comment_data.append((comment))
            print(comment)

        if request.method == 'POST':
            date = datetime.now().strftime('%Y%b%d')
            comment = request.form.get('comment_text')
            user_id=user_id
            # genre=request.form.get('genre')
            query = f"""
                INSERT INTO comments (date, user_id, post_id, comment) 
                values ('{date}', '{user_id}','{post_id}','{comment}')"""
            db_connection.insert(query=query)
            db_connection.close()
            return redirect(url_for('view_detail',post_id=post_id))
        return render_template('detail.html', post=post, comment_data=comment_data)
    else:
        post = db_connection.search(query=f"SELECT * FROM posts where id = {post_id}", multiple=False)
        comments = db_connection.search(query=f"SELECT * FROM comments where post_id={post_id}", multiple=True)
        db_connection.close()
        return render_template('detail.html', post=post, comment_data=comments)


@app.route('/main/<int:post_id>/comment/<int:comment_id>/edit', methods=['GET','POST'])
def edit_comment(post_id, comment_id):
    db_connection = DatabaseWorker("project4")
    post=db_connection.search(query=f"SELECT * FROM posts WHERE id={post_id}", multiple=False)
    comments=db_connection.search(query=f"SELECT * FROM comments WHERE post_id={post_id}", multiple=True)

    if logging():
        user_id = session['user_id']
        comment_to_edit=db_connection.search(query=f"SELECT * FROM comments where id ={comment_id}", multiple=False)
        comment_text=comment_to_edit[4]
        if request.method == "POST":
            new_comment=request.form.get('comment_text')
            db_connection.run_query(f"UPDATE comments set comment='{new_comment}' where id={comment_id}")
            db_connection.close()
            return redirect(url_for('view_detail', post_id=post_id))
    db_connection.close()
    return render_template('detail.html', post=post, comments=comments, comment_text=comment_text)

@app.route('/main/<int:post_id>/comment/<int:comment_id>/delete')
def delete_comment(post_id, comment_id):
    db_connection = DatabaseWorker("project4")
    if session['user_id']:
        user_id = session['user_id']
    db_connection.run_query(query=f"DELETE from comments where id={comment_id}")
    db_connection.close()
    return redirect(url_for('view_detail', post_id=post_id))

@app.route('/post',  methods=['GET','POST'])
def post():
    db_connection = DatabaseWorker("project4")
    if logging():
        user_id = session['user_id']
        if request.method=='POST':
            date=datetime.now().strftime('%Y%b%d')
            text=request.form.get('post_text')
            user_id=user_id
            file = request.files.get('file')
            print(f"file: {file}")
            file_name = f"{date}_{file.filename}"
            file_path = os.path.join('static/post_image', file_name)
            file.save(file_path)
            genre=request.form.get('genre')
            print(genre)
            query=f"""
            INSERT INTO posts(date, post_text,user_id, photo, genre) values ('{date}', '{text}','{user_id}', '{file_name}', '{genre}')"""
            db_connection.insert(query=query)
            db_connection.close()
            return redirect(url_for('main'))
        db_connection.close()
        return render_template('post.html')
    else:
        return redirect(url_for('login'))

@app.route('/main',methods=['GET','POST'])
def main():
    db_connection = DatabaseWorker("project4")
    print(logging())
    if logging():
        logging_user_id = session['user_id']
        print(f"session_id{logging_user_id}")
        posts=db_connection.search(query='SELECT * FROM posts', multiple=True)
        post_data = []
        # /here
        for post in posts:
            post_id=post[0]
            post_user_name=db_connection.search(query=f"SELECT username FROM users WHERE id = {post[3]}")
            like_number = db_connection.search(query=f"SELECT COUNT(*) FROM likes WHERE post_id={post_id}", multiple=False)[0]
            user_like_with=db_connection.search(query=f"SELECT * from likes where post_id={post_id} and user_id={logging_user_id}", multiple=False)
            liked = user_like_with is not None #True: if liked, False: if not liked
            post = list(post) #make post as a list
            post[3] = post_user_name[0]
            post.append(like_number) #add number of likes to a list of post
            post.append(post_user_name)
            post.append(liked)
            post_data.append(post) #add post to post_data

        print(f"login condition{logging()}")
        db_connection.close()
        return render_template('main.html', posts=post_data, logging=logging())

    else: # not logging
        results = db_connection.search(query='SELECT * FROM posts', multiple=True)
        post_data = []
        for r in results:
            post_id = r[0]
            post_user_name=db_connection.search(query=f"SELECT username FROM users WHERE id = {r[3]}")
            like_number = db_connection.search(query=f"SELECT COUNT(*) FROM likes WHERE post_id={post_id}", multiple=False)[0]
            r = list(r)  # タプルをリストに変換
            r.append(like_number)  # 各投稿にいいねの数を追加する
            r.append(post_user_name)
            post_data.append(r)
        # if request.method == 'POST':
        #     return redirect(url_for('login'))
        db_connection.close()
        return render_template('main.html', posts=post_data, logging=logging())

@app.route('/main/<int:post_id>/like', methods=['GET','POST'])
def like(post_id):
    db_connection = DatabaseWorker("project4")
    print(f"logging: {logging()}")
    if not logging():
        db_connection.close()
        return redirect(url_for('login'))
    if logging():
        user_id = session['user_id']
        print(user_id)
        user_like_with = db_connection.search(query=f"SELECT * from likes where post_id={post_id} and user_id={user_id}",multiple=False)
        liked = user_like_with is not None  # True: if liked, False: if not liked
        if liked:
            db_connection.run_query(query=f"DELETE FROM likes WHERE post_id={post_id} and user_id={user_id}")
        else:
            db_connection.run_query(query=f"INSERT INTO likes (post_id, user_id) values ({post_id},{user_id})")
        db_connection.close()
        return redirect(url_for('main'))

@app.route('/profile/<int:user>') #user is the user id of the one that you want to see
def profile(user):
    db_connection = DatabaseWorker("project4")
    if logging():
        user_id=session['user_id']
        user_pro = db_connection.search(query=f"SELECT * FROM users WHERE id={user}", multiple=False)
        f_user_with = db_connection.search(
            query=f"SELECT * from user_follows where user_id={user_id} and following_user_id={user}", multiple=False)
        print(f_user_with)
        following = f_user_with is not None
        return render_template('profile.html', user=user_pro, following=following)
    else:
        user_pro = db_connection.search(query=f"SELECT * FROM users WHERE id={user}", multiple=False)
        return render_template('profile.html', user=user_pro)




    # return redirect((url_for('login')))

@app.route('/profile/<int:f_user_id>/follow', methods=['POST'])
def user_follow(f_user_id):
    db_connection = DatabaseWorker("project4")
    if logging():
        user_id = session['user_id']
    else:
        return redirect(url_for('login'))
    user_pro = db_connection.search(query=f"SELECT * FROM users WHERE id={f_user_id}", multiple=False)
    f_user_with = db_connection.search(query=f"SELECT * from user_follows where user_id={user_id} and following_user_id={f_user_id}",multiple=False)
    print(f_user_with)
    following = f_user_with is not None  # True: if following, False: if not following
    if following:
        db_connection.run_query(query=f"DELETE FROM user_follows WHERE user_id={user_id} and following_user_id={f_user_id}")
    else:
        db_connection.run_query(query=f"INSERT INTO user_follows (user_id, following_user_id) values ({user_id},{f_user_id})")
    db_connection.close()
    return redirect(url_for('profile', user=user_pro[0]))

@app.route('/my_profile', methods=['POST', 'GET'])
def my_profile():
    db_connection = DatabaseWorker("project4")
    if logging():
        user_id = session['user_id']
        my_pro = db_connection.search(query=f"SELECT * FROM users WHERE id={user_id}", multiple=False)
        db_connection.close()
        return render_template('my_profile.html',my_profile=my_pro)
    else:
        return render_template('login2.html')
    # return render_template('my_profile.html',my_profile=my_pro)


if __name__ == '__main__':
    app.run()

db_connection = DatabaseWorker("project4")

