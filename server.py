from flask import Flask, abort, request, jsonify
from flask_cors import CORS, cross_origin
import json
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Universe@7712",
    database="frappetest",
)
cursor = db.cursor()
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/getProducts', methods=['GET'], endpoint='getProducts')
def getProducts():
    cursor.execute("SELECT * FROM Product")
    res = cursor.fetchall()
    db.commit()
    response = []
    for product in res:
        response.append(
            {"id": product[0], "name": product[1], "description": product[2]})
    return jsonify(response)


@app.route('/addProduct', methods=['POST'], endpoint='addProduct')
def addProduct():
    req = request.get_json()
    cursor.execute("INSERT INTO Product(pName,pDescription) VALUES(%s,%s)",
                   (req["name"], req["description"]))
    db.commit()
    return getProducts()


@app.route('/editProduct', methods=['POST'], endpoint="editProduct")
def editProduct():
    req = request.get_json()
    print(req)
    cursor.execute("UPDATE Product SET pName=%s, pDescription=%s where id=%s",
                   (req["name"], req["description"], req["id"]))
    db.commit()
    return getProducts()


@app.route('/delProduct', methods=['POST'], endpoint='delProduct')
def delProduct():
    req = request.get_json()
    cursor.execute("DELETE FROM Product WHERE id = %s", (req["id"],))
    db.commit()
    return getProducts()


@app.route('/getLocations', methods=['GET'], endpoint='getLocations')
def getLocations():
    cursor.execute("SELECT * FROM Location")
    res = cursor.fetchall()
    db.commit()
    response = []
    for location in res:
        response.append(
            {"id": location[0], "name": location[1]})
    return jsonify(response)


@app.route('/addLocation', methods=['POST'], endpoint='addLocation')
def addLocation():
    req = request.get_json()
    cursor.execute("INSERT INTO Location(name) VALUES(%s)",
                   (req["name"], ))
    db.commit()
    return getLocations()


@app.route('/editLocation', methods=['POST'], endpoint='editLocation')
def editLocation():
    req = request.get_json()
    cursor.execute("UPDATE Location SET name = %s WHERE id = %s",
                   (req["name"], req["id"]))
    db.commit()
    return getLocations()


@app.route('/delLocation', methods=['POST'], endpoint='delLocation')
def delLocation():
    req = request.get_json()
    cursor.execute("DELETE FROM Location WHERE id = %s", (req["id"],))
    db.commit()
    return getLocations()


@app.route('/movements/getProducts', methods=['POST'], endpoint='movGetProducts')
def movGetProducts(location=-1):
    requestType = location
    if location == -1:
        req = request.get_json()
        print(req)
        location = req['location']
    cursor.execute("SELECT p.pName, p.pDescription, pmo.product_id, (SELECT SUM(pmi.qty) FROM productmovement AS pmi WHERE pmo.to_location=pmi.to_location AND pmi.product_id = pmo.product_id) AS incoming , (SELECT SUM(pmi.qty) FROM productmovement AS pmi WHERE pmo.to_location=pmi.from_location AND pmi.product_id = pmo.product_id) AS outgoing FROM productmovement AS pmo, product AS p WHERE pmo.product_id = p.id AND pmo.to_location=%s GROUP BY pmo.to_location, pmo.product_id ORDER BY NULL", (location,))
    res = cursor.fetchall()
    db.commit()
    response = []
    print(res)
    for mov in res:
        response.append({"pid": mov[2], "name": mov[0], "description": mov[1], "quantity": str(
            max(mov[3]-mov[4], 0) if mov[4] != None else mov[3])})
    if requestType == -1:
        return jsonify(response)
    else:
        return response


@app.route('/movements/importProduct', methods=['POST'], endpoint='moveProduct')
@app.route('/movements/exportProduct', methods=['POST'], endpoint='moveProduct')
@app.route('/movements/moveProduct', methods=['POST'], endpoint='moveProduct')
def moveProduct():
    req = request.get_json()
    print(req)
    data = (req["product_id"], req["quantity"])
    values = "product_id,qty"
    inputs = "%s,%s"
    location = req["to_location"] if "to_location" in req else req["from_location"]
    if(req["type"] == "import"):
        values += ",to_location"
        inputs += ",%s"
        data = data+(req["to_location"],)
    else:
        if(checkQuantity(req["from_location"],
                         req["product_id"], req["quantity"])):
            if(req["type"] == "export"):
                values += ",from_location"
                inputs += ",%s"
                data = data+(req["from_location"],)
            else:
                values += ",to_location,from_location"
                inputs += ",%s,%s"
                data = data+(req["to_location"], req["from_location"])
        else:
            return abort(403)
    query = "INSERT INTO ProductMovement({fields}) VALUES({inputFields})".format(
        fields=values, inputFields=inputs)
    cursor.execute(query, data)
    db.commit()
    return jsonify(movGetProducts(location))


def checkQuantity(location, product_id, quantity):
    products = movGetProducts(location)
    for product in products:
        if product["pid"] == product_id and int(product["quantity"]) >= int(quantity):
            return True
    return False


if __name__ == '__main__':
    app.run(debug=True)
