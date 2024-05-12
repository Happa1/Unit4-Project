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
    return render_template('main.html')

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
                return redirect(url_for('register'))
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
        return render_template('login.html')
    return render_template('register.html')
    db_connection.close()

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login')))
    # response.set_cookie('user_id', "", expires=0)
    #destory the session
    session.pop('user_id', None)
    return response

@app.route('/post', methods=['POST'])
def main():
    if request.method=='POST':
        date=datetime.now().strftime('%Y%b%d')
        text=request.form.get('text')
        genre=request.form.get('genre')
        query=f"""
        INSERT INTO post(date, )"""

    return render_template('post.html')

@app.route('/main')
def main():
    return render_template('main.html')

if __name__ == '__main__':
    app.run()
