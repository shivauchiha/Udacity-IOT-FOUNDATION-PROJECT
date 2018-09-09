#import from flask and sql alchemy
from flask import (Flask , render_template, request, 
redirect, url_for ,
flash, jsonify)
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

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base , Categories,Items,User 

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']


engine = create_engine('sqlite:///clm.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html',STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    #gathers data from google sign-in variable.
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
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    #if new user create a user entry
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id


    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;'\
                           'border-radius: 150px;-webkit-border-radius: 150px;'\
                           '-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

#USER INFO QUERY FUNCTIONS
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

#main page list all categories
@app.route('/')
@app.route('/catalog/')
def listcategories():
    session = DBSession()
    categories = session.query(Categories).all()

    session.close()
    return render_template('categories.html',
                            categories=categories,
                            login_session=login_session)
#main page jason function
@app.route('/catalog/JSON')
def listcategoriesJSON():
    session = DBSession()
    categories = session.query(Categories).all()
    session.close()
    return jsonify(Categories=[i.serialize for i in categories])


#add new category
@app.route('/catalog/new/', methods=['GET','POST'])
def newcategories():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        session = DBSession()
        ca = Categories(name=request.form['name'],user_id=login_session['user_id'])
        session.add(ca)
        session.commit()
        session.close()
        flash("new  category created !")
        return redirect(url_for('listcategories'))
    else:
        return render_template('categoriesnew.html')

#delete new category
@app.route('/catalog/<string:name>/delete/', methods=['GET','POST'])
def deletecategories(name):
    if 'username' not in login_session:
        return redirect('/login')
    session = DBSession()   
    da = session.query(Categories).filter_by(name=name).one_or_none()
    if da.user_id != login_session['user_id']:
        flash("Warning !! Unauthorised operation")
        return redirect('/catalog')
    if request.method == 'POST':
        session.delete(da)
        session.commit()
        session.close()
        flash("category deleted from database !!")
        return redirect(url_for('listcategories'))
    else:
        return render_template('categoriesdelete.html', item=da)

#list all the items in the category
@app.route('/catalog/<string:categories_name>/')
def categoriesitems(categories_name):
    session = DBSession()
    categories = session.query(Categories).filter_by(name = categories_name).one_or_none()
    items = session.query(Items).filter_by(categories_id = categories.id)
    session.close()
    return render_template('item.html', categories=categories ,
                            items =items,login_session=login_session)
#json object for category items
@app.route('/catalog/<string:categories_name>/list/JSON')
def categoriesitemsJSON(categories_name):
    session = DBSession()
    categories = session.query(Categories).filter_by(name = categories_name).one_or_none()
    items = session.query(Items).filter_by(
        categories_id=categories.id).all()
    session.close()
    return jsonify(Items=[i.serialize for i in items])



#adding item to a category
@app.route('/catalog/<string:categories_name>/new/', methods=['GET','POST'])
def newItems(categories_name):
     if 'username' not in login_session:
        return redirect('/login')
     if request.method == 'POST':
        session = DBSession()
        category = session.query(Categories).filter_by(name = categories_name).one_or_none()
        newItem = (Items(name=request.form['name'],
                   description=request.form['description'], categories_id=category.id,user_id=login_session['user_id']))
        session.add(newItem)
        session.commit()
        session.close()
        flash("new item under this category created !")
        return redirect(url_for('categoriesitems', categories_name=categories_name))
     else:
        return render_template('newitem.html', categories_name=categories_name)

# editing item of a category


@app.route('/catalog/<string:categories_name>/<string:menu_name>/edit/', methods=['GET','POST'])
def editItems(categories_name, menu_name):
    if 'username' not in login_session:
        return redirect('/login')
    session = DBSession()
    category = session.query(Categories).filter_by(name = categories_name).one_or_none()
    item = session.query(Items).filter_by(name = menu_name).one()
    editedItem = session.query(Items).filter_by(id=item.id).one()
   
    if editedItem.user_id != login_session['user_id']:
        flash("Warning !! Unauthorised operation")
        return redirect('/catalog')

    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        
        flash("Update added to the database !!")
        return redirect(url_for('categoriesitems', categories_name=category.name))
    else:
        
        return render_template('edititem.html', categories_name = categories_name,
                                menu_name=menu_name, item=editedItem)


# Task 3: deleting an item from category


@app.route('/catalog/<string:categories_name>/<string:menu_name>/delete/', methods=['GET','POST'])
def deleteItems(categories_name, menu_name):
    if 'username' not in login_session:
        return redirect('/login')
    session = DBSession()
    item = session.query(Items).filter_by(name = menu_name).one_or_none()
    itemToDelete = session.query(Items).filter_by(id=item.id).one_or_none()

    if itemToDelete.user_id != login_session['user_id']:
        flash("Warning !! Unauthorised operation")
        return redirect('/catalog')

    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        session.close()
        flash("Item deleted from database !!")
        return redirect(url_for('categoriesitems', categories_name=categories_name))
    else:
        return render_template('deleteitem.html', item=itemToDelete,
                                categories_name = categories_name)




#basic server initialisation runs @localhost:8000


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host ='0.0.0.0', port = 8000)