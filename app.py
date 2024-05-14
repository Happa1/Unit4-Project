from flask import Flask, render_template, request, redirect, url_for, make_response
from flask import session
import sqlite3
from tools import DatabaseWorker, make_hash, check_hash
from datetime import datetime
from flask import g


app = Flask(__name__)
app.secret_key = "fahjdkfhquwihfvzcnvmfadfhjqkwrypqiu"
# db_name="project4"
# db_connection=DatabaseWorker("project4")
# result=db_connection.search(query="SELECT * FROM users", multiple=True)
# for row in result:
#     print(row[1])

@app.route('/')
def hello_world():  # put application's code here
    db_connection = DatabaseWorker("project4")
    results = db_connection.search(query='SELECT * FROM posts', multiple=True)
    results_with_likes = []
    for r in results:
        post_id = r[0]
        like_number = db_connection.search(query=f"SELECT COUNT(*) FROM likes WHERE post_id={post_id}", multiple=False)[0]
        r = list(r)  # タプルをリストに変換
        r.append(like_number)  # 各投稿にいいねの数を追加する
        results_with_likes.append(r)
        # user_like_with = db_connection.run_query(query=f"-- SELECT * from likes where post_id={post_id} and user_id={user_id}")
        # print(user_like_with)

    db_connection.close()
    return render_template('main.html', posts=results_with_likes)

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
    return render_template('login.html')
    db_connection.close()

@app.route('/register', methods=['GET','POST'])
def register():
    db_connection = DatabaseWorker("project4")
    if request.method=='POST':
        uname=request.form.get('uname')
        password=request.form.get('psw')
        conf_password=request.form.get('psw_conf')

        if password!=conf_password:
            print("the password is incorrect.")

        hash_text=f"name{uname}, pass{password}"
        hash=make_hash(hash_text)
        users_table = db_connection.search(query="SELECT * FROM users", multiple=True)
        valid = True
        for row in users_table:
            if row[0]==uname:
                print("the user name already exist")
                valid=False
        if valid:
            query = f"""INSERT INTO users (username,password)
            values ('{uname}','{hash}');
            """
            db_connection.run_query(query=query)
            db_connection.close()
        return render_template('login.html')
    db_connection.close()
    return render_template('register.html')

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login')))
    # response.set_cookie('user_id', "", expires=0)
    #destory the session
    session.pop('user_id', None)
    return response

@app.route('/main/<int:post_id>', methods=['GET','POST'])
def view_detail(post_id):
    db_connection = DatabaseWorker("project4")
    post=db_connection.search(query=f"SELECT * FROM posts where id = {post_id}", multiple=False)

    return render_template('detail.html', post=post)


@app.route('/post',  methods=['GET','POST'])
def post():
    db_connection = DatabaseWorker("project4")
    if session['user_id']:
        user_id = session['user_id']
    if request.method=='POST':
        date=datetime.now().strftime('%Y%b%d')
        text=request.form.get('post_text')
        user_id=user_id
        # genre=request.form.get('genre')
        query=f"""
        INSERT INTO posts(date, post_text,user_id) values ('{date}', '{text}','{user_id}')"""
        db_connection.insert(query=query)
        db_connection.close()
        return render_template('main.html')
    db_connection.close()
    return render_template('post.html')

@app.route('/main',methods=['GET','POST'])
def main():
    db_connection = DatabaseWorker("project4")

    if session['user_id']:
        user_id = session['user_id']
        print(user_id)
    posts=db_connection.search(query='SELECT * FROM posts', multiple=True)
    post_data = []
    for post in posts:
        post_id=post[0]
        like_number = db_connection.search(query=f"SELECT COUNT(*) FROM likes WHERE post_id={post_id}", multiple=False)[0]
        user_like_with=db_connection.search(query=f"SELECT * from likes where post_id={post_id} and user_id={user_id}", multiple=False)
        liked = user_like_with is not None
        post = list(post)
        post.append(like_number)
        post.append(liked)
        post_data.append(post)
        print(post)
        print(user_like_with)

        if request.method =='POST':
            print(user_like_with)
            query = f"DELETE FROM likes WHERE post_id={post_id} and user_id={user_id}"
            db_connection.run_query(query=query)
            print(query)
            # db_connection.close()
            # return redirect(url_for('main'))
            # return render_template('main.html', posts=post_data, like_number=like_number, user_like_with=user_like_with)

    db_connection.close()
    return redirect(url_for('main'))
    return render_template('main.html', posts=post_data)

if __name__ == '__main__':
    app.run()
