from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///student.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class student(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    mailId = db.Column(db.String(200), nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.name} - {self.mailId}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=="POST":
        name = request.form['studName']
        mailId = request.form['mailid']
        stud = student(name=name, mailId=mailId)
        db.session.add(stud)
        db.session.commit()     
    allStudents = student.query.all()
    return render_template('index.html', allStudents=allStudents)

@app.route('/delete/<int:sno>')
def delete(sno):
    stud = student.query.filter_by(sno=sno).first()
    db.session.delete(stud)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        name = request.form['studName']
        mailId = request.form['mailid']
        stud = student.query.filter_by(sno=sno).first()
        stud.name = name
        stud.mailId = mailId
        db.session.add(stud)
        db.session.commit() 
        return redirect("/")
        
    stud = student.query.filter_by(sno=sno).first()
    return render_template('update.html', stud=stud)

if __name__ == "__main__":
    app.run(debug=True, port=8000)