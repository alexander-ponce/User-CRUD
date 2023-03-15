from flask_app import app
from flask import Flask, render_template, request, redirect, session
from flask_app.models.user import Users
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import flash

@app.route("/")
def index():
    
    return render_template("register_login.html")


@app.route("/create/account", methods=["POST"])
def create_account():
    # validate the form here ...
    # create the hash
    if not Users.validate_user(request.form):
        return redirect ("/")
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    # print(pw_hash)
    # put the pw_hash into the data dictionary
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    # Call the save @classmethod on User
    id = Users.save(data)
    # store user id into session
    session['user_id'] = id

    # return redirect ('user/account/{user_in_db}')
    return redirect ('/user/account')



@app.route('/login', methods=['POST'])
def login_user():
    if not Users.validate_login(request.form):
        return redirect('/')
    email_data={
        'email':request.form['login_email']
    }
    returning_user= Users.get_by_email(email_data)
    session['user_id']= returning_user.id
    return redirect('/user/account')


# @app.route("/login", methods=["POST"])
# def login_account():
#     # see if the username provided exists in the database
#     # data = { "email" : request.form["email"] }
#     user_in_db = Users.get_by_email(request.form)
#     # user_in_db = Users.get_by_email(request.form['email'])
#     # user is not registered in the db
#     if not user_in_db:
#         flash("Invalid Email/Password")
#         return redirect('/')
#     if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
#         # if we get False after checking the password
#         flash("Invalid Email/Password")
#         return redirect('/')
#     # if the passwords matched, we set the user_id into session
#     session['user_id'] = user_in_db.id
#     # never render on a post!!!
#     return redirect('/user/account')

#     return render_template ('post_login.html', user_id = Users.get_one(id_data) )


@app.route('/user/account')
# @app.route('/user/account/<int:id>')
def user_account():
    if 'user_id' not in session:
        return redirect ('/logout')
    id_data={
        'id': session['user_id']
    }
    user_id= Users.get_one(id_data)
    return render_template ('post_login.html', user_id = user_id)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)



# #included user validation
# @app.route('/input_user', methods = ["POST"])
# def input():
#     data = {
#         "first_name": request.form["first_name"],
#         "last_name" : request.form["last_name"],
#         "email" : request.form["email"]
#     }
#     if not Users.validated_user(request.form):
#         return redirect ("/")
#     # We pass the data dictionary into the save method from the Friend class.
#     show_user=Users.save(data)
#     # Don't forget to redirect after saving to the database.
#     return redirect(f'/user/show/{show_user}')
#     # return redirect('/display_users')

# #Show user by ID
# @app.route('/user/show/<int:id>')
# def show_user(id):
#     data = {
#         'id': id
#     }
#     # calling the get_one method and supplying it with the id of the friend we want to get
#     return render_template("read_one.html", user= Users.get_one(data))


# @app.route('/display_users')
# def display():
#     return render_template("/read.html", all_users=Users.get_all())

# @app.route('/user/edit/<int:id>')
# def edit_user(id):
#     data = {
#         'id': id
#     }
#     return render_template("/edit_user.html", user= Users.get_one(data))

# @app.route('/user/update',methods=['POST'])
# def update_users():
#     Users.update(request.form)
#     return redirect('/display_users')

# @app.route('/user/delete/<int:id>')
# def delete_user(id):
#     data = {
#         'id': id
#     }
#     Users.delete(data)
#     return redirect('/display_users' )



