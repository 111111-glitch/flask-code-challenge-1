#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json_as_ascii = False  # Adjusted to fix typo
app.json_encoder = None  # Resetting JSON encoder to default

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

# GET /heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    if heroes:
        return jsonify([hero.to_dict() for hero in heroes]), 200
    else:
        return jsonify({'error': 'No heroes found'}), 404

# GET /heroes/:id
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero:
        return jsonify(hero.to_dict()), 200
    else:
        return jsonify({'error': 'Hero not found'}), 404

# GET /powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    if powers:
        return jsonify([power.to_dict() for power in powers]), 200
    else:
        return jsonify({'error': 'No powers found'}), 404

# GET /powers/:id
@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power:
        return jsonify(power.to_dict()), 200
    else:
        return jsonify({'error': 'Power not found'}), 404

# PATCH /powers/:id
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if power:
        data = request.json
        description = data.get('description')
        if description:
            power.description = description
            try:
                db.session.commit()
                return jsonify(power.to_dict()), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'errors': [str(e)]}), 400
        else:
            return jsonify({'errors': ['Description must be provided']}), 400
    else:
        return jsonify({'error': 'Power not found'}), 404

# POST /hero_powers
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.json
    strength = data.get('strength')
    power_id = data.get('power_id')
    hero_id = data.get('hero_id')
    
    if not (strength and power_id and hero_id):
        return jsonify({'errors': ['Strength, power_id, and hero_id must be provided']}), 400
    
    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)
    
    if not (hero and power):
        return jsonify({'errors': ['Hero or Power not found']}), 404
    
    hero_power = HeroPower(strength=strength, hero=hero, power=power)
    
    try:
        db.session.add(hero_power)
        db.session.commit()
        return jsonify(hero_power.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'errors': [str(e)]}), 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)
