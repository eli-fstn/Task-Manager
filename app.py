from flask import Flask, request, render_template, redirect, url_for, session
from datetime import timedelta, datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret_key"
app.permanent_session_lifetime = timedelta(minutes=5)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///taskmanager.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(10), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<Task {self.id}>"

@app.route("/", methods=["POST", "GET"])
def add_Task():
    if request.method == "POST":
        task_content = request.form.get("content")
        subject_content = request.form.get("subject")
        new_task = Todo(content=task_content, subject=subject_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print("Error adding task:", e)
            return 'There was an issue adding task.'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("data.html", tasks=tasks)
    
@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return 'There was an error deleting your task.'

@app.route("/update/<int:id>", methods=["POST", "GET"])
def update(id):
    task = Todo.query.get_or_404(id)
    
    if request.method == "POST":
        task.content = request.form.get("content")
        task.subject = request.form.get("subject")
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue updating your task"
    else:
        return render_template("update.html", task=task)
    
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        keyword = request.form.get("keyword")
        results = Todo.query.filter(Todo.content.like(f"%{keyword}%")).all()
        return render_template("search.html", tasks=results)
    return render_template("search.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)