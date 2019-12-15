from mongoengine import Document, fields

# Create your models here.

class Certification(Document):
    _id = fields.ObjectIdField(require=True)
    user_id = fields.ObjectIdField(require=True)
    org = fields.StringField(required=True)
    name = fields.StringField(required=True)
    tags = fields.ListField(required=True)
    apply_time = fields.DateTimeField(require=True)
    deal_time = fields.DateTimeField(require=True)
    state = fields.StringField(require=True)   # 通过的状态
    _class = fields.StringField()
    meta = {'collection' : 'Certification'}

class users(Document):
    _id = fields.ObjectIdField(require=True)
    email = fields.StringField(required=True)
    userName = fields.StringField(required=True)
    password = fields.StringField(required=True)
    photo = fields.StringField(required=True)
    point = fields.StringField(required=True)
    _class = fields.StringField()
    meta = {'collection' : 'users'}
