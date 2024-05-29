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

By using the post method, I receive the values input by user by using the `request` library with `POST` method.
I imported `re` and used `match()` module to verify whether valid email or not.

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
To validate the input values, I used boolean. Depending on the input, error become `True` and valid will become `False`.
To prevent the duplication of username, I searched `username` in the database of `users` and I compared stored username with the input username by using for loop.
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
I created hash function in the different file called `tools.py` to prevent the main coe gets longer.
I imported `sha256_crypt` module and create the function to make hash.

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
If all input data fulfill the validation and complete hash, then these values inserted into the table `users`.

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
Using for loop for the values in `users` table, I compare signature stored in the table with hash_text then if it matches, the system recognizes it is a valid login.
If the login succeed, it starts session with `user_id`.
he purpose of using sessions in web development is to maintain stateful information across multiple requests within a user's browsing session. 
Sessions enable the storage and retrieval of user-specific data, enhance security, and facilitate the creation of personalized and interactive web experiences.[^2]
If the login doesn't succeed, it returns error and error message appears on the text.

#### logging validation
To ensure which user make a post or write a comment, the website requires login before the user take actions on the website.
In order to identify whether user logged in or not, I created a `logging` function in `tools.py` so that I can use this function without less code in the main python file.

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
First, it checks the login status of user, and if the user id not logged in, then the page redirect to login page.
Then, I used 'POST' method, to receive the inputs and stores values in the table `posts` with date of post by using 'datetime' package.

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
In html file, I used 'input' which type is `file`. I set acceptable file types in only phot files.

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

#### option menu
I created the system to select the group of the subject and subject in which the user's post belongs.
Each subject belongs to the specific group, so the website makes the user to select group first, then depending on the group the user choose, it shows dropdown menu of subject.
To make this sub-select option menu, I used javascript and referred this website.[^4]

```.py
# post.js
document.addEventListener('DOMContentLoaded', function() {
    // Hide all sub select boxes initially and remove their name attributes
    var allSubBoxes = document.getElementsByClassName("sub_select");
    for (var i = 0; i < allSubBoxes.length; i++) {
        allSubBoxes[i].style.display = 'none';
        allSubBoxes[i].removeAttribute('name'); // Ensure name attribute is removed
    }

    // Process each pulldown set
    var mainBoxes = document.getElementsByClassName('pulldownset');
    for (var i = 0; i < mainBoxes.length; i++) {
        var mainSelect = mainBoxes[i].getElementsByClassName("main_select")[0]; // Get the main select element
        if (mainSelect) { // Check if mainSelect is found
            mainSelect.onchange = function () {
                // Hide all sub select boxes within the same pulldown set and remove their name attributes
                var subBoxes = this.parentNode.getElementsByClassName("sub_select");
                for (var j = 0; j < subBoxes.length; j++) {
                    subBoxes[j].style.display = 'none';
                    subBoxes[j].removeAttribute('name'); // Remove name attribute
                }
                // Show the selected sub select box and set its name attribute
                if (this.value) {
                    var targetSub = document.getElementById(this.value);
                    if (targetSub) { // Check if targetSub is found
                        targetSub.style.display = 'inline';
                        targetSub.setAttribute('name', 'subject'); // Set the name attribute
                    }
                }
            }
        }
    }
});
```
```.py
    <div class="pulldownset">
    <select name="genre" class="main_select" requierd>
         <option value="">Select the group</option>
        <option value="G1">1: Studies in Language and Literature)</option>
        <option value="G2">2: Language Acquisition</option>
        <option value="G3">3: Individuals and Societies</option>
        <option value="G4">4: Experimental Sciences</option>
        <option value="G5">5: Mathematics</option>
        <option value="G6">6: The Arts</option>
    </select>

    <select id="G1" name="subject" class="sub_select" requierd>
        <option value="">Select the subject</option>
        <option value="EA">English A</option>
        <option value="JA">Japanese A</option>
    </select>

    <select id="G2" name="subject" class="sub_select" requierd>
    ......
    </select>
    
    <select id="G3" name="subject" class="sub_select" requierd>
    .......
    </select>
    
    <select id="G4" name="subject" class="sub_select" requierd>
    ......
    </select>
    
```

### like system (Success Criteria 3)
To meet the criteria, I created the like system which the logged-in users to like posts.

```.py
def like(post_id):
    db_connection = DatabaseWorker("project4")
    if not logging():
        db_connection.close()
        return redirect(url_for('login'))
    if logging():
        user_id = session['user_id']
        user_like_with = db_connection.search(query=f"SELECT * from likes where post_id={post_id} and user_id={user_id}",multiple=False)
        liked = user_like_with is not None  # True: if liked, False: if not liked
        if liked:
            db_connection.run_query(query=f"DELETE FROM likes WHERE post_id={post_id} and user_id={user_id}")
        else:
            db_connection.run_query(query=f"INSERT INTO likes (post_id, user_id) values ({post_id},{user_id})")
        db_connection.close()
        return redirect(url_for('main'))
```
When the user click a like button, the system checks the login status of a user.
If the user hasn't logged in yet, the system redirect to login page.
If the user has already logged in, then system obtains the `user_id`.
The system search the table 'like' to check whether the user has already liked the post or not.
If user already like the post, then the system remove like when the like button clicked.
If not, the system add like with 'post_id' and 'user_id'.


### follow system (Success Criteria 4)
To meet the criteria, I created follow / unfollow system.
It allows user to follow other users or topics that they are interested in.

#### user follow
```.py
def user_follow(f_user_id):
    db_connection = DatabaseWorker("project4")
    if logging():
        user_id = session['user_id']
    else:
        return redirect(url_for('login'))
    f_user_with = db_connection.search(query=f"SELECT * from user_follows where user_id={user_id} and following_user_id={f_user_id}",multiple=False)
    following = f_user_with is not None  # True: if following, False: if not following
    if following:
        db_connection.run_query(query=f"DELETE FROM user_follows WHERE user_id={user_id} and following_user_id={f_user_id}")
    else:
        db_connection.run_query(query=f"INSERT INTO user_follows (user_id, following_user_id) values ({user_id},{f_user_id})")
    db_connection.close()
    return redirect(url_for('profile', user==f_user_id))
```
This systems allows only logged-in user to use follow function, so it first identify the login status of user.
If the user hasn't logged in yet, it redirect to login page.
When the follow button is clicked on, the system obtain the clicked user's user id and give this value to `user_follow` function, and this is saved as `f_user_id`.
First, by using the given `f_user_id`, the system checks whether the user currently follows that `f_user_id` from the table `user_follows`, and returns the value of `f_user_with`.
`f_user_with` returns `None` if the user hasn't followed the selected user.
If `f_user_with` is not `None`, it is `following == True`, and if it's not `following==False`.
From the above process, the system identify the following status.
Then, if the user already followed the clicked user, it removes following record from the table `user_follows`.
If the user hasn't followed the clicked user, it inserts user's id and selected following user's id in the table `user_follows`.

#### topic follow


### profile (Success Criteria 5)
To meet the criteria, system provides user's relevant information on the profile page.
This information includes, username, user's profile photo, profile message, the number of posts, the number of following users, the number of followed users, and posts the user made.
If it is your profile, the user can edit, photo and message. If it is other user's profile, the user can follow or unfollow from there.


### sending emails (Success Criteria 7)

### UI design

## CriteriaD
Please watch this vide.

## CriteriaE

## Citation
[^1]: Majeed, Umer, et al. “Blockchain for IoT-Based Smart Cities: Recent Advances, Requirements, and Future Challenges.” Journal of Network and Computer Applications, vol. 181, 1 May 2021, pp. 103007–103007, www.sciencedirect.com/topics/computer-science/hash-function#:~:text=Hash%20functions%20are%20used%20for,the%20hash%20itself%20is%20signed., https://doi.org/10.1016/j.jnca.2021.103007. Accessed 29 May 2024.
[^2]: EITCA Academy. “What Is the Purpose of Using Sessions in Web Development? - EITCA Academy.” EITCA Academy, 8 Aug. 2023, eitca.org/web-development/eitc-wd-pmsf-php-and-mysql-fundamentals/expertise-in-php/sessions/examination-review-sessions/what-is-the-purpose-of-using-sessions-in-web-development/#:~:text=To%20summarize%2C%20the%20purpose%20of,personalized%20and%20interactive%20web%20experiences. Accessed 29 May 2024.
[^3]: mule. “フォームで画像選択時にプレビュー表示する【HTML・CSS・JQuery】.” Muleの技術ブログ, 25 June 2022, tool-engineer.work/article50/. Accessed 29 May 2024.
[^4]:“【HTML】複数のプルダウンを連動させる方法とは？JavaScriptのコードも徹底解説 - WEBCAMP MEDIA.” WEBCAMP MEDIA, 15 Sept. 2021, web-camp.io/magazine/archives/85111. Accessed 29 May 2024.








