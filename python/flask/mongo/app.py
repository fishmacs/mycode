import pytz
from datetime import datetime

from flask import Flask, request, render_template, redirect, url_for
from flask.ext.mongokit import MongoKit, Document

app = Flask(__name__)

app.config.MONGODB_DATABASE = 'flask'
app.config.MONGODB_HOST = 'localhost'


def now():
    return datetime.utcnow().replace(tzinfo=pytz.utc)

    
class IdMixin(object):
    @property
    def id(self):
        return self._id

db = MongoKit(app)


@db.register
class Task(Document, IdMixin):
    __collection__ = 'tasks'
    structure = {
        'title': unicode,
        'text': unicode,
        'creation': datetime,
    }
    required_fields = ['title', 'creation']
    default_values = {'creation': now}
    use_dot_notation = True


@db.register
class Root(Document):

    structure = {
        'root': int
    }
    use_dot_notation = True
    required_fields = ['root']


@db.register
class A(Root):
    __collection__ = 'root'
    
    structure = {
        'a_field': basestring,
    }
    required_fields = ['a_field']


@db.register
class B(Root):
    __collection__ = 'root'
    structure = {
        'b_field': basestring,
    }


@db.register
class C(A, B):
    __collection__ = 'root'
    structure = {'c_field': float}
