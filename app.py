#!/usr/bin/env python
from functools import wraps
from flask import Flask, render_template, request, redirect, jsonify,\
    url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, bicycleCatalogItem, Category, User
from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Bicycle Item Inventory Catalog Application"

# Connect to Database and create database session for the app
engine = create_engine('sqlite:///bicyclesItemCatalog.db',
                       connect_args={'check_same_thread': False}
                       )

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Login required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in login_session:
            return redirect(url_for('showLogin'))
        return f(*args, **kwargs)

    return decorated_function


# JSON APIs to show The Bicycle Catalog information

@app.route('/catalog.json')
def showCatalogJSON():
    """Returns JSON of all items in The Bicycle catalog"""
    bicycles = session.query(bicycleCatalogItem).order_by(
        bicycleCatalogItem.id.desc())
    return jsonify(bicycleCatalogItems=[i.serialize for i in bicycles])


# Show cover page
@app.route('/')
def showCover():
    return render_template('cover.html')


# Show home page
@app.route('/catalog')
def showHome():
    if 'username' not in login_session:
        return render_template('cover.html')
    else:
        return render_template('catalogInv_list.html', )


@app.route(
    '/categories/<int:bicyclesCategory_id>/item/'
    '<int:bicyclesCatalogItem_id>/JSON')
def bicycleCatalogItemJSON(bicyclesCategory_id, bicyclesCatalogItem_id):
    """Returns JSON of selected item in The Bicycle Inventory catalog"""
    Catalog_Item = session.query(
        bicycleCatalogItem).filter_by(id=bicyclesCatalogItem_id).one()
    return jsonify(Catalog_Item=Catalog_Item.serialize)


@app.route('/catalog/categories/JSON')
def bicycleCategoriesJSON():
    """Returns JSON of all categories in the Bicycle Inventory catalog"""
    categories = session.query(Category).all()
    return jsonify(Categories=[r.serialize for r in categories])


# CRUD for The Bicycle Inventory categories

@app.route('/')
@app.route('/categories/edit')
def showCatalog():
    """Returns The Bicycle Inventory catalog page with all categories and
        recently added items with edit/delete opt"""
    categories = session.query(Category).all()
    bicycles = session.query(bicycleCatalogItem).order_by(
        bicycleCatalogItem.id.desc())
    quantity = bicycles.count()
    if 'username' not in login_session:
        return render_template(
            'public_catalogInv.html',
            categories=categories, bicycles=bicycles, quantity=quantity)
    else:
        return render_template(
            'catalogInv.html',
            categories=categories, bicycles=bicycles, quantity=quantity)


@app.route('/')
@app.route('/categories/bicycles')
def showBiciCatalog():
    """Returns The Bicycle Inventory catalog page with all categories and
    recently added items"""
    categories = session.query(Category).all()
    bicycles = session.query(bicycleCatalogItem).order_by(
        bicycleCatalogItem.id.desc())
    quantity = bicycles.count()
    if 'username' not in login_session:
        return render_template(
            'public_catalogInv.html',
            categories=categories, bicycles=bicycles, quantity=quantity)
    else:
        return render_template(
            'CatalogInv_Bikes.html',
            categories=categories, bicycles=bicycles, quantity=quantity)


# Create new bicycle categories
@app.route('/categories/new', methods=['GET', 'POST'])
@login_required
def newBicycleCategory():
    """Allows user to create new category into The Bicycle Inventory"""
    if request.method == 'POST':
        print
        login_session
        if 'user_id' not in login_session and 'email' in login_session:
            login_session['user_id'] = getUserID(login_session['email'])

        newBicycleCategory = Category(
         name=request.form['name'],
         user_id=login_session['user_id'])
        if request.form['name'] == '':
            flash('The field cannot be empty.')
            return redirect(url_for('newBicycleCategory'))
            flash('The field cannot be empty.')
            return redirect(url_for('newBicycleCategory'))
        # Check for duplicate categories
        category = session.query(Category). \
            filter_by(name=request.form['name']).first()
        if category is not None:
            flash(
                '%s  already exists in the category, please enter a new '
                'one.' % newBicycleCategory.name)
            return redirect(url_for('newBicycleCategory'))

        session.add(newBicycleCategory)
        session.commit()
        flash('New category %s successfully created!' %
              newBicycleCategory.name,
              'success')
        return redirect(url_for('showCatalog'))

    else:
        return render_template('new_catalogInv_category.html')


# edit The Bicycle Inventory  category
@app.route('/categories/<int:bicyclesCategory_id>/edit/',
           methods=['GET', 'POST'])
@login_required
def editBicycleCategory(bicyclesCategory_id):
    """Allows user to edit an existing category in the app"""
    editedBikeCategory = session.query(
        Category).filter_by(id=bicyclesCategory_id).one()
    if editedBikeCategory.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not " \
               "authorized!')}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedBikeCategory.name = request.form['name']
            flash(
                'Category Successfully Edited %s' % editedBikeCategory.name,
                'success')
            return redirect(url_for('showCatalog'))
    else:
        return render_template(
            'edit_catalogInv_category.html', category=editedBikeCategory)


# Delete  a category from the Bicyle Inventory app
@app.route('/categories/<int:bicyclesCategory_id>/delete/',
           methods=['GET', 'POST'])
@login_required
def deleteBicycleCategory(bicyclesCategory_id):
    """Allows user to delete an existing category the Bicycle Inventory app"""
    categoryToDelete = session.query(
        Category).filter_by(id=bicyclesCategory_id).one()
    if categoryToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not " \
               "authorized!')}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(categoryToDelete)
        flash('%s successfully deleted from the Bicycle Inventory ' %
              categoryToDelete.name,
              'success')
        session.commit()
        return redirect(
            url_for('showCatalog', bicyclesCategory_id=bicyclesCategory_id))
    else:
        return render_template(
            'delete_categoryInv.html', category=categoryToDelete)


#  show Bicycle category items
@app.route('/categories/<int:bicyclesCategory_id>/')
@app.route('/categories/<int:bicyclesCategory_id>/item/')
def showCategoryItems(bicyclesCategory_id):
    """returns bicycles items  in category"""
    category = session.query(Category).filter_by(id=bicyclesCategory_id).one()
    categories = session.query(Category).all()
    creator = getUserInfo(category.user_id)
    bicycles = session.query(
        bicycleCatalogItem).filter_by(
        bicyclesCategory_id=bicyclesCategory_id).order_by(
        bicycleCatalogItem.id.desc())
    quantity = bicycles.count()
    return render_template(
        'catalogInv_menu.html',
        categories=categories,
        category=category,
        bicycles=bicycles,
        quantity=quantity,
        creator=creator)


@app.route('/categories/<int:cat_id>/')
@app.route('/categories/<int:cat_id>/bicycles/')
def showCategoryBicycles(cat_id):
    """returns bicycles items  in category with the edit/delete option"""
    category = session.query(Category).filter_by(id=cat_id).one()
    categories = session.query(Category).all()
    creator = getUserInfo(category.user_id)
    bicycles = session.query(
        bicycleCatalogItem).filter_by(
        bicyclesCategory_id=cat_id).order_by(bicycleCatalogItem.id.desc())
    quantity = bicycles.count()
    return render_template(
        'CatalogInv_Bikes.html',
        #    'catalog_Inv.html',
        categories=categories,
        category=category,
        bicycles=bicycles,
        quantity=quantity,
        creator=creator)


# Select specific item show specific information about that bicycle
@app.route(
    '/categories/<int:bicyclesCategory_id>/item/<int:bicyclesCatalogItem_id>/')
def showCatalogItem(bicyclesCategory_id, bicyclesCatalogItem_id):
    """returns bicycle category item"""
    category = session.query(Category).filter_by(id=bicyclesCategory_id).one()
    item = session.query(
        bicycleCatalogItem).filter_by(id=bicyclesCatalogItem_id).one()
    creator = getUserInfo(category.user_id)
    return render_template(
        'catalogInv_menu_item.html',
        category=category, item=item, creator=creator)


# Create a bicycle item
@app.route('/categories/item/new', methods=['GET', 'POST'])
@login_required
def newBicycleCatalogItem():
    """Create a new bicycle item"""
    categories = session.query(Category).all()
    if request.method == 'POST':
        addNewItem = bicycleCatalogItem(
            name=request.form['name'],
            description=request.form['description'],
            price=request.form['price'],
            upc=request.form['upc'],
            bicyclesCategory_id=request.form['category'],
            user_id=login_session['user_id'])
        session.add(addNewItem)
        session.commit()
        flash("%s was created and added to the Bicycle Catalog Item!" %
              addNewItem.name, 'success')
        return redirect(url_for('showCatalog'))
    else:
        return render_template('new_catalogInv_item.html',
                               categories=categories)


# Update the bicycle category
@app.route(
    '/categories/<int:bicyclesCategory_id>/item/<int:bicyclesCatalogItem_id>'
    '/edit',
    methods=['GET', 'POST'])
@login_required
def editBicycleCatalogItem(bicyclesCategory_id, bicyclesCatalogItem_id):
    """This page will return an updated bicycle catalog item"""
    editedItem = session.query(
        bicycleCatalogItem).filter_by(id=bicyclesCatalogItem_id).one()
    if editedItem.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not " \
               "\authorized!')}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['category']:
            editedItem.bicyclesCategory_id = request.form['category']
        session.add(editedItem)
        if request.form['upc']:
            editedItem.upc = request.form['upc']
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
            session.commit()
        flash("The Bicycle catalog item has been updated!", 'success')
        return redirect(url_for('showCatalog'))
    else:
        categories = session.query(Category).all()
        return render_template(
            'catalogInv_edit_item.html',
            categories=categories,
            item=editedItem)


# Delete a bicycle catalog item
@app.route(
    '/categories/<int:bicyclesCategory_id>/item/<int:bicyclesCatalogItem_id'
    '> /delete',
    methods=['GET', 'POST'])
@login_required
def deleteBicycleCatalogItem(bicyclesCategory_id, bicyclesCatalogItem_id):
    itemToDelete = session.query(
        bicycleCatalogItem).filter_by(id=bicyclesCatalogItem_id).one()
    if itemToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not " \
               "authorized!')}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Bicycle catalog item successfully deleted', 'success')
        return redirect(url_for('showCatalog'))
    else:
        return render_template(
            'delete_catalogInv_item.html', item=itemToDelete)


# Login route
@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(
            string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Connect FB login
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print
    "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=' \
          'fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_' \
          'token=%s' % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.8/me' \
          '?fields=id%2Cname%2Cemail%2Cpicture&access_token=' + access_token

    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session
    # in order to properly logout out the application
    login_session['access_token'] = access_token

    # Get user picture
    login_session['picture'] = data["picture"]["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius:' \
              ' 150px;-webkit-border-radius: 150px;-moz-border-radius: ' \
              '150px;"> '

    flash("Now logged in as %s" % login_session['username'], 'success')
    return output


# disconnect FB login
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
           facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    # return "you have been logged out"
    return render_template(
        # 'cover.html)
        'public_catalogInv_list.html')


# CONNECT - Google login get token
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
                  json.dumps("Token's user ID doesn't match given user ID."),
                  401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print
        "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.to_json()
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if not create new user
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: ' \
              '150px;-webkit-border-radius: 150px;-moz-border-radius: ' \
              '150px;"> '
    flash("you are now logged in as %s" % login_session['username'], 'success')
    print
    "done!"
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # only disconnect a connected user
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-type'] = 'application/json'
        return response
    # execute HTTP GET request to revoke current token
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # reset the user's session
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(
            json.dumps('Successfully disconnected from the Bicycle Inv App.'),
            200)
        response.headers['Content-Type'] = 'application/json'
        return response

    else:
        # token given is invalid
        response = make_response(
            json.dumps(
                'Application failed to revoke the token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# User helper functions
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def createUser(login_session):
    newUser = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    print
    login_session
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            if 'gplus_id' in login_session:
                del login_session['gplus_id']
            if 'credentials' in login_session:
                del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        if 'username' in login_session:
            del login_session['username']
        if 'email' in login_session:
            del login_session['email']
        if 'picture' in login_session:
            del login_session['picture']
        if 'user_id' in login_session:
            del login_session['user_id']
        del login_session['provider']
        flash(
            "You have successfully been logged out the Bicycle Inventory "
            "Catalog.", 'success')
        return redirect(url_for('showHome'))
    else:
        flash("You were not logged into the Bicycle Inventory Catalog",
              'danger')
        return redirect(url_for('showBiciCatalog'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)