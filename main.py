from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory,send_file
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE IN DB
class User(UserMixin,db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("index.html")

#
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_user():
    return dict(logged_in=current_user.is_authenticated)

@app.route('/register',methods =  ['GET','POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    hashed_password = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=8
        )
    #Handles the case where the user is alread logged in
    if User.query.filter_by(email=email).first():
            flash("You've already signed up with that email. Please log in instead.")
            return redirect(url_for("login"))
    new_user = User(name = name,email = email, password = hashed_password)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user) 
    return render_template('secrets.html',name = request.form["name"])

@app.route('/login',methods = ['POST','GET'])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        #HANDLE USER NOT FOUND OR WRONG PASSWORD CASES
        if not user:
            flash("That email does not exist. Please try again.")
            return redirect(url_for("login"))

        if not check_password_hash(user.password, password):
            flash("Password incorrect. Please try again.")
            return redirect(url_for("login"))
        
        #HANDLE USER LOGIN
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("secrets"))
        else:
            return "Invalid credentials"

    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html")


from flask_login import logout_user

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route('/download')
@login_required
def download(filename):
    return send_from_directory(directory="static",path = "files/cheat_sheet.pdf", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
