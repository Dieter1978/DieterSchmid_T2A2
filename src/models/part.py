from init import db, ma

class Part(db.Model):
    __tablename__="parts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text())
    value = db.Column(db.Float)

    pc_build_parts = db.relationship(
        'Pc_Build_Part', back_populates='part', cascade='all,delete')

class PartSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'value')