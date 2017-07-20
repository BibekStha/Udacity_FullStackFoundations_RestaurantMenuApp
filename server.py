from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


#Create session for query by binding with engine created with database
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


#Create an instance of Flask 
app = Flask(__name__)



#Display list of restaurants
@app.route('/')
@app.route('/restaurants/')
def restaurants():
	restaurants = session.query(Restaurant).all()
	return render_template('/restaurants.html/', restaurants = restaurants)

#Add new restaurant
@app.route('/restaurants/new/', methods = ['GET', 'POST'])
def newRestaurant():
	if request.method == 'POST':
		newRestaurant = Restaurant(name = request.form['name'])
		session.add(newRestaurant)
		session.commit()
		flash('New restaurant added to database')
		return redirect(url_for('restaurants'))
	else:
		return render_template('/newrestaurant.html')

#Edit existing restaurant
@app.route('/restaurants/<int:restaurant_id>/edit/', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
	restaurantToEdit = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		restaurantToEdit.name = request.form['name']
		session.commit()
		flash('Restaurant successfully edited')
		return redirect(url_for('restaurants'))
	else:
		return render_template('/editrestaurant.html', restaurantToEdit = restaurantToEdit)

#Delete existing restaurant
@app.route('/restaurants/<int:restaurant_id>/delete/', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	restaurantToDelete = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		session.delete(restaurantToDelete)
		session.commit()
		flash('Restaurant successfully deleted')
		return redirect(url_for('restaurants'))
	return render_template('/deleterestaurant.html', restaurantToDelete = restaurantToDelete)




#Display list of menu items of a restaurants
@app.route('/restaurants/<int:restaurant_id>')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()
	return render_template('/restaurantmenu.html', restaurant = restaurant, items = menuItems)

#Add new menu item
@app.route('/restaurants/<int:restaurant_id>/menu/new/', methods = ['GET', 'POST'])
def newMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		if request.form['description']:
			description = request.form['description']
		else:
			description = 'None'
		if request.form['course']:
			course = request.form['course']
		else:
			course = 'None'

		if request.form['price']:
			price = request.form['price']
		else:
			price = 'None'
		newMenuItem = MenuItem(name = request.form['name'], description =description, course = course, price = price, restaurant_id = restaurant.id)
		session.add(newMenuItem)
		session.commit()
		flash('New menu successfully added to the database')
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant.id))
	return render_template('/newmenu.html', restaurant = restaurant)

#Edit menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods = ['GET', 'POST'])
def editMenu(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	itemToEdit = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			itemToEdit.name = request.form['name']
		if request.form['description']:
			itemToEdit.description = request.form['description']
		if request.form['course']:
			itemToEdit.course = request.form['course']
		if request.form['price']:
			itemToEdit.price = request.form['price']
		session.commit()
		flash('Menu successfully edited')
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	return render_template('/editmenu.html', restaurant = restaurant, itemToEdit = itemToEdit)

#Delete menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods = ['GET', 'POST'])
def deleteMenu(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	itemToDelete = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		flash('Menu successfully deleted')
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id, menu_id = menu_id))
	return render_template('/deletemenu.html', restaurant = restaurant, itemToDelete = itemToDelete)

#API for /restaurants
@app.route('/json')
@app.route('/restaurants/json')
def restaurantsJson():
	restaurants = session.query(Restaurant).all()
	return jsonify(Restaurants = [r.serialize for r in restaurants])

#API for /restaurants/<id>/menu
@app.route('/restaurants/<int:restaurant_id>/json')
@app.route('/restaurants/<int:restaurant_id>/menu/json')
def restaurantMenuJson(restaurant_id):
	restaurants = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return jsonify(restaurantMenu = [i.serialize for i in items])

#API for /restaurants/<id>/menu/<id>
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/json')
def menuItemJson(restaurant_id, menu_id):
	menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
	return jsonify(MenuItem = menuItem.serialize)


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 8000)