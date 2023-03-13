from flask import Flask
app=Flask(__name__)
app.secret_key = "secretsecret"

# from flask_app.controllers import user_routes