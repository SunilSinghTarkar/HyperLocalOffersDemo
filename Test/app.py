from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://avnadmin:AVNS_iNf7uPwTKi16T5Adrcj@mysql-1206eb68-hyperlocaloffers.e.aivencloud.com:24725/defaultdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# Define a User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)

#     def __repr__(self):
#         return f'<User {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    users = User.query.all()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list), 200

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.json['name']
    email = request.json['email']
    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully!'}), 201

@app.route('/get_user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user:
        return jsonify({'id': user.id, 'name': user.name, 'email': user.email})
    else:
        return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
