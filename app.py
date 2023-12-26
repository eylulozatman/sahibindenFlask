
from flask import Flask, request, redirect, url_for, flash,json
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from models import db, Category , Advert
 
app = Flask(__name__)
app.debug = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///advertapp.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
from models import db

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/hello')
def check():
	return 'Flask is working'

@app.route('/add_category/<name>', methods=['POST']) #kategori ekle
def add_category(name):
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    
    return f'Category {name} added successfully'

@app.route('/addAdvert', methods=['POST'])  #yeni ilan ekle
def addAdvert():
    data = request.json
    description = data.get('description')
    price = data.get('price')
    city = data.get('city')
    image = data.get('image')
    category_id = data.get('category_id')

    advert = Advert(
        description=description,
        price=price,
        city=city,
        image=image,
        category_id=category_id
    )

    db.session.add(advert)
    db.session.commit()

    return f'Advert added successfully'

@app.route('/updateAdvert', methods=['PUT'])
def updateAdvert():

    data = request.json  
    advert_id = data.get('id')
    advert = Advert.query.filter_by(id=advert_id).first() 

    if 'description' in data:
        advert.description = data.get('description')
    if 'price' in data:
        advert.price = data.get('price')
    if 'city' in data:
        advert.city = data.get('city')
    if 'image' in data:
        advert.image = data.get('image')

    db.session.commit() 
    return f'Advert with ID {advert_id} updated successfully'

@app.route('/deleteAdvert', methods=['DELETE'])
def deleteAdvert(advert_id):
    advert_id = request.args.get('advert_id')
    advert = Advert.query.get_or_404(advert_id)  
    db.session.delete(advert)
    db.session.commit()
    return f'Advert with ID {advert_id} deleted successfully'




@app.route("/getCategories")
def getCategories():
    categories = Category.query.all() 
    category_list = [] 

   
    for category in categories:
        category_list.append({'id': category.id, 'name': category.name})

    return {'categories': category_list}  

def get_categories_count(adverts):
    categories = {}
    for category in Category.query.all():
        count_by_category = sum(1 for advert in adverts if advert.category_id == category.id)
        if count_by_category > 0:
             categories[category.name] = count_by_category
    return categories

@app.route('/allAdvert',methods=['GET'])
def getAllAdvert():
    all_adverts = Advert.query.all()
    adverts_list = []

    for advert in all_adverts:
        adverts_list.append({
            'id': advert.id,
            'description': advert.description,
            'price': advert.price,
            'city': advert.city,
            'image': advert.image,
            'category_id': advert.category_id
        })

    return (adverts_list)
    
  
@app.route('/', methods=['GET'])
def getAdverts():
    adverts = Advert.query.all()  # Tüm ilanları veritabanından çekin
    advert_list = []  

    categories = get_categories_count(adverts)

    for advert in adverts:
        advert_data = {
            'id': advert.id,
            'description': advert.description,
            'price': advert.price,
            'city': advert.city,
            'image': advert.image,
            'category_id': advert.category_id
        }
        advert_list.append(advert_data)

    return render_template('homepage.html', adverts=adverts,categories=categories)

def get_adverts(query=None):

    adverts = Advert.query.filter((Advert.description.contains(query)) | (Advert.city.contains(query))).all()
    return adverts


@app.route('/search')
def search():
    query = request.args.get('query')  # Arama sorgusunu al
    adverts = get_adverts(query)  # Arama sorgusuna göre ilanları getir
    categories = get_categories_count(adverts)  # Filtrelenmiş ilanların kategorilere göre sayılarını getir
    return render_template('searchPage.html', adverts=adverts, categories=categories)

@app.route('/byCategory')
def getAdByCategory():

    category_name = request.args.get('category')
    category = Category.query.filter_by(name=category_name).first()

    adverts = Advert.query.filter(Advert.category == category).all()
    categoryAndCount = get_categories_count(adverts) 
    return render_template('searchPage.html', adverts=adverts, categories=categoryAndCount)

@app.route('/details')
def getDetails():

    advert_id = request.args.get('advertId')
    advert = Advert.query.filter_by(id=advert_id).first()
    return render_template('details.html', advert=advert)



@app.route("/favicon.ico")
def favicon():
    return url_for('static', filename='data:,')


if __name__ == '__main__':
    
    app.run()

  