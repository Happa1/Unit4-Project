# Unit4 Project

## CriteriaC Development


### login / registration System (Success Criteria 1)
#### registration


```.pycon
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

        users_table = db_connection.search(query="SELECT * FROM users", multiple=True)

        for row in users_table:
            if row[1]==uname:
                user_err=True
                print("the user name already exist")
                valid=False
                break

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


        if valid:
            query = f"""INSERT INTO users (username,password,email,pro_msg,pro_img)
            values ('{uname}','{hash}','{email}','','blank_user.jpeg');
            """
            db_connection.run_query(query=query)
            db_connection.close()
            return redirect(url_for('login'))

        db_connection.close()
        return render_template('register.html', email_err=email_err, psw_err=psw_err, psw_cnf_err=psw_cnf_err, user_err=user_err)
    db_connection.close()
    return render_template('register.html')
```


### posting system (Success Criteria 2)



### like system (Success Criteria 3)



### follow system (Success Criteria 4)



### profile (Success Criteria 5)
### upload images (Success Criteria 6)
### sending emails (Success Criteria 7)

## CriteriaD
## CriteriaE

## Citation
[^1]

