# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, bicycleCatalogItem, Category, User

# Create database and create a shortcut for easier to update database
engine = create_engine('sqlite:///bicyclesItemCatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create dummy user
User1 = User(name="I am a Bicycle", email="bi.cycle@gmail.com",
             picture="/static/fake_user.jpg")

session.add(User1)
session.commit()

# Create category of Mountain Bike
category1 = Category(user_id=1, name="Mountain Bike")
session.add(category1)
session.commit()

# Create category of Hybrid/Comfort Bike
category2 = Category(user_id=1, name="Hybrid/Comfort Bike")
session.add(category2)
session.commit()

# Create category of Road Bike
category3 = Category(user_id=1, name="Road Bike")
session.add(category3)
session.commit()

# Add Items into categories
bicycleCatalogItem1 = bicycleCatalogItem(
    upc='1111',
    name='Mountain Bike',
    description='These bikes have flat handlebars and rugged frames and '
                '\components. Mountain bikes often have\
                 suspension to help any cyclist navigate rocky mountain '
                'trails.',
    price='499.99',

    category=category1,
    user_id=1
)

session.add(bicycleCatalogItem1)
session.commit()

bicycleCatalogItem2 = bicycleCatalogItem(
    upc='2222',
    name='Hybrid/Comfort Bike',
    description='Hybrids and Sport Comfort Bikes share the same comfort\ '
                'features but are distinguished by wheel size.',
    price='599.99',

    category=category2,
    user_id=1
)

session.add(bicycleCatalogItem2)
session.commit()

bicycleCatalogItem3 = bicycleCatalogItem(
    upc='3333',
    name='Road Bike',
    description='Road bikes can be identified by their skinny tires and\ '
                'down-turned or drop handlebars. These bikes\
                rule the road due to their extreme efficiency and speed.',
    price='699.99',

    category=category3,
    user_id=1
)

session.add(bicycleCatalogItem3)
session.commit()

print
"added category items to the Bicycle Inventory!"
