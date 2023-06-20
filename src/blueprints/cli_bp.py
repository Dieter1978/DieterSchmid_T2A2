from flask import Blueprint
from datetime import date
from models.user import User
from models.part import Part
from models.pc_build_part import Pc_Build_Part
from models.pc import Pc
from init import db, bcrypt

cli_bp = Blueprint('db', __name__)

@cli_bp.cli.command('create')
def create_db():
    db.drop_all()
    db.create_all()
    print('Tables created successfully')

@cli_bp.cli.command('seed')
def seed_db():
    users = [
        User(
            email='admin@spam.com',
            password=bcrypt.generate_password_hash('spinynorm').decode('utf8'),
            is_admin=True
        ),
        User(
            name='John Cleese',
            email='cleese@spam.com',
            password=bcrypt.generate_password_hash(
                'tisbutascratch').decode('utf8')
        )
    ]
    # Create an instance of the User model in memory
    # Add the user to the session (transaction)
    #Truncate table
    db.session.query(User).delete()
    db.session.add_all(users)
    db.session.commit()

    pcs = [
        Pc(
           name="The Hog",
           description="Beast of a machine",
           value=0,
           user=users[0]
        ),
        Pc(
           name="The Dart",
           description="Stealthy and quiet",
           value=0,
           user=users[0]
        ),
        Pc(
           name="The Beetle",
           description="Monster of a machine",
           value=0,
           user=users[1]
        )
    ]
    # Create an instance of the Pc model in memory
    # Add the pcs to the session (transaction)
    #Truncate table
    db.session.query(Pc).delete()
    db.session.add_all(pcs)
    db.session.commit()

    parts = [
        Part(
            name="16GB RAM",
            description="stick of RAM",
            value=100.00
        ),
        Part(
            name="32GB RAM",
            description="stick of RAM",
            value=180.00
        ),
        Part(
            name="i7 11700KF intel",
            description="super fast cpu",
            value=399.00
        ),
        Part(
            name="Ryzen 9 7950X3D",
            description="Really really fast CPU",
            value=1000.00
        ),
        Part(
            name="GeForce RTX 3060",
            description="12GB super fast graphics card",
            value=499.00
        )
    ]

    # Create an instance of the Part model in memory
    # Add the parts to the session (transaction)
    #Truncate table
    db.session.query(Part).delete()
    db.session.add_all(parts)
    db.session.commit()

    pc_build_parts = [
        Pc_Build_Part(
        pc = pcs[0],
        part = parts[0]
        ),
        Pc_Build_Part(
        pc = pcs[0],
        part = parts[2]
        ),
        Pc_Build_Part(
        pc = pcs[0],
        part = parts[4]
        )


    ]

     # Create an instance of the PC_Build_Part model in memory
    # Add the pc_build_parts to the session (transaction)
    #Truncate table
    db.session.query(Pc_Build_Part).delete()
    db.session.add_all(pc_build_parts)
    db.session.commit()