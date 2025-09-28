# app/routes/admin_routes.py
from sqlalchemy import func
from collections import defaultdict
import json
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.routes import admin_bp
from functools import wraps

# --- Imports ---
from app.models import User, Doctor, Patient, Appointment
from app.forms import AddDoctorForm, AddPatientForm, AddAppointmentForm

# Imports needed to define forms directly in this file
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, BooleanField, TextAreaField, DateTimeLocalField
from wtforms.validators import DataRequired, Length, Email, Optional


# --- Local Form Definitions (Bypass Solution) ---

class EditDoctorForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    specialization = StringField('Specialization', validators=[DataRequired(), Length(max=100)])
    contact_number = StringField('Contact Number', validators=[DataRequired(), Length(max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    is_available = BooleanField('Available for Appointments')
    user_id = SelectField('Link to User Account', coerce=int, validators=[Optional()])
    submit = SubmitField('Save Changes')

class EditAppointmentForm(FlaskForm):
    """A form for the admin to edit an appointment's status and add notes."""
    status = SelectField('Status', choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')])
    notes = TextAreaField('Doctor\'s Notes (optional)')
    submit = SubmitField('Update Appointment')


# --- Decorator for Admin-Only Routes ---

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


# --- Admin Routes ---

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    doctor_count = Doctor.query.count()
    patient_count = Patient.query.count()
    appointment_count = Appointment.query.count()
    recent_appointments = Appointment.query.order_by(Appointment.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                           doctor_count=doctor_count,
                           patient_count=patient_count,
                           appointment_count=appointment_count,
                           recent_appointments=recent_appointments)

# --- Doctor Management ---

@admin_bp.route('/doctors')
@login_required
@admin_required
def manage_doctors():
    doctors = Doctor.query.all()
    return render_template('admin/doctors.html', doctors=doctors)

@admin_bp.route('/doctor/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_doctor():
    form = AddDoctorForm()
    if form.validate_on_submit():
        doctor = Doctor()
        form.populate_obj(doctor)
        db.session.add(doctor)
        db.session.commit()
        flash('Doctor added successfully!', 'success')
        return redirect(url_for('admin.manage_doctors'))
    return render_template('admin/doctor_form.html', form=form)

@admin_bp.route('/doctor/edit/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    form = EditDoctorForm(obj=doctor)
    
    available_users = User.query.filter(User.is_admin == False, User.doctor == None, User.patient == None).all()
    form.user_id.choices = [(u.id, u.username) for u in available_users]
    if doctor.user:
        form.user_id.choices.insert(0, (doctor.user_id, doctor.user.username))

    if form.validate_on_submit():
        # ** THE FIX: Explicitly setting each field to guarantee the data is saved. **
        doctor.first_name = form.first_name.data
        doctor.last_name = form.last_name.data
        doctor.specialization = form.specialization.data
        doctor.contact_number = form.contact_number.data
        doctor.email = form.email.data
        doctor.is_available = form.is_available.data  # This now guarantees the status is saved
        doctor.user_id = form.user_id.data if form.user_id.data else None
        
        db.session.commit()
        flash(f'Profile for Dr. {doctor.full_name} updated successfully!', 'success')
        return redirect(url_for('admin.manage_doctors'))
        
    return render_template('admin/edit_doctor.html', form=form, doctor=doctor)

@admin_bp.route('/doctor/delete/<int:doctor_id>', methods=['POST'])
@login_required
@admin_required
def delete_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    # Note: In a real app, you might want to handle existing appointments first
    db.session.delete(doctor)
    db.session.commit()
    flash(f'Dr. {doctor.full_name} has been deleted.', 'success')
    return redirect(url_for('admin.manage_doctors'))


# --- Patient Management ---

@admin_bp.route('/patients')
@login_required
@admin_required
def manage_patients():
    patients = Patient.query.all()
    return render_template('admin/patients.html', patients=patients)

@admin_bp.route('/patient/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_patient():
    form = AddPatientForm()
    if form.validate_on_submit():
        patient = Patient()
        form.populate_obj(patient)
        db.session.add(patient)
        db.session.commit()
        flash('Patient added successfully!', 'success')
        return redirect(url_for('admin.manage_patients'))
    return render_template('admin/patient_form.html', form=form)

@admin_bp.route('/patient/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_patient(id):
    patient = Patient.query.get_or_404(id)
    form = AddPatientForm(obj=patient)
    if form.validate_on_submit():
        form.populate_obj(patient)
        db.session.commit()
        flash('Patient updated successfully!', 'success')
        return redirect(url_for('admin.manage_patients'))
    return render_template('admin/patient_form.html', form=form, patient=patient)

@admin_bp.route('/patient/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    flash('Patient deleted successfully!', 'success')
    return redirect(url_for('admin.manage_patients'))


# --- Appointment Management ---

@admin_bp.route('/appointments')
@login_required
@admin_required
def manage_appointments():
    appointments = Appointment.query.order_by(Appointment.appointment_date.desc()).all()
    return render_template('admin/appointments.html', appointments=appointments)

@admin_bp.route('/appointment/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_appointment():
    form = AddAppointmentForm()
    if form.validate_on_submit():
        appointment = Appointment()
        form.populate_obj(appointment)
        appointment.status = 'Scheduled'
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment scheduled successfully!', 'success')
        return redirect(url_for('admin.manage_appointments'))
    return render_template('admin/appointment_form.html', form=form)

# --- NEW: Routes to View and Edit Appointments ---

@admin_bp.route('/appointment/view/<int:appointment_id>')
@login_required
@admin_required
def view_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    return render_template('admin/view_appointment.html', appointment=appointment)

@admin_bp.route('/appointment/edit/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    form = EditAppointmentForm(obj=appointment)
    if form.validate_on_submit():
        form.populate_obj(appointment)
        db.session.commit()
        flash('Appointment updated successfully!', 'success')
        return redirect(url_for('admin.manage_appointments'))
    return render_template('admin/edit_appointment.html', form=form, appointment=appointment)

@admin_bp.route('/appointment/delete/<int:appointment_id>', methods=['POST'])
@login_required
@admin_required
def delete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    db.session.delete(appointment)
    db.session.commit()
    flash('Appointment deleted successfully!', 'success')
    return redirect(url_for('admin.manage_appointments'))

@admin_bp.route('/reports')
@login_required
@admin_required
def reports():
    # --- Chart 1: Appointment Status Distribution ---
    status_counts = db.session.query(
        Appointment.status, 
        func.count(Appointment.status)
    ).group_by(Appointment.status).all()
    
    # Prepare data for the doughnut chart
    status_labels = [status[0] for status in status_counts]
    status_data = [status[1] for status in status_counts]

    # --- Chart 2: Monthly Appointments (Last 12 Months) ---
    monthly_counts = db.session.query(
        func.strftime('%Y-%m', Appointment.appointment_date), 
        func.count(Appointment.id)
    ).group_by(func.strftime('%Y-%m', Appointment.appointment_date)).order_by(
        func.strftime('%Y-%m', Appointment.appointment_date)
    ).all()
    
    # Prepare data for the bar chart
    monthly_labels = [item[0] for item in monthly_counts]
    monthly_data = [item[1] for item in monthly_counts]

    return render_template('admin/reports.html',
                           status_labels=json.dumps(status_labels),
                           status_data=json.dumps(status_data),
                           monthly_labels=json.dumps(monthly_labels),
                           monthly_data=json.dumps(monthly_data))
    
@admin_bp.route('/settings')
@login_required
@admin_required
def settings():
    return render_template('admin/settings.html')