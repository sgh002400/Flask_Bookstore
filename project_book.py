from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup_book import Base, BookStore, BookItem

app = Flask(__name__)

engine = create_engine('mysql+pymysql://root:root@localhost/bookstore')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/bookstores/<int:bookstore_id>/booklist/JSON')
def bookListJSON(bookstore_id):
    bookstore = session.query(BookStore).filter_by(id=bookstore_id).one()
    items = session.query(BookItem).filter_by(
        bookstore_id=bookstore_id).all()
    return jsonify(BookItems=[i.serialize for i in items])



@app.route('/')
@app.route('/bookstores/<int:bookstore_id>/booklist')
def bookList(bookstore_id=None):
    if bookstore_id == None:
        bookstore_id = 1
    bookstore = session.query(BookStore).filter_by(id=bookstore_id).one()
    items = session.query(BookItem).filter_by(bookstore_id=bookstore_id)
    return render_template(
        'booklist.html', bookstore=bookstore, items=items, bookstore_id=bookstore_id)


@app.route('/bookstores/<int:bookstore_id>/new', methods=['GET', 'POST'])
def newBookItem(bookstore_id):

    if request.method == 'POST':
        newItem = BookItem(name=request.form['name'], price=request.form['price'], bookstore_id=bookstore_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('bookList', bookstore_id=bookstore_id))
    else:
        return render_template('newbook.html', bookstore_id=bookstore_id)


@app.route('/bookstores/<int:bookstore_id>/<int:book_id>/edit',
            methods=['GET', 'POST'])
def editBookItem(bookstore_id, book_id):
    editedItem = session.query(BookItem).filter_by(id=book_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['price']:
            editedItem.price = request.form['price']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('bookList', bookstore_id=bookstore_id))
    else:

        return render_template(
            'editbook.html', bookstore_id=bookstore_id, book_id=book_id, item=editedItem)


@app.route('/bookstores/<int:bookstore_id>/<int:book_id>/delete',
            methods=['GET', 'POST'])
def deleteBookItem(bookstore_id, book_id):
    itemToDelete = session.query(BookItem).filter_by(id=book_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('bookList', bookstore_id=bookstore_id))
    else:
        return render_template('deletebook.html', item=itemToDelete)


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
