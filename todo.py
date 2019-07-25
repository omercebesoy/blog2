from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy #kütüphaneleri dahil ettik.


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/omerc/Desktop/TodoApp/todo.db' #veritabani ile flask baglantisini yaptik.
db=SQLAlchemy(app)
@app.route("/")
def index():

    todos =Todo.query.all() #classtaki verileri alicaz.
    """if todo.complete == True:
        todo.complete =False
    else:
        todo.complete =True""" 
    return render_template("index.html",todos=todos)
@app.route("/complete/<string:id>") #dinamik url
def completeTodo(id):
    todo = Todo.query.filter_by(id = id).first() #id'si 1 olan veriyi classtan objeye atadik.
    todo.complete =not todo.complete #false ise true,true isede false olacak
    db.session.commit()
    return redirect(url_for("index"))
@app.route("/add",methods=["POST"])
def addTodo():
    title=request.form.get("title") # titleyi formdan aldik.
    newTodo= Todo(title =title,complete=False )
    db.session.add(newTodo) #veritabanina ekledik.
    db.session.commit() #veritabaninda degisti
    return redirect(url_for("index"))
@app.route("/delete/<string:id>")
def delete(id):
    todo=Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))
class Todo(db.Model): #olusturacagimiz tablolalari class tanimlayarak ve database.model olarak icine veri gönderipp yapacagiz.
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(80))
    complete = db.Column(db.Boolean) #bool degiskenli bi degisken olusturduk

if __name__=="__main__":
    db.create_all() # tüm classa yazılan tabloları olusturacak.

    app.run(debug=True)