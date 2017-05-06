from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Owner(db.Model):
    """ Table storing dog owner info """

    __tablename__ = "owners"

    o_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(50), nullable=False)

    # Make a relationship to Dog and use backref so dog has a relationship
    # to Owner using the word 'owner'
    dogs = db.relationship("Dog", backref="owner")

    def __repr__(self):
        return "<Owner %s>" % (self.name)


class Dog(db.Model):
    """ Table storing dogs to be walked """

    __tablename__ = 'dogs'

    d_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    size = db.Column(db.String(10), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("owners.o_id"))

    # Connect Walkers and Dogs through WalkerDogs using secondary
    walkers = db.relationship("Walker",
                              secondary="walkerdogs")

    def __repr__(self):
        return "<Dog: %s>" % (self.name)


class Walker(db.Model):
    """Table to store dog walkers"""

    __tablename__ = 'walkers'

    w_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    day = db.Column(db.String(10), nullable=False)
    car = db.Column(db.String(20), nullable=True)

    # Connect Walkers and Dogs through WalkerDogs using secondary
    dogs = db.relationship("Dog",
                           secondary="walkerdogs")

    def __repr__(self):
        return "<Walker: %s walks on %s>" % (self.name, self.day)


class WalkerDog(db.Model):
    """ Association table for dogs and walkers """

    __tablename__ = 'walkerdogs'

    wd_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    dog_id = db.Column(db.Integer, db.ForeignKey("dogs.d_id"))
    walker_id = db.Column(db.Integer, db.ForeignKey("walkers.w_id"))

    def __repr__(self):
        return "<Dog Walker %d>" % (self.wd_id)


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///dogwalkers'
    db.app = app
    db.init_app(app)


def example():
    """ Create the tables and populate with some data """

    db.drop_all()
    db.create_all()

    owner1 = Owner(name="Shana", address="123 Main")

    # If you haven't committed yet, you can still make a connection between
    # the dog and owner by using the relationship attribute
    dog1 = Dog(name="Bootsy", size="med", owner=owner1)

    walker1 = Walker(name="Rachel", day="Wednesday", car="truck")

    # Add a bunch of rows at once using db.session.add_all()
    db.session.add_all([owner1, dog1, walker1])
    db.session.commit()

    walkerdog1 = WalkerDog(dog_id=dog1.d_id, walker_id=walker1.w_id)
    db.session.add(walkerdog1)
    db.session.commit()

    print "Dog %s is walked by %s and owned by %s" % (dog1.name,
                                                      dog1.walkers[0].name,
                                                      dog1.owner.name)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    app = Flask(__name__)
    connect_to_db(app)
    print "Connected to DB."