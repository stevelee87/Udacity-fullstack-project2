from flask import Flask, flash
from database_setup import Base, User, Category, Item
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class DAOItem():
    def create(self, title, description, cat_id, user_id):
        new_item = Item(title=title,
                        description=description,
                        cat_id=cat_id,
                        user_id=user_id)
        db.session.add(new_item)
        db.session.commit()
        flash("\"{}\" successfully created!".format(new_item.title))

    def update(self, item_title, new_title, new_description, new_cat_id):
        item_to_be_edited = self.get_item_by_title(item_title)
        item_to_be_edited.title = new_title
        item_to_be_edited.description = new_description
        item_to_be_edited.cat_id = new_cat_id
        db.session.commit()
        flash("The item \"{}\" was successfully updated"
              .format(item_to_be_edited.title))

    def delete(self, item_to_be_deleted):
        deleted_item_title = item_to_be_deleted.title
        db.session.delete(item_to_be_deleted)
        db.session.commit()
        flash("The item \"{}\" was successfully deleted"
              .format(deleted_item_title))

    def get_item_by_title(self, item_title):
        return db.session.query(Item).filter_by(title=item_title).one()

    def get_latest_items(self, quantity):
        latest_items = db.session.query(Item, Category).join(Category)\
                       .order_by(Item.id.desc()).limit(quantity).all()
        return latest_items


class DAOCategory:
    def get_category_items(self, category):
        category_items = db.session.query(Item).join(Category)\
                         .filter_by(name=category).all()
        return category_items

    def get_category_of_item(self, item_title):
        category = db.session.query(Category).join(Item)\
                   .filter_by(title=item_title).first()
        return category

    def get_all_categories(self):
        categories = db.session.query(Category).all()
        return categories


class DAOUser:
    def create(self, login_session):
        new_user = User(name=login_session['username'],
                        email=login_session['email'])
        db.session.add(new_user)
        db.session.commit()
        user = db.session.query(User).filter_by(
               email=login_session['email']).one()
        return user.id

    def get_user_id(self, email):
        try:
            user = db.session.query(User).filter_by(email=email).one()
            return user.id
        except:
            return None

    def is_logged(self, login_session):
        if 'email' in login_session:
            if self.get_user_id(login_session['email']) is not None:
                return True
            else:
                return False
        else:
            return False
