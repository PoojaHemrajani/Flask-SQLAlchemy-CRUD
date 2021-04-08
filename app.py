from flask import Flask, render_template,request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# class Example(db.Model):
#     __tablename__ = 'example'
#     id = db.Column('id', db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     username = db.Column(db.String(80), unique=True, nullable=False)

class Products(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(300),unique=True, nullable=False)
    price = db.Column('price', db.Integer, nullable=False)    


@app.route('/')
def view():
    data = Products.query.all()
    return render_template('index.html',data=data)

@app.route('/form', methods=['GET', 'POST'])
def Form():
    if request.method == "POST":
        name = request.form.get('product')
        price = request.form.get('price')
        product = Products(name=name,price=price)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('view'))
    return render_template('form.html')

@app.route('/editForm/<int:id>', methods=['GET', 'POST'])
def editForm(id):
    if request.method == "POST":
        name = request.form.get('name')
        price = request.form.get('price')
        product = Products.query.get(id)
        product.name = name
        product.price = price
        db.session.commit()
        return redirect(url_for('view'))
    data = Products.query.filter_by(id=id).first()
    print(data)
    return render_template('edit-form.html',data=data)


