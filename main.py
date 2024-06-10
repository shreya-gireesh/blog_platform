from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from admin import admin_blueprint



app = Flask(__name__)
app.config['SECRET_KEY'] = 'blog-o-sphere'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Shrgs%40root123@localhost:3306/blog_platform'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.register_blueprint(admin_blueprint, url_prefix='/admin')

# Models
class UserModel(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    user_mail = db.Column(db.String(100),unique=True, nullable=False)
    user_pass = db.Column(db.String(50), nullable=False)
    about_me = db.Column(db.Text, nullable=True)
    status = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<User {self.username}>'


@app.route('/')
def home():
    user = session.get('user', None)
    return render_template("index.html", user = user)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/account')
def account():
    return render_template("account.html")


@app.route('/account/myblogs')
def myblogs():
    return render_template("myblogs.html")


@app.route('/blogs')
def blogs():
    return render_template("blogpage.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/categories')
def categories():
    return render_template("categories.html")


@app.route('/blog')
def blog():
    return render_template("blog.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if 'login-btn' in request.form:
            usermail = request.form.get('usermail')
            password = request.form.get('user_password')
            found_user = UserModel.query.filter_by(user_mail=usermail, user_pass=password).first()
            if found_user:
                session['user'] = found_user.user_name
                return redirect(url_for('home'))
            else:
                flash('User does not exist', 'error')
        if 'reg-btn' in request.form:
            username = request.form.get('user_name')
            usermail = request.form.get('user_mail')
            password = request.form.get('user_pass')
            found_user = UserModel.query.filter_by(user_mail=usermail).first()
            if found_user:
                flash('User already exists! Please login instead.', 'error')
            else:
                new_user = UserModel(user_name=username, user_mail=usermail,user_pass=password)
                db.session.add(new_user)
                db.session.commit()
                flash('User created successfully!', 'success')
            print(f"Received username: {username},email: {usermail}, password: {password}")
    return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('home'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
