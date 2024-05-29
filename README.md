# Unit4 Project

## CriteriaC Development


### login / registration System (Success Criteria 1)
#### registration
To meet the criteria, I made a registration system. This registration system receive username, email, and password as inputs.
```.py
def register():
    db_connection = DatabaseWorker("project4")
    if request.method=='POST':
        uname=request.form.get('uname')
        email=request.form.get('email')
        match = re.match('[A-Za-z0-9._+]+@[A-Za-z]+.[A-Za-z]', email)
        password = request.form.get('psw')
        conf_password = request.form.get('psw_conf')
```

By using the post method, I receive the values input by user by using the 'request' library with 'POST' method.
I imported 're' and used 'match()' module to verify whether valid email or not.

```.py
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
```
To validate the input values, I used boolean. Depending on the input, error become 'True' and valid will become 'False'.
To prevent the duplication of username, I searched 'username' in the database of 'users' and I compared stored username with the input username by using for loop.
If the username has been used, then it returns error in username and set valid.
In other cases, such as invalid form of email, less than 8 characters for password, and unmatch of password and confirmed password, it returns error and appeared the error message on the text.


To enhance the security I decided to use hash. 
Hash functions are used for data integrity and often in combination with digital signatures. With a good hash function, even a 1-bit change in a message will produce a different hash (on average, half of the bits change). With digital signatures, a message is hashed and then the hash itself is signed. [^1]

```.py
# tools.py
from passlib.hash import sha256_crypt

hasher = sha256_crypt.using(rounds=30000)

def make_hash(text:str):
    return hasher.hash(text)
```
I created hash function in the different file called 'tools.py' to prevent the main coe gets longer.
I imported 'sha256_crypt' module and create the function to make hash.

```.py
from tools import make_hash, check_hash
        hash_text=f"name{uname}, pass{password}"
        hash=make_hash(hash_text)


        if valid:
            query = f"""INSERT INTO users (username,password,email,pro_msg,pro_img)
            values ('{uname}','{hash}','{email}','','blank_user.jpeg');
            """
            db_connection.run_query(query=query)
            db_connection.close()
            return redirect(url_for('login'))
```
By using username and password, I create hashed signature.
If all input data fulfill the validation and complete hash, then these values inserted into the table 'users'.

**password entering**


#### login
To meet the criteria, I created login system which requires username and password for logging. 
```.py
def login():
    db_connection = DatabaseWorker("project4")
    login_err=False
    if request.method=='POST':
        uname=request.form.get('uname')
        password=request.form.get('psw')
        #Check database for user, then compare hash for the password
        results=db_connection.search(query="""SELECT * FROM users""", multiple=True)
        for row in results:
            signature=row[2] #hash text
            hash_text=f"name{uname}, pass{password}"
            valid=check_hash(hashed_text=signature, text=hash_text)
            if valid:
                user_id = row[0]
                session['user_id'] = user_id
                return redirect(url_for('main'))
            else:
                login_err=True
```
First, I received username and password as inputs. Then, create hash_text with inputted username and password. 
Using for loop for the values in 'users' table, I compare signature stored in the table with hash_text then if it matches, the system recognizes it is a valid login.
If the login succeed, it starts session with 'user_id'.
he purpose of using sessions in web development is to maintain stateful information across multiple requests within a user's browsing session. 
Sessions enable the storage and retrieval of user-specific data, enhance security, and facilitate the creation of personalized and interactive web experiences.[^2]
If the login doesn't succeed, it returns error and error message appears on the text.

#### logging validation
To ensure which user make a post or write a comment, the website requires login before the user take actions on the website.
In order to identify whether user logged in or not, I created a 'logging' function in 'tools.py' so that I can use this function without less code in the main python file.

```.py
def logging():
    login=False
    user_id = session.get('user_id')  # get()メソッドを使って安全に取得
    if user_id:
        login = True
    return login
```


### posting system (Success Criteria 2, Success Criteria 6)
To meet the criteria, I created posting system that a user can post a question and photo on the website.
This posting system requires question, photo, group of subject, and subject as inputs.

```.py
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
            subject=request.form.get('subject')
            print(subject)
            query = """
            INSERT INTO posts (date, post_text, user_id, photo, genre, subject) 
            VALUES (?, ?, ?, ?, ?, ?)
            """
            values = (date, text, user_id, file_name, genre, subject)
            db_connection.run_query(query=query, params=values)
            db_connection.close()
            return redirect(url_for('main'))
        db_connection.close()
        return render_template('post.html', logging=logging())
    else:
        return redirect(url_for('login'))

```
First, it checks the login state of user, and if the user id not logged in, then the page redirect to login page.
Then, I used 'POST' method, to receive the inputs and stores values in the table 'posts' with date of post by using 'datetime' package.

#### upload photo
```.py
#html
        <div class="image_box">
            <img id="img" accept="image/*" src="/static/image/upload_img.jpeg">
            <div class="buttons">
                <label for="file">
                  <input type="file" name="file" id="form" accept=".jpg, .jpeg, .png, .gif">
                </label>
              <button type="button" id="delete">reset</button>
            </div>
        </div>
```
In html file, I used 'input' which type is 'file'. I set acceptable file types in only phot files.

```.py
#app.py
            file = request.files.get('file')
            file_name = f"{date}_{file.filename}"
            file_path = os.path.join('static/post_image', file_name)
            file.save(file_path)
```
In python file, I receive the name of the file by using 'POST' method and create 'file_name' with date to make the file name unique.
Then, using 'os' package, I store the image in 'post_image' folder in 'static' folder.

#### preview photo
To allow user to see the photo he/she upload, I created the function to show the preview of photo.
To make the preview function, I used javascript and referred this website.[^3]
```.py
#post.js
$('#form').on('change', function (e) {
    var reader = new FileReader();
    reader.onload = function (e) {
        $("#img").attr('src', e.target.result);
    }
    reader.readAsDataURL(e.target.files[0]);
});

// initialize the preview when the reset button is clicked
$('#delete').on('click', function (e) {
  $("#img").attr('src', '/static/image/upload_img.jpeg');
  $("#form").val('');
})
```


### like system (Success Criteria 3)



### follow system (Success Criteria 4)



### profile (Success Criteria 5)
### upload images (Success Criteria 6)
### sending emails (Success Criteria 7)

## CriteriaD
I cite[^1]
## CriteriaE

## Citation
[^1]: Majeed, Umer, et al. “Blockchain for IoT-Based Smart Cities: Recent Advances, Requirements, and Future Challenges.” Journal of Network and Computer Applications, vol. 181, 1 May 2021, pp. 103007–103007, www.sciencedirect.com/topics/computer-science/hash-function#:~:text=Hash%20functions%20are%20used%20for,the%20hash%20itself%20is%20signed., https://doi.org/10.1016/j.jnca.2021.103007. Accessed 29 May 2024.
[^2]: EITCA Academy. “What Is the Purpose of Using Sessions in Web Development? - EITCA Academy.” EITCA Academy, 8 Aug. 2023, eitca.org/web-development/eitc-wd-pmsf-php-and-mysql-fundamentals/expertise-in-php/sessions/examination-review-sessions/what-is-the-purpose-of-using-sessions-in-web-development/#:~:text=To%20summarize%2C%20the%20purpose%20of,personalized%20and%20interactive%20web%20experiences. Accessed 29 May 2024.
[^3]: mule. “フォームで画像選択時にプレビュー表示する【HTML・CSS・JQuery】.” Muleの技術ブログ, 25 June 2022, tool-engineer.work/article50/. Accessed 29 May 2024.









