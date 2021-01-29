import flask
from flask import request, jsonify
import sqlite3
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Stock Control</h1>
<p>A prototype API for stock control.</p>'''


@app.route('/API/resources/items/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('resources/items.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM items;').fetchall()

    return jsonify(all_books)



@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/API/resources/items/post', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('ID')
    name = query_parameters.get('name')
    quantity = query_parameters.get('qty')
    threshold = query_parameters.get('threshold')
    type = query_parameters.get('type')

    query = "SELECT * FROM items WHERE"
    to_filter = []

    if id:
        query += ' ID=? AND'
        to_filter.append(id)
    if name:
        query += ' name=? AND'
        to_filter.append(name)
    if quantity:
        query += ' qty=? AND'
        to_filter.append(quantity)
    if threshold:
        query += ' threshold=? AND'
        to_filter.append(threshold)
    if type:
        query += ' type=? AND'
        to_filter.append(type)

    if not (id or name or type or threshold or quantity):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('resources/items.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)


@app.route('/API/resources/items/post', methods=['POST'])
def api_post():

    data = request.get_json()
    #data = json.loads(myJSON)
    print(data)
    
    mydata = (data['name'],data['quantity'],data['threshold'],data['type']);
    
    query = '''INSERT INTO items(name,qty,threshold,type) VALUES(?,?,?,?)'''

    conn = sqlite3.connect('resources/items.db')
    cur = conn.cursor()

    cur.execute(query,mydata)

    conn.commit()

    return ''

@app.route('/API/resources/items/delete', methods=['DELETE'])
def api_delete():

    data = request.get_json()

    mydata = data['ID']

    query = "DELETE FROM items WHERE ID ="

    conn = sqlite3.connect('resources/items.db')
    cur = conn.cursor()

    cur.execute(query + str(mydata))

    conn.commit()

    return 'Deleted'


app.run()