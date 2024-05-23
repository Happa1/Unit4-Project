from datetime import datetime
from time import strftime

from flask import Flask, render_template, request, redirect, url_for, make_response, session
from tools import DatabaseWorker

app = Flask(__name__)
app.secret_key = "fahjdkfhquwihfvzcnvmfadfhjqkwrypqiu"

@app.route('/food/<int:food_id>', methods=['GET','POST'])
def get_food(food_id):
    db = DatabaseWorker('database.db')
    food = db.search(query=f"SELECT * from foods where id={food_id}", multiple=False)
    reviews = db.search(query=f"SELECT * from reviews where food_id={food_id}", multiple=True)
    print(reviews)
    if request.method == 'POST':
        #the form was submitted with the new review
        date = datetime.now().strftime('%Y/%b/%d')
        comment=request.form.get('comment')
        stars=request.form.get('stars')
        query=f"""INSERT into reviews(data, comment, stars, food_id) values 
        ('{date}','{comment}',{stars},{food_id})"""
        print(query)
        db.insert(query=query)
        db.close()
        return redirect(url_for('get_food', food_id=food_id))

    db.close()
    return render_template('food.html',food=food, reviews=reviews)

@app.route('/food/<int:food_id>/review/<int:review_id>/delete')
def delete_review (review_id, food_id):
    db = DatabaseWorker('database.db')
    db.run_query(f"DELETE from reviews where id={review_id}")
    db.close()
    return redirect(url_for('get_food', food_id=food_id))


@app.route('/food/<int:food_id>/review/<int:review_id>/edit', methods={'GET','POST'})
def edit_review (review_id, food_id):
    db = DatabaseWorker('database.db')
    food=db.search(query=f"SELECT * from foods where id={food_id}", multiple=False)
    reviews = db.search(query=f"SELECT * from reviews where id={food_id}", multiple=True)
    review_to_edit = db.search(query=f"SELECT * from reviews where id={review_id}", multiple=False)
    comments=review_to_edit[1]
    stars=review_to_edit[3]
    if request.method == 'POST': #update the review and redirect to the food page
        comment = request.form.get('comment')
        stars = request.form.get('stars')
        db.run_query(f"UPDATE reviews set comment='{comment}', stars={stars} where id={review_id}")
        db.close()
        return redirect(url_for('get_food', food_id=food_id))
    db.close()
    return render_template('food.html', food=food, reviews=reviews, comments=comments, stars=stars)

@app.route('/food/all')
def get_all_food():
    user="guest"
    if request.cookies.get('user_id'):
        user_id=request.cookies.get('user_id')
        users={1:'bob',2:'alice'}
        #query the database to get the user info
        user=users[int(user_id)]

    #1 query the darabase,get all foods
    #2 return a template (html) with the variable results
    db = DatabaseWorker('database.db')
    results = db.search(query='SELECT * from foods', multiple=True)
    db.close()
    return render_template('foods.html',foods=results, name=user)

@app.route('/profile')
def profile():
    # if request.cookies.get('user_id'):
    if session['user_id']:
        user_id=session['user_id']
        # user_id=request.cookies.get('user_id')
        users={1:'bob',2:'alice'}
        #query the database to get the user info
        user=users[int(user_id)]
        return  f'<h1>Hello {user}</h1>'
    return redirect((url_for('login')))

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login')))
    # response.set_cookie('user_id', "", expires=0)

    #destory thr session
    session.pop('user_id', None)
    return response


@app.route('/', methods=['GET','POST'])
def login():  # put application's code here
    if request.method=='POST':
        uname=request.form.get('uname')
        password=request.form.get('psw')
        #Check database for user, then compare hash for the password
        if uname=="bob":
            #valid login, create a cookie
            user_id = 1
            #using cookies
            # response = make_response(redirect(url_for('get_all_food')))
            # response.set_cookie('user_id',f"{user_id}")
            session['user_id'] = user_id
            return redirect(url_for('get_all_food'))
    return render_template('login2.html')


if __name__ == '__main__':
    app.run()

