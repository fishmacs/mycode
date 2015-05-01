from datetime import datetime
from bson.objectid import ObjectId

from mongokit import IS, OR
from flask.ext.mongokit import Document
from flask.ext.babel import lazy_gettext as _

import timezone
from app import db


class IdMixin(object):
    @property
    def id(self):
        return self._id


@db.register
class User(Document, IdMixin):
    __collection__ = 'user'
    structure = {
        'username': unicode,
        'fullname': unicode,
        'password': basestring,
        'is_active': bool,
        'last_login': datetime,
        #'created_time': datetime,
        'roles': [IS('student', 'parent', 'teacher', 'admin')],
        'device': basestring,
        'device_free': bool,
        'school': {'id': ObjectId, 'name': unicode},
        'class': OR(
            {
                'id': ObjectId,
                'name': unicode,
                'grade': int,
                'courses': [{
                    'id': ObjectId,
                    'code': int,
                    'name': unicode
                }]
            },
            [{'id': ObjectId, 'name': unicode, 'grade': int}]
        ),
        'courses': [{'id': ObjectId, 'code': int, 'name': unicode, 'name2': unicode}],
        'newwares': [ObjectId]
    }
    required_fields = ['username', 'password', 'is_active']
    default_values = {
        'is_active': True,
        #'created_time': timezone.now,
        'device_free': False
    }

    def is_teacher(self):
        return self.role == 'teacher'
        
        
@db.register
class School(Document, IdMixin):
    __collection__ = 'school'
    structure = {
        'name': unicode,
        'name2': unicode,
        'email': unicode,
        'phone': basestring
    }
    required_fields = ['name']


@db.register
class SchoolClass(Document, IdMixin):
    __collection__ = 'class'
    structure = {
        'school': {'id': ObjectId, 'name': unicode},
        'name': unicode,
        'grade': int
    }


@db.register
class Course(Document, IdMixin):
    __collection__ = 'course'
    structure = {
        'name': unicode,
        'name2': unicode,
        'code': int,
        'school': {'id': ObjectId, 'name': unicode},
        'class': {'id': ObjectId, 'name': unicode, 'grade': int},
        'is_active': bool,
        'start_date': datetime,
        'end_date': datetime,
        'teachers': [{'id': ObjectId, 'name': unicode}],
        'students': [ObjectId],
        'image': unicode
    }
    required_fields = ['name']
    default_values = {
        'is_active': True,
    }


@db.register
class Category(Document, IdMixin):
    __collection__ = 'category'
    structure = {
        'name': unicode,
        'name2': unicode
    }
    required_fields = ['name']


@db.register
class Courseware(Document, IdMixin):
    STATE_FETCHING = 0
    STATE_WAITING = 1
    STATE_CONVERTING = 5
    STATE_CONVERTED = 10
    STATE_CONFIRMED = 20
    STATE_DELIVERING = 30
    STATE_FINISHED = 40
    STATE_FETCH_ERROR = -1
    STATE_CONVERT_ERROR = -2
    STATE_DELIVER_ERROR = -3

    STATE_DISPLAY = {
        STATE_FETCHING: _('downloading') + '...',
        STATE_WAITING: _('wait for convert'),
        STATE_CONVERTING: _('converting') + '...',
        STATE_CONVERTED: _('converted'),
        STATE_DELIVERING: _('delivering') + '...',
        STATE_FINISHED: _('delivered'),
        STATE_FETCH_ERROR: _('download failure'),
        STATE_CONVERT_ERROR: _('convert failure'),
        STATE_DELIVER_ERROR: _('deliver failure')
    }
    
    __collection__ = 'courseware'
    structure = {
        'name': unicode,
        'name2': unicode,
        'course': {'id': ObjectId, 'code': int, 'name': unicode, 'name2': unicode},
        'teacher': {'id': ObjectId, 'name': unicode},
        'students': [ObjectId],
        'category': {'name': unicode, 'name2': unicode},
        'state': int,
        'srcpath': basestring,
        'outpath': basestring,
        'remote_image': unicode,
        'local_image': basestring,
        #'created_time': datetime,
        'modified_time': datetime,
    }
    required_fields = ['name', 'course', 'teacher', 'students']
    default_values = {
        'state': STATE_WAITING,
        #'created_time': timezone.now,
        'modified_time': timezone.now
    }
    

@db.register
class Delivered(Document, IdMixin):
    __collection__ = 'delivered'
    structure = {
        'device': basestring,
        'courseware': ObjectId,
        'srcpath': basestring,
        'outpath': basestring,
        #'created_time': datetime,
        'download_time': datetime
    }
    required_fields = ['device', 'courseware', 'srcpath', 'outpath']
    # default_values = {
    #     'created_time': timezone.now
    # }
    