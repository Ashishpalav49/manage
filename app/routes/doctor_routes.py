# app/routes/doctor_routes.py
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Appointment, Patient
from app.routes import doctor_bp # We will create this blueprint next
from functools import wraps
from datetime import datetime

def doctor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.doctor is None:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@doctor_bp.route('/dashboard')
@login_required
@doctor_required
def dashboard():
    doctor = current_user.doctor
    # Get appointments for the logged-in doctor
    now = datetime.utcnow()
    upcoming_appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.appointment_date >= now
    ).order_by(Appointment.appointment_date.asc()).all()

    past_appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.appointment_date < now
    ).order_by(Appointment.appointment_date.desc()).all()
    
    return render_template('doctor/dashboard.html', 
                           upcoming_appointments=upcoming_appointments,
                           past_appointments=past_appointments)

@doctor_bp.route('/appointment/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
@doctor_required
def view_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    # Ensure the appointment belongs to the current doctor
    if appointment.doctor_id != current_user.doctor.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('doctor.dashboard'))
        
    if request.method == 'POST':
        appointment.notes = request.form.get('notes')
        appointment.status = request.form.get('status', appointment.status)
        db.session.commit()
        flash('Appointment details updated successfully.', 'success')
        return redirect(url_for('doctor.view_appointment', appointment_id=appointment.id))
        
    return render_template('doctor/view_appointment.html', appointment=appointment)