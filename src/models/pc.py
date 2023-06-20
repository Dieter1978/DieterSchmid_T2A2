from init import db, ma
from marshmallow import fields


class Pc(db.Model):
    __tablename__="pcs"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text())
    value = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', back_populates='pcs')

    pc_build_parts = db.relationship(
        'Pc_Build_Part', back_populates='pc', cascade='all,delete')

class PcSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude=[
                         'password', 'pcs'])
    class Meta:
        fields = ('id', 'name', 'description', 'value','user')
        ordered = True