from flask import Flask, render_template, redirect, request, flash, session
from forms import new_feedback_form, update_feedback_form, user_form, login_form
from models import Feedback, User, db, connect_db
from werkzeug.exceptions import Unauthorized
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'



app.app_context().push()
connect_db(app)
db.create_all()

@app.route('/')
def root():
    return redirect('/register')

@app.route('/register', methods=['GET','POST'])
def register():
    form = user_form();

    if "username" in session:
        return redirect(f"/users/{session['username']}")
    else:
        if form.validate_on_submit():
            username = form.username.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data
            

            user = User.register(username, password, first_name, last_name, email)
        
            db.session.commit()

            session['username'] = user.username

            return redirect(f"/users/{user.username}")
        else:
            return render_template('index.html', form=form)



@app.route('/login', methods=["GET","POST"])
def login():
    form = login_form();

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username and password combination"]
            return render_template("login.html", form=form)

    return render_template('login.html', form = form)

@app.route('/logout')
def logout():

    session.pop("username")
    return redirect("/login")

@app.route('/users/<username>')
def user_info(username):
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    else:
        user = User.query.get(username)

        return render_template('user_info.html', user = user)
    
@app.route('/users/<username>/feedback/add', methods=["GET","POST"])
def add_feedback(username):

    if "username" not in session or username != session['username']:
        raise Unauthorized()
    else:

        form = new_feedback_form()

        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data

            feedback = Feedback(
                title = title,
                content = content,
                username = username
            )

            db.session.add(feedback)
            db.session.commit()

            return redirect(f"/users/{username}")
        
        else:

            return render_template('add_feedback.html', form = form)
        

@app.route("/feedback/<feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):

    feedback =  Feedback.query.get_or_404(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    

    else:
        db.session.delete(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    
@app.route("/feedback/<feedback_id>/update", methods=['GET','POST'])
def update_feedback(feedback_id):

    feedback = Feedback.query.get_or_404(feedback_id)
    form = update_feedback_form()

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()
    
    if form.validate_on_submit():
        title = form.title.data,
        content = form.content.data

        feedback.title = title
        feedback.content = content
        
        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    
    else:

        return render_template('edit_feedback.html', form = form, feedback=feedback)
    
@app.route("/users/<username>/delete")
def delete_user(username):

    
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    else:

        user = User.query.get_or_404(username)

        
        db.session.delete(user)
        db.session.commit()
        session.pop("username")

        return redirect('/')