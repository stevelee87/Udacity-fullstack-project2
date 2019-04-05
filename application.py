from flask import Flask, url_for, render_template, redirect, request, flash, \
                jsonify, session as login_session, make_response
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import random
import string
import json
import requests
import httplib2
import DAO

app = DAO.app

dao_item = DAO.DAOItem()
dao_user = DAO.DAOUser()
dao_category = DAO.DAOCategory()

CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']


@app.route('/')
def home():
    categories = dao_category.get_all_categories()
    latest_items = dao_item.get_latest_items(10)
    return render_template('home.html',
                           categories=categories,
                           latest_items=latest_items,
                           login_session=login_session,
                           is_logged=dao_user.is_logged(login_session))


@app.route('/catalog/<string:category_name>/items')
def show_items(category_name):
    categories = dao_category.get_all_categories()
    category_items = dao_category.get_category_items(category_name)
    items_quantity = len(category_items)
    return render_template('showitem.html',
                           categories=categories,
                           category_name=category_name,
                           category_items=category_items,
                           items_quantity=items_quantity,
                           login_session=login_session,
                           is_logged=dao_user.is_logged(login_session))


@app.route('/catalog/<string:category_name>/<string:item_title>')
def show_item_description(category_name, item_title):
    categories = dao_category.get_all_categories()
    item = dao_item.get_item_by_title(item_title)
    description = item.description
    authorized = get_authorization(item_title, login_session)
    return render_template('showdescription.html',
                           categories=categories,
                           category_name=category_name,
                           item_title=item_title,
                           description=description,
                           login_session=login_session,
                           is_logged=dao_user.is_logged(login_session),
                           authorized=authorized)


@app.route('/catalog/<string:item_title>/edit', methods=['GET', 'POST'])
def edit_item(item_title):
    if dao_user.is_logged(login_session) is False:
        return alert()

    if request.method == 'POST':
        new_title = request.form['new_title']
        dao_item.update(item_title,
                        new_title,
                        request.form['new_description'],
                        request.form['new_category'])
        category = dao_category.get_category_of_item(new_title)
        return redirect(url_for('show_item_description',
                                category_name=category.name,
                                item_title=new_title))
    else:
        item_to_be_edited = dao_item.get_item_by_title(item_title)
        categories = dao_category.get_all_categories()
        category = dao_category.get_category_of_item(item_title)
        return render_template('edititem.html',
                               item=item_to_be_edited,
                               category_name=category.name,
                               categories=categories,
                               login_session=login_session,
                               is_logged=dao_user.is_logged(login_session))


@app.route('/catalog/<string:item_title>/delete', methods=['GET', 'POST'])
def delete_item(item_title):
    if dao_user.is_logged(login_session) is False:
        return alert()

    item_to_be_deleted = dao_item.get_item_by_title(item_title)
    category = dao_category.get_category_of_item(item_title)
    if request.method == 'POST':
        dao_item.delete(item_to_be_deleted)
        return redirect(url_for('show_items', category_name=category.name))
    else:
        categories = dao_category.get_all_categories()
        return render_template('deleteitem.html',
                               item=item_to_be_deleted,
                               category_name=category.name,
                               categories=categories,
                               login_session=login_session,
                               is_logged=dao_user.is_logged(login_session))


@app.route('/catalog/additem', methods=['GET', 'POST'])
def add_item():
    if dao_user.is_logged(login_session) is False:
        return alert()

    if request.method == 'POST':
        dao_item.create(request.form['new_title'],
                        request.form['new_description'],
                        request.form['new_category'],
                        dao_user.get_user_id(login_session['email']))
        return redirect(url_for('home'))
    else:
        category_name = None
        categories = dao_category.get_all_categories()
        return render_template('additem.html',
                               categories=categories,
                               category_name=category_name,
                               login_session=login_session,
                               is_logged=dao_user.is_logged(login_session))


@app.route('/catalog/<string:category_name>/additem', methods=['GET', 'POST'])
def add_item_to_specific_category(category_name):
    if dao_user.is_logged(login_session) is False:
        return alert()

    if request.method == 'POST':
        dao_item.create(request.form['new_title'],
                        request.form['new_description'],
                        request.form['new_category'],
                        dao_user.get_user_id(login_session['email']))
        return redirect(url_for('show_items', category_name=category_name))
    else:
        categories = dao_category.get_all_categories()
        return render_template('additem.html',
                               categories=categories,
                               category_name=category_name,
                               login_session=login_session,
                               is_logged=dao_user.is_logged(login_session))


@app.route('/login', methods=['GET', 'POST'])
def auth_login():
    state = ''.join(random.choice(string.ascii_uppercase +
                    string.digits) for x in range(32))
    login_session['state'] = state
    if request.method == 'POST':
        pass
    else:
        return render_template('login.html', STATE=state)


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
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}'
           .format(access_token))
    http_obj = httplib2.Http()
    result = json.loads(http_obj.request(url, 'GET')[1])
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
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
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
    login_session['email'] = data['email']

    # Create or authenticate user
    if dao_user.get_user_id(login_session['email']) is None:
        user_id = dao_user.create(login_session)
    else:
        user_id = dao_user.get_user_id(login_session['email'])

    login_session['user_id'] = user_id

    output = ''
    output += 'Welcome, '
    output += login_session['username']
    output += '!'
    flash("you are now logged in as {}".format(login_session['username']))
    print("done!")
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is {}'.format(access_token))
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token={}'\
          .format(login_session['access_token'])
    http_obj = httplib2.Http()
    result = http_obj.request(url, 'GET')[0]
    print('result is ')
    print(result)
    del login_session['access_token']
    del login_session['gplus_id']
    del login_session['username']
    del login_session['email']
    del login_session['user_id']
    del login_session['state']
    flash("Logged out successfully")
    return redirect(url_for('home'))


@app.route('/catalog.json')
def get_json_all_categories_all_items():
    if dao_user.is_logged(login_session) is False:
        return alert()

    categories = dao_category.get_all_categories()
    return jsonify(Category=[category.serialize for category in categories])


@app.route('/catalog/<string:category_name>.json')
def get_json_from_specific_category(category_name):
    if dao_user.is_logged(login_session) is False:
        return alert()

    categories = dao_category.get_category_items(category_name)
    return jsonify(Category=[category.serialize for category in categories])


@app.route('/catalog/<string:category_name>/<item_title>.json')
def get_json_from_specific_item(category_name, item_title):
    if dao_user.is_logged(login_session) is False:
        return alert()

    item = dao_item.get_item_by_title(item_title)
    return jsonify(Item=[item.serialize])


def get_authorization(item_title, login_session):
    item = dao_item.get_item_by_title(item_title)
    try:
        if item.user_id == dao_user.get_user_id(login_session['email']):
            return True
        else:
            return False
    except:
        return False


def alert():
    alert_msg = "<script> \
        function myFunction(){ \
        alert('You are not logged in!'); \
        setTimeout(function() {window.location.href = '/';}, 200);} \
        </script><body onload='myFunction()''>"
    return alert_msg


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
