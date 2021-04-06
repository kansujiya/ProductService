
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
# from RabbitMQSender import RabbitMQSender
import pika
from kafka import KafkaProducer

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

print(__name__)

app = Flask(__name__)

client = ProductServiceClient()
producer = KafkaProducer(bootstrap_servers = 'localhost:9092')

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
    sendKafka()
    # print(res)    
    # rbSender = RabbitMQSender("OrderCreation")
    connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
    channel = connection.channel()
    channel.queue_declare(queue='OrderCreation')
    # rbSender.publish_order_creation(res.order_id, res.msg, res.product_id, res.order_date, 'OrderPlaced')
    body = res.msg + ' on ' + res.order_date + ' for ' + str(res.product_id) + ' Order Id is ' + str(res.order_id)
    channel.basic_publish(exchange='', routing_key='OrderCreation', body=body)
    connection.close()

    # Kafka    
    producer.send('test', json.dumps(body).encode('utf-8'))
    return jsonify({'product_id': res.product_id, 'order_id': res.order_id, 'order_date': res.order_date, 'Message': res.msg})    


def sendKafka():
    producer = KafkaProducer(bootstrap_servers = 'localhost:9092')
    mm = "hihihsuresh"
    producer.send('test', mm.encode('utf-8'))
# def __init__(self, queueName):
#     connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
#     channel = connection.channel()
#     channel.queue_declare(queue=queueName)

# def publish_order_creation(self, order_id, msg, product_id, date, key):
#     body = msg + 'on' + date + 'for' + str(product_id) + 'Order Id is' + str(order_id)
#     channel.basic_publish(exchange='', routing_key=key, body=body)
#     connection.close()

# #POST
# @app.route('/place_order', methods=['POST'])
# def add_book():	
# 	requestData = request.get_json()	
# 	if (validBookObject(requestData)):
# 		# books.insert(0, requestData)		
# 		Book.add_book(requestData['name'], requestData['price'], requestData['isbn'])
# 		response = Response("Book sucessfully added", 201, mimetype='application/json')
# 		response.headers['Location'] = "/addbooks/" + str(requestData['isbn'])
# 		return response
# 	else:
# 		invalidBookObject = {
# 			"error": "Invalid book object passed"
# 		}
# 		response = Response(json.dumps(invalidBookObject), status=400,mimetype='application/json')
# 		return response

app.run(port=9000)

