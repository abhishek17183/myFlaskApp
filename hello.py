from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///iNotes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Notes(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    notes = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self)-> str:
        return f"{self.sno} - {self.title}"

@app.route('/',methods=["GET","POST"])
def hello_world():
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['description']
        note=Notes(title=title,notes=desc)
        db.session.add(note)
        db.session.commit()
        
    allNotes=Notes.query.all()
    return render_template('index.html',allNotes=allNotes)
    
    
@app.route('/update/<int:sno>',methods=["GET","POST"])
def update(sno):
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['description']
        note=Notes.query.filter_by(sno=sno).first()
        note.title=title
        note.notes=desc
        db.session.add(note)
        db.session.commit()
        return redirect('/')
    note=Notes.query.filter_by(sno=sno).first()
    return render_template('update.html',note=note)
    
@app.route('/delete/<int:sno>')
def delete(sno):
    note=Notes.query.filter_by(sno=sno).first()
    db.session.delete(note)
    db.session.commit()
    return redirect('/')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)