import pymysql
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from flask_ckeditor import CKEditor
from datetime import date, datetime
import pymysql
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

from password import password

userdb = pymysql.connect(host="localhost", user="root", password=password, database="blogusers")
usercursor = userdb.cursor()

app = Flask(__name__)
ckeditor = CKEditor(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DATABASE
db = pymysql.connect(host="localhost", user="root", password=password, database="updatedmovieblog")
cursor = db.cursor()

# Configure flask-login's login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Specify the login view


# Create a user_loader callback
@login_manager.user_loader
def load_user(user_id):
    return User.get_user(user_id)


class User(UserMixin):
    def __init__(self, id, email, password, name):
        self.id = id
        self.email = email
        self.password = password
        self.name = name

    @staticmethod
    def get_user(user_id):
        usercursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        data = usercursor.fetchone()
        if data:
            return User(data[0], data[1], data[2], data[3])
        return None

    def get_id(self):
        return str(self.id)


# CONFIGURE TABLE cursor.execute( "CREATE TABLE BlogPost(fid INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(250),
# subtitle VARCHAR(250), date VARCHAR(250), body VARCHAR(1000), author VARCHAR(250), img_url VARCHAR(250))") db.commit()

class PostForm(FlaskForm):
    title = StringField(label="Blog Title", validators=[DataRequired(), ])
    subtitle = StringField(label="Subtitle", validators=[DataRequired(), ])
    author = StringField(label="Author Name", validators=[DataRequired(), ])
    img_url = StringField(label="Image URL", validators=[DataRequired(), ])
    content = CKEditorField("content")
    submit = SubmitField(label="Submit Post")


def insert_data(fid, title, subtitle, fdate, body, author, img_url):
    sql = "INSERT INTO BlogPost (fid, title, subtitle, date, body, author, img_url) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (fid, title, subtitle, date, body, author, img_url)
    cursor.execute(sql, values)
    db.commit()
    print("movie inserted successfully.")


#
# insert_data(0, "Abiagail",
#             "A crew are hired to kidnap a little girl (Weir) and keep her in a secure location. The little girl is a "
#             "vampire.",
#             "19 Apr 2024",
#             "In 1907, twist-in-the-tale specialist O. Henry published The Ransom Of Red Chief, a short story about "
#             "kidnappers whose victim is so obnoxious they wind up paying the brat’s family to take him back. It’s "
#             "been repeatedly adapted, officially and unofficially, including versions by Yasujiro Ozu and Howard "
#             "Hawks. Abigail offers a new spin. Twelve-year-old ballerina — Alisha Weir, in a ferocious "
#             "how-not-to-be-typecast-forever-as-Matilda-from-Matilda-The-Musical turn — is actually an ancient, "
#             "bloodthirsty, rage-fuelled vampire with extreme daddy issues.", "Henry",
#             "https://www.empireonline.com/movies/reviews/abigail/")
# insert_data(2,"Baby Reindeer","When Donny Dunn (Richard Gadd) gives a woman named Martha (Jessica Gunning) a free cup "
#                               "of tea in the pub where he works, little does he know that this one simple act of "
#                               "kindness will soon transform into a nightmare that changes his life forever.","15 April 2024","Making the move from Edinburgh Fringe to the West End and now Netflix, Baby Reindeer stars a fictionalised version of comedian Richard Gadd, who strikes up a flirty friendship with Martha (Jessica Gunning), a dishevelled, somewhat unhinged woman who claims to be a hotshot lawyer yet can't afford a Diet Coke or cup of tea. The struggling comic 'instantly felt sorry for her', Donny reveals via increasingly candid narration. But when the attention Martha gives him descends into full-blown stalking — including a total of 41,071 emails and 350 hours of voicemail — Donny is forced to reckon with past traumas and his own culpability in what happens next.","David Opie","https://www.empireonline.com/tv/reviews/baby-reindeer/")
# insert_data(3,"Tranformers","Transformers One Trailer Breakdown","18 April2024","Can robots have a coming of age story? Well, Optimus Prime, Megatron and their assembled mechanical factions are alien robots known as Transformers, so, you know, anything is possible. And indeed, Transformers One takes us back to a time before sides had been taken in the war between the Autobots and Decepticons, when Optimus was known as Orion Pax, and Megatron went by the slightly less imposing moniker of D-16.","James White","https://www.empireonline.com/movies/features/transformers-one-director-interview-josh-cooley-optimus-megatron-cybertron/")
# insert_data(4,"Fallout Season 2","Fallout Season 2 Confirmed At Prime Video","19 April 2024","The apocalypse was just the beginning. A week ago, Prime Video unleashed its streaming series adaptation of the ultra-popular Fallout video games – bringing a post-nuclear wasteland filled with vault-dwellers, metal-clad soldiers and irradiated ghouls to fans old and new. And not only has Season 1 been a critical hit, receiving considerable acclaim in reviews and notices as one of the best game-to-screen adaptations, but it’s clearly been a ratings winner for the streamer too. So much so that, within seven days of its entire-season drop, Amazon has committed to more mutant mayhem: Fallout will officially be back for Season 2.","Ben Travis","https://www.empireonline.com/tv/news/fallout-season-2-confirmed-prime-video/")
# insert_data(5,"Sisu","For the Nazis","24 may 2023","It’s 1944, and although the Nazis are on the retreat in Finland, they’re determined to burn the country to bits as they go. Meanwhile, in the Lapland wilderness, lone war veteran Aatami Korpi (Tommila), having literally struck gold, crosses paths with them. It’s an unfortunate situation. (For the Nazis, that is.)","Alex Godfrey","https://www.empireonline.com/movies/reviews/sisu/?itm_source=Bibblio&itm_campaign=Bibblio-related&itm_medium=Bibblio-footer-1")


def get_all_posts():
    posts = []

    try:
        query = "SELECT * FROM blogpost"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            post = {
                "id": row[0],
                "title": row[1],
                "subtitle": row[2],
                "date": row[3],
                "body": row[4],
                "author": row[5],
                "img_url": row[6]
            }
            posts.append(post)
    except pymysql.Error as e:
        print(f"Error while retrieving data: {e}")
    finally:
        db.close()
    return posts


@app.route('/')
@login_required
def home():
    posts = get_all_posts()
    return render_template("index.html", all_posts=posts)


# TODO: Add a route so that you can click on individual posts.
@app.route('/posts/<int:post_id>')
def show_post(post_id):
    # TODO: Retrieve a BlogPost from the database based on the post_id
    posts = get_all_posts()
    requested_post = None

    for post in posts:
        if post["id"] == post_id:
            requested_post = post
            break

    if requested_post:
        return render_template("post.html", post=requested_post)
    else:
        return "post not found"


# TODO: add_new_post() to create a new blog post
@app.route("/new-post", methods=["POST", "GET"])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        subtitle = form.subtitle.data
        author = form.author.data
        img_url = form.img_url.data
        content = form.content.data
        datenow = date.today().strftime("%B %d, %Y")

        cursorr = db.cursor()
        sql = "INSERT INTO BlogPost (title, subtitle, date, body, author, img_url) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (title, subtitle, datenow, content, author, img_url)
        cursorr.execute(sql, values)
        db.commit()
        cursorr.close()
        db.close()
        flash(f"{title} successfully added to books")
        return redirect(url_for("home"))

    return render_template("make-post.html", form=form)


# TODO: edit_post() to change an existing blog post
@app.route('/edit-post/<int:post_id>', methods=["GET", "POST"])
def edit_post(post_id):
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        subtitle = form.subtitle.data
        author = form.author.data
        img_url = form.img_url.data
        content = form.content.data
        datenow = date.today().strftime("%B %d, %Y")

        cursorr = db.cursor()
        sql = "UPDATE BlogPost SET subtitle = %s, date = %s, body = %s, author = %s, img_url = %s WHERE fid = %s"
        values = (subtitle, datenow, content, author, img_url, {post_id})
        cursor.execute(sql, values)
        db.commit()
        cursorr.close()
        db.close()
        return redirect(url_for("home"))

    return render_template("make-post.html", form=form, is_edit=True)


# TODO: delete_post() to remove a blog post from the database
@app.route("/delete/<int:post_id>", methods=["GET", "POST"])
def delete_post(post_id):
    cursorr = db.cursor()
    cursor.execute(f"DELETE FROM BlogPost WHERE fid = {post_id}")
    db.commit()
    cursorr.close()
    db.close()
    return redirect(url_for("home"))


# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        # Hashing and salting the password entered by the user
        hash_and_salted_password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=16)
        new_user = User(None, email, hash_and_salted_password, name)
        # Storing the hashed password in our database
        usercursor.execute("INSERT INTO users (email, password, name) VALUES (%s, %s, %s)",
                           (new_user.email, new_user.password, new_user.name))
        userdb.commit()
        flash("You have been registered successfully!", "success")

        # Log in and authenticate the user after adding details to the database
        login_user(new_user)

        # Redirect to the secrets page
        return redirect(url_for("home"))

    return render_template("register.html")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/login', methods=["POST", "GET"])
def login():
    login_status = False
    if request.method == "POST":
        email = request.form.get('email')
        userpassword = request.form.get('password')
        print(email)
        print(password)
        # Find user by email
        usercursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user_data = usercursor.fetchone()

        if user_data:
            print(user_data)
            stored_password = user_data[0]
            print(f"DEBUG: User found with email {email}. Stored password hash: {stored_password}")
            if check_password_hash(stored_password, userpassword):
                # Load the user from the database
                user = User(user_data[0], user_data[1], user_data[2], user_data[3])
                login_user(user)
                print(f"DEBUG: User {email} logged in successfully.")
                login_status = True
                return render_template("index.html")
            else:
                flash("Incorrect password. Please try again.")
                print(f"DEBUG: Incorrect password for user {email}.")
        else:
            flash("Email not found. Please register first.")
            print(f"DEBUG: Email {email} not found in the database.")

    return render_template("login.html", loggged_in=login_status)


if __name__ == "__main__":
    app.run(debug=True, port=5003)
