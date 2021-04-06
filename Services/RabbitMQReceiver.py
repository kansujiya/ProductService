import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
channel = connection.channel()
channel.queue_declare(queue='OrderCreation')

def callback(ch, method, properties, body):  
  print("Received: %r" % (body,))

channel.basic_consume('OrderCreation', callback, auto_ack=True)

channel.start_consuming()