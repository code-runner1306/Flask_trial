from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class todo(db.Model):
    sno= db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    desc=db.Column(db.String(200), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.now())

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    
@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        Todo=todo(title=title,desc=desc)
        db.session.add(Todo)
        db.session.commit()
    alltodo = todo.query.all()
    return render_template('index.html',alltodos=alltodo)
    #return 'Hello, World!'

@app.route('/update//<int:sno>', methods=['GET','POST'])
def update(sno):
    Todo=todo.query.filter_by(sno=sno).first()
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        Todo=todo.query.filter_by(sno=sno).first()
        Todo.title=title
        Todo.desc=desc
        db.session.commit()
        return redirect("/")
    return render_template("update.html",TODO=Todo)

@app.route('/delete//<int:sno>')
def delete(sno):
    alltodo = todo.query.filter_by(sno=sno).first()
    db.session.delete(alltodo)
    db.session.commit()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True,port=8000)
