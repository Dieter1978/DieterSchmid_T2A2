from init import db, ma
from marshmallow.validate import Length, OneOf, And, Regexp
from marshmallow import fields

class Part(db.Model):
    __tablename__="parts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text())
    value = db.Column(db.Float)

    pc_build_parts = db.relationship(
        'Pc_Build_Part', back_populates='part', cascade='all,delete')

class PartSchema(ma.Schema):
    name = fields.String(required=True, validate=And(
        Length(min=5, error='Title must be at least 3 characters long'),
        error='Must be 5 characters long'))
    
    description = fields.String(load_default='')

    value = fields.Float(load_default=0)

    class Meta:
        fields = ('id', 'name', 'description', 'value')