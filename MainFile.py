from flask import Flask,render_template,request,flash,redirect,url_for,session
from Databases import User,Posts
from flask_bcrypt import generate_password_hash,check_password_hash

app = Flask(__name__)
app.secret_key = "bnvsdnvsfvdvkvnjvdvdkbvdsc"

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    user = Posts.get(Posts.id == id)
    if request.method == "POST":
        names = request.form["names"]
        place = request.form["place"]
        date = request.form["date"]
        time = request.form["time"]
        cost = request.form["cash"]
        content = request.form["content"]
        user.names = names
        user.place = place
        user.date = date
        user.time = time
        user.cost = cost
        user.content = content
        user.save()
        flash("Post Updated Successfully")
        return redirect(url_for('show'))
    return render_template("update.html",user = user)


@app.route('/delete/<int:id>')
def delete(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    owner_id = session['id']
    Posts.delete().where(Posts.id == id).execute()
    flash("Details Deleted Successfully")
    return redirect(url_for('show'))


@app.route('/show')
def show():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    id = session['id']
    users = Posts.select()
    return render_template('events.html', users = users)


@app.route('/',methods=['GET','POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == "POST":
        names = request.form["names"]
        place = request.form["place"]
        date = request.form["date"]
        time = request.form["time"]
        cost = request.form["cash"]
        content = request.form["content"]
        id = session['id']
        Posts.create(names = names, place = place, date = date, time = time,cost=cost,content=content)
        flash("Event Posted Successfully")
        flash("User "+names)
    return render_template("addevents.html")


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == "POST":
        names = request.form["names"]
        email = request.form["email"]
        password = request.form["password"]
        password = generate_password_hash(password)
        User.create(names = names, email = email, password = password)
        flash("Account Created Successfully")
    return render_template("register.html")


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            user = User.get(User.email==email)
            hashed_password = user.password
            if check_password_hash(hashed_password,password):
                flash("Logged in Successfully")
                session['logged_in']=True
                session['names']=user.names
                session['id']=user.id
                return redirect(url_for('show'))
        except User.DoesNotExist:
            flash("Wrong Username or Password")
    return render_template("login.html")


if __name__ == '__main__':
    app.run()










