import os
import tornado.log
import tornado.ioloop
import tornado.web
import boto3
from jinja2 import Environment, PackageLoader
from dotenv import load_dotenv
load_dotenv('.env')

ENV = Environment(
    loader=PackageLoader('myapp', 'templates')
)

client = boto3.client(
  'ses',
  aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
  aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
  region_name=os.environ.get('AWS_DEFAULT_REGION')
)
class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.set_header("Content-Type", 'text/plain')
    self.write("Hello, world")

class FormHandler(tornado.web.RequestHandler):
    def post(self):
        response = client.send_email(
          Destination={
            'ToAddresses': ['gnealsr@gmail.com'],
          },
          Message={
            'Body': {
              'Text': {
                'Charset': 'UTF-8',
                'Data': 'This is the message body in text format.',
              },
            },
            'Subject': {'Charset': 'UTF-8', 'Data': 'Test email'},
          },
          Source='mailer@gregnealsr.com',
        )
        self.redirect('/thank-you')

    def get(self):
        # self.set_header("Content-Type", 'text/plain')
        # self.render('test_form.html')
        template = ENV.get_template('test_form.html')
        self.write(template.render())

class YouHandler(tornado.web.RequestHandler):
  def get(self):
    self.set_header("Content-Type", 'text/plain')
    name = self.get_query_argument('name', 'Nobody')
    self.write("Hello, {}".format(name))

class YouThreeHandler(tornado.web.RequestHandler):
  def get(self):
    self.set_header("Content-Type", 'text/plain')
    names = self.get_query_arguments('name')
    for name in names:
      self.write("Hello, {}\n".format(name))

def make_app():
  return tornado.web.Application([
    (r"/", MainHandler),
    (r"/test_form", FormHandler),
    (r"/hello3", YouThreeHandler),
    (r"/hello/(.*)", YouHandler),
    ], autoreload=True)

if __name__ == "__main__":

  tornado.log.enable_pretty_logging()

  app = make_app()
  app.listen(8888, print('hosting at 8888'))
  tornado.ioloop.IOLoop.current().start()
