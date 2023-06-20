from init import db, ma
from marshmallow import fields

class Pc_Build_Part(db.Model):
    __tablename__ = 'pc_build_parts'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    value = db.Column(db.Float)

    pc_id = db.Column(db.Integer, db.ForeignKey(
        'pcs.id', ondelete='CASCADE'), nullable=False)
    
    part_id = db.Column(db.Integer, db.ForeignKey(
        'parts.id', ondelete='CASCADE'), nullable=False)
    
    pc = db.relationship('Pc', back_populates='pc_build_parts')
    part = db.relationship('Part', back_populates='pc_build_parts')

class Pc_Build_PartSchema(ma.Schema):
    pc = fields.Nested('PcSchema', only=['name'])
    part = fields.Nested('PartSchema',only=['name','description'])
    
    class Meta:
        fields = ('number','value','part','pc')
        ordered = True