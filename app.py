from flask import Flask, render_template, request, redirect, url_for
from models import db, Note
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    semester = request.args.get("semester")
    if semester:
        notes = Note.query.filter_by(semester=semester).all()
    else:
        notes = Note.query.all()
    return render_template("index.html", notes=notes)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        title = request.form["title"]
        subject = request.form["subject"]
        semester = request.form["semester"]
        file = request.files["file"]

        filename = file.filename
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        note = Note(
            title=title,
            subject=subject,
            semester=semester,
            filename=filename
        )
        db.session.add(note)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)
