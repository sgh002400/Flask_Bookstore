from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup_book import BookStore, Base, BookItem

engine = create_engine('mysql+pymysql://root:root@localhost/bookstore')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


bookstore1 = BookStore(name="JK Rowling")

session.add(bookstore1)
session.commit()

bookItem1 = BookItem(name="Harry Potter1", price="$7.50", bookstore=bookstore1)

session.add(bookItem1)
session.commit()


bookItem2 = BookItem(name="Harry Potter2", price="$8.50", bookstore=bookstore1)

session.add(bookItem2)
session.commit()


bookItem3 = BookItem(name="Harry Potter3", price="$9.50", bookstore=bookstore1)

session.add(bookItem3)
session.commit()



bookstore2 = BookStore(name="Shakespeare")

session.add(bookstore2)
session.commit()


bookItem1 = BookItem(name="King Lear", price="$7.50", bookstore=bookstore2)

session.add(bookItem1)
session.commit()


bookItem2 = BookItem(name="Hamlet", price="$8.50", bookstore=bookstore2)

session.add(bookItem2)
session.commit()


bookItem3 = BookItem(name="Macbeth", price="$9.50", bookstore=bookstore2)

session.add(bookItem3)
session.commit()


print ("added book items!")