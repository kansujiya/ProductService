from concurrent import futures
import time
import codegen
import grpc
import product_pb2
import product_pb2_grpc
from datetime import date
import pika
from kafka import KafkaProducer
from flask import json

producer = KafkaProducer(bootstrap_servers = 'localhost:9092')

class PlaceOrderServiceServicer(product_pb2_grpc.PlaceOrderServiceServicer): 
	def PlaceOrder(self, request, context):
		# id = request.order_id
		print('grpc request')
		print(request.product_id)
		print(context)
		order = product_pb2.Order(
			order_id = request.product_id * 3,
			order_date = str(date.today()),
			product_id = request.product_id,
			msg = "order placed succesfully"
		)
		print(order)
		publishRabbimtMq(order.order_id)
		publishKafkaMsg(order.order_id)
		return order

def publishRabbimtMq(order_id):
	connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
	channel = connection.channel()
	channel.queue_declare(queue='OrderCreation')		
	body = "Order placed succesfully: Order Id is :" + str(order_id)
	channel.basic_publish(exchange='', routing_key='OrderCreation', body=body)
	connection.close()	

def publishKafkaMsg(order_id):
	body = "Order placed succesfully: Order Id is :" + str(order_id)
	producer.send('test', json.dumps(body).encode('utf-8'))

if __name__ == '__main__':
	# Run a gRPC server with one thread.
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
	# Adds the servicer class to the server.	
	product_pb2_grpc.add_PlaceOrderServiceServicer_to_server(PlaceOrderServiceServicer(), server)
	server.add_insecure_port('0.0.0.0:6556')
	server.start()
	print('API server started. Listening at 0.0.0.0:6556.')
	while True:
		time.sleep(60)