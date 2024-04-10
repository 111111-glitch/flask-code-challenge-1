from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    super_name = Column(String, nullable=False)
    hero_powers = relationship('HeroPower', back_populates='hero', cascade='all, delete')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name,
            'hero_powers': [hero_power.to_dict() for hero_power in self.hero_powers]
        }

    def __repr__(self):
        return f'<Hero {self.id}>'

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    hero_powers = relationship('HeroPower', back_populates='power', cascade='all, delete')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

    @validates('description')
    def validate_description(self, key, description):
        assert len(description) >= 20, 'Description must be at least 20 characters long'
        return description

    def __repr__(self):
        return f'<Power {self.id}>'

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = Column(Integer, primary_key=True)
    strength = Column(String, nullable=False)
    hero_id = Column(Integer, ForeignKey('heroes.id'), nullable=False)
    power_id = Column(Integer, ForeignKey('powers.id'), nullable=False)
    hero = relationship('Hero', back_populates='hero_powers')
    power = relationship('Power', back_populates='hero_powers')

    def to_dict(self):
        return {
            'id': self.id,
            'strength': self.strength,
            'hero_id': self.hero_id,
            'power_id': self.power_id,
            'hero': self.hero.to_dict(),
            'power': self.power.to_dict()
        }

    @validates('strength')
    def validate_strength(self, key, strength):
        assert strength in ['Strong', 'Weak', 'Average'], 'Strength must be "Strong", "Weak", or "Average"'
        return strength

    def __repr__(self):
        return f'<HeroPower {self.id}>'
