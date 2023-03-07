from flask import Flask, render_template, session, redirect, request # added render_template!
from user import Users
app = Flask(__name__)
app.secret_key="rootroot"

@app.route("/")
def index():
    
    return render_template("create.html")

@app.route('/input_user', methods = ["POST"])
def input():
    data = {
        "first_name": request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"]
    }
    # We pass the data dictionary into the save method from the Friend class.
    show_user=Users.save(data)
    # Don't forget to redirect after saving to the database.
    return redirect(f'/user/show/{show_user}')

#Show user by ID
@app.route('/user/show/<int:id>')
def show_user(id):
    data = {
        'id': id
    }
    # calling the get_one method and supplying it with the id of the friend we want to get
    return render_template("read_one.html", user= Users.get_one(data))


@app.route('/display_users')
def display():
    return render_template("/read.html", all_users=Users.get_all())

@app.route('/user/edit/<int:id>')
def edit_user(id):
    data = {
        'id': id
    }
    return render_template("/edit_user.html", user= Users.get_one(data))

@app.route('/user/update',methods=['POST'])
def update_users():
    Users.update(request.form)
    return redirect('/display_users')

@app.route('/user/delete/<int:id>')
def delete_user(id):
    data = {
        'id': id
    }
    Users.delete(data)
    return redirect('/display_users' )

if __name__ == "__main__":
    app.run(debug=True)

