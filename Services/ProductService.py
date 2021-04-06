
from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
from flask import json
from functools import wraps
import datetime
from concurrent import futures
import codegen
import grpc 
import product_pb2
import product_pb2_grpc

SERVER_ADDRESS = '0.0.0.0'
PORT = 6556

class ProductServiceClient(object):
    def __init__(self):
        self.channel = grpc.insecure_channel(f'{SERVER_ADDRESS}:{PORT}')
        self.stub = product_pb2_grpc.PlaceOrderServiceStub(self.channel)
    
    def get_placeOrder(self, product_id):

        request = product_pb2.PlaceOrderRequest(
            product_id = product_id
        )

        try:
            return self.stub.PlaceOrder(request)
            print(response)
        except grpc.RpcError as err:
            print(err.details()) #pylint: disable=no-member
            print('{}, {}'.format(err.code().name, err.code().value)) #pylint: disable=no-member


products = [
	{
        'id': 100,
		'name': 'iPhone SE',
		'color': 'White',
        'description': 'Apple new launched.',
		'price': '100 rupee'
	},
	{
        'id': 200,
		'name': 'iPhone XR',
		'color': 'Red',
        'description': 'Apple new launched.',
		'price': '200 rupee'
	},
    {
        'id': 300,
		'name': 'iPhone X',
		'color': 'Red',
        'description': 'Apple new launched.',
		'price': '200 rupee'
	},
    {
        'id': 400,
		'name': 'iPhone 6',
		'color': 'Red',
        'description': 'Apple new launched.',
		'price': '200 rupee'
	},
    {
        'id': 500,
		'name': 'iPhone 8',
		'color': 'Red',
        'description': 'Apple new launched.',
		'price': '200 rupee'
	}
]

app = Flask(__name__)
client = ProductServiceClient()

#GET
@app.route('/') 
def print_hello():
	return 'Python gRPC'

@app.route('/products')
def get_products():
	return jsonify({'products': products})

@app.route('/productDetail/<int:id>')
def get_product_id(id):
    res = next((sub for sub in products if sub['id'] == id), None)
    return jsonify(res)	

@app.route('/placeOrder/<int:id>')
def place_order(id):
    res = client.get_placeOrder(id)    
    print(res)
    return jsonify({'product_id': res.product_id, 'order_id': res.order_id, 'order_date': res.order_date, 'Message': res.msg})    

app.run(port=9000)

