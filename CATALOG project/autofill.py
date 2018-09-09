from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Categories, Base, Items ,User
 
engine = create_engine('sqlite:///clm.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()


#data for soccer category
c1 = Categories(user_id=1,name = "Soccer")

session.add(c1)
session.commit()


i1 = Items(user_id=1,name = "Telestar18", description = "The foot ball inspired from FIFA worldcup", categories = c1)

session.add(i1)
session.commit()

i2 = Items(user_id=1,name = "Leg pad", description = "Guard for leg protection.", categories = c1)

session.add(i2)
session.commit()

i3 = Items(user_id=1,name = " Groin guard", description = "Protection for pelvic area.", categories = c1)

session.add(i3)
session.commit()

i4 = Items(user_id=1,name = "MAN UTD. unifrom", description = "Football unifrom inspired from the legendary Manchester united team.", categories = c1)

session.add(i4)
session.commit()





#Menu for Super Stir Fry
c2 = Categories(user_id=1,name = "Cricket")

session.add(c2)
session.commit()


i1 = Items(user_id=1,name = "WCC ball", description = "The original WCC cricket ball.", categories = c2)

session.add(i1)
session.commit()

i2 = Items(user_id=1,name = "Knee pad", description = "Guard for leg protection.", categories = c2)

session.add(i2)
session.commit()

i3 = Items(user_id=1,name = " Groin guard", description = "Protection for pelvic area.", categories = c2)

session.add(i3)
session.commit()

i4 = Items(user_id=1,name = "All stars unifrom", description = "Cricket unifrom inspired from the legendary EA Games all stars team.", categories = c2)

session.add(i4)
session.commit()

i5 = Items(user_id=1,name = "Cricket helmet", description = "Protection for the head.", categories = c2)

session.add(i5)
session.commit()





#Menu for Panda Garden
c3 = Categories(user_id=1,name = "Snow Boarding")

session.add(c3)
session.commit()


i1 = Items(user_id=1,name = "Snow board", description = "Used for skating in snow capped peaks.", categories = c3)

session.add(i1)
session.commit()

i2 = Items(user_id=1,name = "Thermal wear", description = "Used for thermal protection in high altitude areas", categories=c3)
session.add(i2)
session.commit()

