import pymysql
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from flask_ckeditor import CKEditor
from datetime import date, datetime

from password import password

'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''

app = Flask(__name__)
ckeditor = CKEditor(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DATABASE
db = pymysql.connect(host="localhost", user="root", password=password, database="updatedmovieblog")
cursor = db.cursor()


# CONFIGURE TABLE
# cursor.execute(
#     "CREATE TABLE BlogPost(fid INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(250), subtitle VARCHAR(250), date VARCHAR(250), body VARCHAR(1000), author VARCHAR(250), img_url VARCHAR(250))")
# db.commit()

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
    db = pymysql.connect(host="localhost", user="root", password=password, database="updatedmovieblog")
    cursor = db.cursor()

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
        cursor.execute(sql, values)
        db.commit()
        cursorr.close()
        db.close()
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


if __name__ == "__main__":
    app.run(debug=True, port=5003)
