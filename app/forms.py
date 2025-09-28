# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, DateField, DateTimeLocalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from datetime import datetime, timedelta
from app.models import User, Doctor, Patient

# --- User Authentication Forms ---

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

# --- Patient-Facing Forms ---

class EditProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('', 'Select Gender'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    blood_group = SelectField('Blood Group', choices=[
        ('', 'Select Blood Group'), ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-')
    ])
    contact_number = StringField('Contact Number', validators=[DataRequired(), Length(max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = TextAreaField('Address', validators=[DataRequired()])
    submit = SubmitField('Save Changes')

class BookAppointmentForm(FlaskForm):
    doctor_id = SelectField('Doctor', coerce=int, validators=[DataRequired(message="Please select a doctor.")])
    appointment_date = DateTimeLocalField('Appointment Date & Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    reason = TextAreaField('Reason for Appointment', validators=[DataRequired()])
    submit = SubmitField('Book Appointment')

    def __init__(self, *args, **kwargs):
        super(BookAppointmentForm, self).__init__(*args, **kwargs)
        
        # --- DEBUGGING CODE ADDED ---
        print("\n--- DEBUG: Populating BookAppointmentForm ---")
        try:
            available_doctors = Doctor.query.filter_by(is_available=True).all()
            print(f"Found {len(available_doctors)} available doctors in the database.")
            if available_doctors:
                for doc in available_doctors:
                    print(f" -> Available: Dr. {doc.full_name} (ID: {doc.id})")
            else:
                print(" -> Query returned no available doctors.")
            
            self.doctor_id.choices = [
                (d.id, f"Dr. {d.full_name} ({d.specialization})") 
                for d in available_doctors
            ]
        except Exception as e:
            print(f"ERROR during form population: {e}")
            self.doctor_id.choices = []
        print("--- END DEBUG ---\n")

    def validate_appointment_date(self, field):
        if field.data:
            if field.data < datetime.now():
                raise ValidationError('Appointment time must be in the future.')
            # This validation rule has been re-added for more robust booking
            if field.data < (datetime.now() + timedelta(hours=24)):
                raise ValidationError('Appointments must be scheduled at least 24 hours in advance.')
            if field.data.weekday() >= 5:  # Monday is 0 and Sunday is 6
                raise ValidationError('Appointments are only available on weekdays.')
            if field.data.hour < 8 or field.data.hour >= 18:
                raise ValidationError('Appointments are only available between 8 AM and 6 PM.')

# --- Admin-Facing Forms ---

class AddDoctorForm(FlaskForm):
    
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    specialization = StringField('Specialization', validators=[DataRequired(), Length(max=100)])
    contact_number = StringField('Contact Number', validators=[DataRequired(), Length(max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    is_available = BooleanField('Available for Appointments', default=True)
    submit = SubmitField('Add Doctor')

class EditDoctorForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    specialization = StringField('Specialization', validators=[DataRequired(), Length(max=100)])
    contact_number = StringField('Contact Number', validators=[DataRequired(), Length(max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    is_available = BooleanField('Available for Appointments')
    user_id = SelectField('Link to User Account', coerce=int, validators=[Optional()])
    submit = SubmitField('Save Changes')

class AddPatientForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('', 'Select Gender'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    blood_group = SelectField('Blood Group', choices=[
        ('', 'Select Blood Group'), ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-')
    ])
    contact_number = StringField('Contact Number', validators=[DataRequired(), Length(max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = TextAreaField('Address', validators=[DataRequired()])
    submit = SubmitField('Add Patient')

class AddAppointmentForm(FlaskForm):
    patient_id = SelectField('Patient', coerce=int, validators=[DataRequired()])
    doctor_id = SelectField('Doctor', coerce=int, validators=[DataRequired()])
    appointment_date = DateTimeLocalField('Appointment Date & Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    reason = TextAreaField('Reason for Appointment', validators=[DataRequired()])
    submit = SubmitField('Add Appointment')

    def __init__(self, *args, **kwargs):
        super(AddAppointmentForm, self).__init__(*args, **kwargs)
        self.doctor_id.choices = [(d.id, f"{d.full_name} ({d.specialization})") for d in Doctor.query.filter_by(is_available=True).all()]
        self.patient_id.choices = [(p.id, p.full_name) for p in Patient.query.all()]