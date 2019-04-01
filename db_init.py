from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, Item

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create Admin user
Admin = User(id=1, name="Admin", email="Admin@geekcoffee.com")
session.add(Admin)
session.commit()

# Category: Laptop accessories
category1 = Category(id=1, name="Laptop accessories")

session.add(category1)
session.commit()

Item1 = Item(title = "Darth Vader 15 inches cover", 
            description="A nice Darth Vader black finish cover for your 15 inches laptop.", 
            cat_id=1, user_id=1)

session.add(Item1)
session.commit()

Item2 = Item(title = "R2D2 Macbook Pro 13 inches cover", 
            description="Make your Macbook Pro 13 inches prettier with this R2D2 laptop cover.", 
            cat_id=1, user_id=1)

session.add(Item2)
session.commit()

Item3 = Item(title = "Iron Man Macbook Pro 15 inches cover", 
            description= "Bring Tony Stark and his awesome suit with you wherever you go with this cover for Macbook Pro 15 inches.", 
            cat_id=1, user_id=1)

session.add(Item3)
session.commit()

# Category: Souvenirs
category2 = Category(id=2, name="Souvenirs")

session.add(category2)
session.commit()

Item1 = Item(title = "Darth Vader key ring", 
            description="Show off to your friends with the coolest key ring ever.", 
            cat_id=2, user_id=1)

session.add(Item1)
session.commit()

Item2 = Item(title = "Iron man mini figure", 
            description="Do you ever want to have Iron man's suit? How about this mini figure? It is handcrafted by Sebastian Schulmann and it weights 117g.", 
            cat_id=2, user_id=1)

session.add(Item2)
session.commit()

# Category: Car accessories
category3 = Category(id=3, name="Car accessories")

session.add(category3)
session.commit()



# Category: Gadgets
category4 = Category(id=4, name="Gadgets")

session.add(category4)
session.commit()



# Category: Appliances
category5 = Category(id=5, name="Appliances")

session.add(category5)
session.commit()



# Category: Clothes
category6 = Category(id=6, name="Clothes")

session.add(category6)
session.commit()



# Category: Limited edition
category7 = Category(id=7, name="Limited edition")

session.add(category7)
session.commit()


# Category: Others
category8 = Category(id=8, name="Others")

session.add(category8)
session.commit()




print("added Categories and items!")