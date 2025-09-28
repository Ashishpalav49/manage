# app/models.py
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    # Relationship with Patient
    patient = db.relationship('Patient', backref='user', uselist=False) # Changed to one-to-one

    # Add this line for the doctor relationship
    doctor = db.relationship('Doctor', backref='user', uselist=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add the user_id foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=True)
    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20))
    email = db.Column(db.String(120))
    is_available = db.Column(db.Boolean, default=True)

    # Relationships
    appointments = db.relationship('Appointment', backref='doctor', lazy='dynamic')

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f'<Doctor {self.full_name}>'

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10))
    blood_group = db.Column(db.String(5))
    contact_number = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    
    # ADD THIS LINE
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    appointments = db.relationship('Appointment', backref='patient', lazy='dynamic')
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        today = datetime.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
    
    def __repr__(self):
        return f'<Patient {self.full_name}>'
        
# ... (Appointment model is unchanged)
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.Text)
    notes = db.Column(db.Text) # This field will be used by doctors
    status = db.Column(db.String(20), default='Scheduled')  # Scheduled, Completed, Cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Appointment {self.id}: {self.patient.full_name} with Dr. {self.doctor.full_name}>'