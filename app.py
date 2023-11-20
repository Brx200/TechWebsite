from flask import Flask, render_template, url_for, flash, redirect, request, session
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
import os

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'jpg','jpeg','png','gif'}
UPLOAD_FOLDER = './static/images'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Vicky1023@Localhost:5432/TechWebsite'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(205),nullable=False)
    image1 = db.Column(db.String,nullable=False)
    image2 = db.Column(db.String,nullable=False)
    image3 = db.Column(db.String,nullable=False)
    image4 = db.Column(db.String,nullable=False)
    image5 = db.Column(db.String,nullable=False)
    description = db.Column(db.String,nullable=False)
    specification = db.Column(db.String,nullable=False)
    price = db.Column(db.Numeric(10,2),nullable=False)

class Team(db.Model):
    __tablename__ = "teams"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(205),nullable=False)
    bio = db.Column(db.String,nullable=False)
    description = db.Column(db.String,nullable=False)
    role = db.Column(db.String,nullable=False)
    image = db.Column(db.String,nullable=False)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(205),nullable=False)
    password = db.Column(db.string,nullable=False)
    email = db.column(db.string,nullable=False)

    def get_password(self):
        return self.password

@app.route('/')
def index():
    products = Product.query.all()
    return render_template("index.html",products = products)

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        
        existing_email2 = User.query.filter_by(email)
        if existing_email2:
            password_input = existing_email2.get_password()
            if password == password_input:
                session['email'] = existing_email2
                flash('login successful')
                redirect(url_for('index'))

        else:
            flash("You don't have an account")
            redirect(url_for('signup'))
    return render_template("login.html")

@app.route('/log_out',methods=['POST','GET'])
def log_out():
    redirect (url_for('index.html'))

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        existing_email = User.query.filter_by(email)
        if existing_email:
            flash('You have an account')
            redirect(url_for('login'))
        else:
            new_user = User(
                name=name,
                email=email,
                password=password
            )
            db.session.add(new_user)
            db.session.commit()
            db.session.close()
    return render_template("signup.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/add_product',methods=['POST','GET'])
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        image1 = request.files.get('image1')
        image2 = request.files.get('image2')
        image3 = request.files.get('image3')
        image4 = request.files.get('image4')
        image5 = request.files.get('image5')
        description = request.form.get('description')
        price = request.form.get('price')
        specification = request.form.get('specification')

        new_products = Product(name=name,
                               description=description,
                               price=price,
                               specification=specification)
        
        db.session.add(new_products)
        if image1:
            filename = secure_filename(image1.filename)
            image1.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            new_products.image1 = filename

        if image2:
            filename = secure_filename(image2.filename)
            image2.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            new_products.image2 = filename

        if image3:
            filename = secure_filename(image3.filename)
            image3.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            new_products.image = filename

        if image4:
            filename = secure_filename(image4.filename)
            image4.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            new_products.image4 = filename

        if image5:
            filename = secure_filename(image5.filename)
            image5.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            new_products.image5 = filename

        db.session.commit()
        db.session.close()
        # flash('New product add successfully')
        return redirect(url_for('add_product'))
    return render_template("add_product.html")

@app.route('/add_property')
def add_property():
    return render_template("add_property.html")

@app.route('/add_to_cart')
def add_to_cart():
    pass

@app.route('/product/<int:id>/details')
def product_details(id):
    products = Product.query.get(id)
    return render_template('single.html', products=products)

@app.route('/add_team',methods=['POST','GET'])
def add_team():
    if request.method == 'POST':
        name = request.form.get('name')
        bio = request.form.get('bio')
        description = request.form.get('description')
        role = request.form.get('role')
        image = request.files.get('image')

        new_team = Team(name=name,
                        bio=bio,
                        description=description,
                        role=role,
                        image=image)
        
        db.session.add(new_team)
        db.session.commit()
        db.session.close()
    return render_template("add_team.html")

@app.route('/admin-index')
def admin_index():
    return render_template("admin-index.html")

@app.route('/admin_product')
def admin_product():
    products = Product.query.all()
    return render_template("admin-product.html",products = products)

@app.route('/admin-team')
def admin_team():
    teams = Team.query.all()
    return render_template("admin-team.html",teams = teams)

@app.route('/base')
def base():
    return render_template("base.html")

@app.route('/base2')
def base2():
    return render_template("base2.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/product')
def product():
    return render_template("product.html")

@app.route('/services')
def services():
    return render_template("services.html")

@app.route('/edit_product/<int:id>',methods = ['GET','POST'])
def edit_product(product_id):
    product = Product.query.get(product_id)

    if request.method=='POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.specification = request.form.get('specification')
        product.price = request.form.get('price')
        image1 = request.files.get("image1")
        image2 = request.files.get("image2")
        image3 = request.files.get("image3")
        image4 = request.files.get("image4")
        image5 = request.files.get("image5")
        if image1:
            filename = secure_filename(image1.filename)
            image1.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            product.image1 = filename

        if image2:
            filename = secure_filename(image2.filename)
            image2.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            product.image2 = filename

        if image3:
            filename = secure_filename(image3.filename)
            image3.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            product.image3 = filename

        if image4:
            filename = secure_filename(image4.filename)
            image4.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            product.image4 = filename

        if image5:
            filename = secure_filename(image5.filename)
            image5.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            product.image5 = filename

        db.session.commit()
        return redirect(url_for('edit_product',product_id = product.id))
    return render_template("edit_product.html",product = product)

@app.route('/delete_product/<int:id>',methods = ['GET','DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()
    db.session.close()
    return redirect("admin-product.html")

@app.route('/edit_team/<int:id>',methods = ['GET','POST'])
def edit_team(Team_id):
    team = Team.query.get(Team_id)

    if request.method=='POST':
        team.name = request.form.get('name')
        team.bio = request.form.get('bio')
        team.role = request.form.get('role')
        team.description = request.form.get('description')
        image = request.files.get("image")

        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            product.image = filename

        db.session.commit()
        return redirect(url_for('edit_team',Team_id = team.id))
    return render_template("edit_team.html",team = team)

@app.route('/delete_team/<int:id>',methods = ['GET','DELETE'])
def delete_team(team_id):
    team = Product.query.get(team_id)
    db.session.delete(team)
    db.session.commit()
    db.session.close()
    return redirect("admin-team.html")

if __name__ == "__main__":
    app.run(debug=True)