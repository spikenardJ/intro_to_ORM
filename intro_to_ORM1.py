# Question 1: Flask-SQLAlchemy Fitness Center Management

# Task 1: Setting Up Flask with Flask-SQLAlchemy

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields 
from marshmallow import ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:!Jaedyn77@localhost/fitness_center_db"
db = SQLAlchemy(app)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    name = fields.String(required=True)
    age = fields.Integer(required=True)
    phone = fields.String(required=True)
    email = fields.String(required=True)

    class Meta:
        fields = ("name", "age", "phone", "email", "id")

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

class WorkoutSessionSchema(ma.Schema):
    session_date = fields.Date(required=True)
    session_time = fields.String(required=True)
    activity = fields.String(required=True)
    member_id = fields.Integer(required=True)

    class Meta:
        fields = ("session_date", "session_time", "activity", "member_id")

workout_session_schema = WorkoutSessionSchema()
workout_sessions_schema = WorkoutSessionSchema(many=True)

class Member(db.Model):
    __tablename__ = "Members"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer())
    phone = db.Column(db.String(15))
    email = db.Column(db.String(320))
 
    workout_sessions = db.relationship("WorkoutSession", backref="member")

class WorkoutSession(db.Model):
    __tablename__ = "WorkoutSessions"
    session_id = db.Column(db.Integer, primary_key=True)
    session_date = db.Column(db.Date, nullable=False)
    session_time = db.Column(db.String(255), nullable=False)
    activity = db.Column(db.String(320), nullable=False)
    
  
    member_id = db.Column(db.Integer, db.ForeignKey("Members.id"))
    # member = db.relationship("Members", backref="workout_sessions", uselist=False)
    


# Task 2: Implementing CRUD Operations for Members Using ORM

@app.route("/members", methods=["GET"])
def get_members():
    members = Member.query.all()
    return members_schema.jsonify(members)

@app.route("/members", methods=["POST"])
def add_member():
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_member = Member(name=member_data["name"], age=member_data["age"], phone=member_data["phone"], email=member_data["email"])
    db.session.add(new_member)
    db.session.commit()
    return jsonify({"MESSAGE": "New member added successfully."}), 201

@app.route("/members/<int:id>", methods=["PUT"])
def update_member(id):
    member = Member.query.get_or_404(id)
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    member.name = member_data["name"]
    member.age = member_data["age"]
    member.phone = member_data["phone"]
    member.email = member_data["email"]
    db.session.commit()
    return jsonify({"MESSAGE": "Member details updated successfully."}), 200

@app.route("/members/<int:id>", methods=["DELETE"])
def delete_member(id):
    member = Member.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    return jsonify({"MESSAGE": "Member removed successfully."}), 200
    
    
# Task 3: Managing Workout Sessions with ORM

@app.route("/workout_sessions/<int:member_id>", methods=["GET"])
def query_workout_sessions_by_member_id(member_id):
    workout_sessions = WorkoutSession.query.filter_by(member_id=member_id).all()
    if workout_sessions:
        return workout_sessions_schema.jsonify(workout_sessions)
    else:
        return jsonify({"MESSAGE": "No Workout Sessions found for member, or member not found."}), 404
    
@app.route("/workout_sessions", methods=["POST"])
def add_workout_session():
    try:
        workout_session_data = workout_session_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_workout_session = WorkoutSession(session_date=workout_session_data["session_date"], session_time=workout_session_data["session_time"], activity=workout_session_data["activity"], member_id=workout_session_data["member_id"])
    db.session.add(new_workout_session)
    db.session.commit()
    return jsonify({"MESSAGE": "New workout session added successfully."}), 201

@app.route("/workout_sessions/<int:id>", methods=["PUT"])
def update_workout_session(id):
    workout_session = WorkoutSession.query.get_or_404(id)
    try:
        workout_session_data = workout_session_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    workout_session.session_date = workout_session_data["session_date"]
    workout_session.session_time = workout_session_data["session_time"]
    workout_session.activity = workout_session_data["activity"]
    workout_session.member_id = workout_session_data["member_id"]
    db.session.commit()
    return jsonify({"MESSAGE": "Workout session details updated successfully."}), 200

@app.route("/workout_sessions/<int:id>", methods=["DELETE"])
def delete_workout_session(id):
    workout_session = WorkoutSession.query.get_or_404(id)
    db.session.delete(workout_session)
    db.session.commit()
    return jsonify({"MESSAGE": "Workout session removed successfully."}), 200


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)