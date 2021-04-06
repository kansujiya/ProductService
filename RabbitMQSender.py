import pika

class RabbitMQSender:

  def __init__(self, queueName):
    self.connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
    self.channel = connection.channel()
    self.channel.queue_declare(queue=queueName)

  def publish_order_creation(self, order_id, msg, product_id, date, key):
    body = msg + 'on ' + date + ' for ' + str(product_id) + ' Order Id is ' + str(order_id)
    self.channel.basic_publish(exchange='', routing_key=key, body=body)
    self.connection.close()
