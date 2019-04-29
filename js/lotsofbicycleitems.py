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
             picture= "/static/fake_user.jpg")

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

# # Create category of BMX/Trick Bike
# category4 = Category(user_id=1, name="BMX/Trick Bike")
# session.add(category4)
# session.commit()
# # Create category of Commuting Bike
# category5 = Category(user_id=1, name="Commuting Bike")
# session.add(category5)
# session.commit()
#
#
# # Create category of Cyclocross Bike
# category6 = Category(user_id=1, name="Cyclocross Bike")
# session.add(category6)
# session.commit()
#
# # Create category of Track Bike/Fixed Gea
# category7 = Category(user_id=1, name="Track Bike/Fixed Gea")
# session.add(category7)
# session.commit()

# Add Items into categories
bicycleCatalogItem1 = bicycleCatalogItem(
    upc='1111',
    name='Mountain Bike',
    description='These bikes have flat handlebars and rugged frames and '
                '\components. Mountain bikes often have\
                 suspension to help any cyclist navigate rocky mountain '
                'trails.',
    price = '499.99',

    category=category1,
    user_id =1
)

session.add(bicycleCatalogItem1)
session.commit()

bicycleCatalogItem2 = bicycleCatalogItem(
    upc='2222',
    name='Hybrid/Comfort Bike',
    description='Hybrids and Sport Comfort Bikes share the same comfort\ '
                'features but are distinguished by wheel size.',
    price = '599.99',

    category=category2,
    user_id =1
)

session.add(bicycleCatalogItem2)
session.commit()

bicycleCatalogItem3 = bicycleCatalogItem(
    upc='3333',
    name='Road Bike',
    description='Road bikes can be identified by their skinny tires and\ '
                'down-turned or drop handlebars. These bikes\
                rule the road due to their extreme efficiency and speed.',
    price = '699.99',

    category=category3,
    user_id =1
)

session.add(bicycleCatalogItem3)
session.commit()


# bicycleCatalogItem4 = bicycleCatalogItem(
#     upc='4444',
#     name='BMX/Trick Bike',
#     description='BMX stands for Bicycle Motor Cross because these single-speed bikes are raced around a short dirt\
#                  track similar to the motor sport.  Frequently, the term BMX is used to describe any single-speed \
#                  bike with a 20 inches wheel.',
#     price = '799.99',
#
#     category=category4,
#     user_id =1
# )
# session.add(bicycleCatalogItem4)
# session.commit()
#
# bicycleCatalogItem5 = bicycleCatalogItem(
#     upc='5555',
#     name='Commuting Bike',
#     description='Simply put, a commuting bike is any bicycle used as general transportation, regardless of the style.\
#                  Commuting bikes generally have practical amenities such as lights, rear racks, bags, locks and \
#                  fenders.',
#     price = '899.99',
#
#     category=category5,
#     user_id =1
# )
#
# session.add(bicycleCatalogItem5)
# session.commit()
#
# bicycleCatalogItem6 = bicycleCatalogItem(
#     upc='6666',
#     name='Cyclocross Bike',
#     description='A cyclocross bike has road bike style drop handlebars but with wider knobby tires. These bikes are\
#                 designed to be raced around a dirt trail where obstacles have been placed at various intervals.',
#     price = '999.99',
#
#     category=category6,
#     user_id =1
# )
#
# session.add(bicycleCatalogItem6)
# session.commit()
#
# bicycleCatalogItem7 = bicycleCatalogItem(
#     upc='7777',
#     name='Track Bike/Fixed Gear',
#     description='A track bike is a road bike with a single gear that does not freewheel or coast.This means the cyclist\
#                  cannot coast on this style of bike. In fact, true track bikes do not even have brakes so the athlete\
#                   must use their leg strength to stop the cranks from turning, which stops the motion of the bike.',
#     price = '1199.99',
#
#     category=category7,
#     user_id =1
# )
#
# session.add(bicycleCatalogItem7)
# session.commit()


print "added category items to the Bicycle Inventory!"