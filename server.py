from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cd_collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    alpha2 = db.Column(db.String(2), nullable=False, unique=True)
    alpha3 = db.Column(db.String(3), nullable=False, unique=True)
    region = db.Column(db.String(8), nullable=False, unique=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(), nullable=False)
    countryCode = db.Column(db.String(3), db.ForeignKey('countries.alpha2'), nullable=False)
    isPublic = db.Column(db.Boolean(), nullable=False)
    phone = db.Column(db.String(50), unique=True)
    image = db.Column(db.String(200))

with app.app_context():
    db.create_all()

@app.route('/api/ping', methods=['GET'])
def send():
    return jsonify({"status": "ok"}), 200

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()

    # проверяем
    if data is None:
        return jsonify({'reason': 'Invalid JSON format'}), 400

    login = data.get('login', '')
    email = data.get('email', '')
    password = data.get('password', '')
    country_code = data.get('countryCode', '')
    is_public = data.get('isPublic', True)
    phone = data.get('phone', '')
    image = data.get('image', '')

    if not login or not email or not password or not country_code:
      return jsonify({'reason': 'missing data'}), 400

    if User.query.filter_by(login=login).first():
        return jsonify({'reason': 'User already exists'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'reason': 'User already exists'}), 400

    if len(password) >= 8:
        a = 0
        b = 0
        for i in range(len(password)):
            if password[i] == '#' or password[i] == '*' or password[i] == '%' or password[i] == '&' or password[i] == '!' or password[i] == '@' or password[i] == '$' or password[i] == '^' or password[i] == '(' or password[i] == ')' or password[i] == '-' or password[i] == '+':
                a = 1
            elif password[i] == '0' or password[i] == '1' or password[i] == '2' or password[i] == '3' or password[i] == '4' or password[i] == '5' or password[i] == '6' or password[i] == '7' or password[i] == '8' or password[i] == '9':
                b = 1
        if a != 1 or b != 1:
            return jsonify({'reason': 'Password is too bad'}), 400
    else:
        return jsonify({'reason': 'Password is too short'}), 400

    if not Country.query.filter_by(alpha2=country_code).first():
        return jsonify({'reason': 'No such country'}), 400

    if len(image) > 200:
        return jsonify({'reason': 'Image is too long'}), 400

    if phone[0] != '+':
        return jsonify({'reason': 'Invalid phone number'}), 400

    user = User(login=login,
                    email=email,
                    country_code=country_code,
                    is_public=is_public,
                    image=image,
                    phone_number=phone)
    db.session.add(user)
    db.session.commit()
    return jsonify({'profile': user.to_dict()}), 200

def present_country(country):
    return {
        'id': country.id,
        'name': country.name
    }

@app.route('/api/countries', methods=['GET'])
def get_all_countries():
    regions = request.args.getlist('region')
    if not regions:
        countries = Country.query.all()
    else:
        countries = Country.query.filter(Country.region.in_(regions)).all()
    country_descriptions = [present_country(country) for country in countries]
    return jsonify(country_descriptions), 200

@app.route('/api/countries/<alpha2>', methods=['GET'])
def get_country_by_alpha2(alpha2):
    country = Country.query.filter_by(alpha2=alpha2).first()
    if not country:
        return jsonify({'reason': 'Country not found'}), 400
    return jsonify(present_country(country)), 200


@app.route('/api/countries', methods=['POST'])
def add_country():
    data = request.get_json()
    if data is None:
        return jsonify({'reason': 'Invalid JSON format'}), 400
    name = data.get('name')
    if not name:
        return jsonify({'reason': 'Missing name'}), 400
    if Country.query.filter_by(name=name).first():
        return jsonify({'reason': 'Country already exists'}), 400
    country = Country(name=name)
    db.session.add(country)
    db.session.commit()
    return jsonify(present_country(country)), 200

if __name__ == '__main__':
    app.run(debug=True)
