import json, requests
from flask_login import LoginManager, current_user, login_user, login_required

from flask import Flask, request, render_template, redirect, flash, url_for
from sqlalchemy.exc import IntegrityError

from models import db, User, List
from forms import SignUp, LogIn


''' Begin boilerplate code '''

''' Begin Flask Login Functions '''
login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

''' End Flask Login Functions '''


def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config['SECRET_KEY'] = "MYSECRET"
  app.config['TEMPLATES_AUTO_RELOAD'] = True
  login_manager.init_app(app)
  db.init_app(app)
  return app

app = create_app()

app.app_context().push()
db.create_all(app=app)
''' End Boilerplate Code '''

@app.route('/', methods=['GET'])
def index():
  return render_template('homepage.html')

@app.route('/about', methods=['GET'])
def about():
  return render_template('about.html')
  
@app.route('/login', methods=['GET'])
def login():
  form = LogIn()
  return render_template('login.html', form=form)

#user submits the login form
@app.route('/login', methods=['POST'])
def loginAction():
  form = LogIn()
  if form.validate_on_submit(): # respond to form submission
      data = request.form
      user = User.query.filter_by(username = data['username']).first()
      if user and user.check_password(data['password']): # check credentials
        flash('Logged in successfully.') # send message to next page
        login_user(user) # login the user
        return redirect(url_for('index')) # redirect to main page if login successful
  flash('Invalid credentials')
  return redirect(url_for('login'))
  
@app.route('/signup', methods=['GET'])
def signup():
  form = SignUp() # create form object
  return render_template('signup.html', form=form) # pass form object to template


@app.route('/signup', methods=['POST'])
def signupAction():
  form = SignUp() # create form object
  if form.validate_on_submit():
    data = request.form # get data from form submission
    newuser = User(username=data['username'], email=data['email']) # create user object
    newuser.set_password(data['password']) # set password
    newuser.check_password(data['password'])
    db.session.add(newuser) # save new user
    db.session.commit()
    flash('Account Created!')# send message
    return redirect(url_for('login'))# redirect to login page
  flash('Error invalid input!')
  return redirect(url_for('signup')) 


@app.route('/list', methods=['GET'])
@login_required
def get_list():
  lists = lists = List.query.filter_by(userid=current_user.id).all()
  return render_template('shoppinglist.html', lists=lists)
  
@app.route('/createList', methods=['POST'])
@login_required
def create_list():
  data = request.form
  list = List(text=data['text'], userid=current_user.id, done=False)
  db.session.add(list)
  db.session.commit()
  flash('Created')
  return redirect(url_for('get_list'))

@app.route('/toggle/<id>', methods=['POST'])
@login_required
def toggle(id):
  done = request.form.get('done') # either 'on' or 'None'
  list = List.query.filter_by(userid=current_user.id, id=id).first()
  if list == None:
    flash('Invalid id or unauthorized') 
  list.done = True if done == 'on' else False
  flash('Done!') if list.done else flash ('Not Done!')
  db.session.add(list)
  db.session.commit()
  return redirect(url_for('get_list'))

@app.route('/editList/<id>', methods=["GET"])
@login_required
def edit_list(id):
  list = List.query.filter_by(id=id, userid=current_user.id).first()
  if list:
    return render_template('edit.html', id=id)
  else:
    flash('Todo not found or unauthorized')
  return redirect(url_for('get_list'))


@app.route('/deleteList/<id>', methods=["GET"])
@login_required
def delete_list(id):
  list = List.query.filter_by(userid=current_user.id, id=id).first()
  if list == None:
    flash ('Invalid id or unauthorized')
  db.session.delete(list) # delete the object
  db.session.commit()
  flash ('Deleted!')
  return redirect(url_for('get_list'))

@app.route('/editList/<id>', methods=["POST"])
@login_required
def edit_action(id):
  list = List.query.filter_by(id=id, userid=current_user.id).first()
  data = request.form
  if list:
    list.text = data['text']
    db.session.add(list)
    db.session.commit()
    flash('List Updated')
    redirect(url_for('get_list'))
  else :
    flash('List not found or unauthorized')
  return redirect(url_for('get_list'))  
''''
@app.route('/recipes', methods=['GET'])
def get_recipes():
  return render_template('recipes.html')
'''
@app.route('/recipes', methods=['GET'])
def get_recipes():
  recipes = []
  main_ingredient = request.args.get('search')
  
  url = f'https://www.themealdb.com/api/json/v1/1/filter.php?i={main_ingredient}'

  meals = requests.request("GET", url).json()

  for meal in meals['meals']:

    meal_id = meal['idMeal']
  
    recipe_url = f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}'

    recipe = requests.request("GET", recipe_url).json()

    recipes.append(recipe['meals'][0])

  print(recipes)
  return render_template('recipes.html', recipes = recipes)

app.run(host='0.0.0.0', port=8080, debug=True)