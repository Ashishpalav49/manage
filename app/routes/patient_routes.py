# app/routes/patient_routes.py
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Patient, Appointment, Doctor
from app.forms import BookAppointmentForm, EditProfileForm
from datetime import datetime
from app.routes import patient_bp
from functools import wraps

# This is a helper decorator to ensure a patient profile exists for a route.
def profile_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        if not patient:
            flash('Please create your patient profile to access this page.', 'warning')
            return redirect(url_for('patient.edit_profile'))
        # Pass the patient object to the decorated function
        return f(patient, *args, **kwargs)
    return decorated_function

# --- Patient Dashboard ---
@patient_bp.route('/dashboard')
@profile_required
def dashboard(patient):
    now = datetime.now()
    upcoming_appointments = Appointment.query.filter(
        Appointment.patient_id == patient.id,
        Appointment.appointment_date > now
    ).order_by(Appointment.appointment_date.asc()).all()
    past_appointments = Appointment.query.filter(
        Appointment.patient_id == patient.id,
        Appointment.appointment_date <= now
    ).order_by(Appointment.appointment_date.desc()).all()
    
    return render_template('patient/dashboard.html', 
                           patient=patient,
                           upcoming_appointments=upcoming_appointments,
                           past_appointments=past_appointments)

# --- Profile Management ---
# This route does NOT use the decorator, because its purpose is to create the profile.
@patient_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    form = EditProfileForm(obj=patient)
    
    if form.validate_on_submit():
        if patient is None:
            patient = Patient(user_id=current_user.id)
            db.session.add(patient)
        
        form.populate_obj(patient)
        db.session.commit()
        flash('Your profile has been updated successfully!', 'success')
        return redirect(url_for('patient.dashboard'))
    
    return render_template('patient/edit_profile.html', form=form, patient=patient)

# --- Appointment Management ---
@patient_bp.route('/appointments')
@profile_required
def appointments(patient):
    all_appointments = Appointment.query.filter_by(patient_id=patient.id).order_by(Appointment.appointment_date.desc()).all()
    return render_template('patient/appointments.html', 
                           appointments=all_appointments,
                           patient=patient)

@patient_bp.route('/book-appointment', methods=['GET', 'POST'])
@profile_required
def book_appointment(patient):
    form = BookAppointmentForm()
    # Query available doctors and pass to template
    available_doctors = Doctor.query.filter_by(is_available=True).all()
    if form.validate_on_submit():
        appointment = Appointment(
            patient_id=patient.id,
            doctor_id=form.doctor_id.data,
            appointment_date=form.appointment_date.data,
            reason=form.reason.data,
            status='Scheduled'
        )
        db.session.add(appointment)
        db.session.commit()
        # Debug print to confirm creation
        print(f"DEBUG: Created appointment: id={appointment.id}, patient_id={appointment.patient_id}, doctor_id={appointment.doctor_id}, date={appointment.appointment_date}, reason={appointment.reason}, status={appointment.status}")
        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('patient.dashboard'))
    elif form.is_submitted():
        # If form was submitted but not valid, show errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
    return render_template('patient/book_appointment.html', form=form, patient=patient, doctors=available_doctors)

@patient_bp.route('/view-appointment/<int:id>')
@profile_required
def view_appointment(patient, id):
    appointment = Appointment.query.get_or_404(id)
    if appointment.patient_id != patient.id:
        flash('You do not have permission to view this appointment.', 'danger')
        return redirect(url_for('patient.dashboard'))
    
    return render_template('patient/view_appointment.html', appointment=appointment, patient=patient)

@patient_bp.route('/cancel-appointment/<int:id>', methods=['POST'])
@profile_required
def cancel_appointment(patient, id):
    appointment = Appointment.query.get_or_404(id)
    if appointment.patient_id != patient.id:
        flash('You do not have permission to cancel this appointment.', 'danger')
        return redirect(url_for('patient.dashboard'))

    if appointment.appointment_date <= datetime.now():
        flash('Cannot cancel past or current appointments.', 'warning')
        return redirect(url_for('patient.view_appointment', id=id))
    
    appointment.status = 'Cancelled'
    db.session.commit()
    flash('Appointment cancelled successfully.', 'success')
    return redirect(url_for('patient.dashboard'))

# --- Medical Records & Support ---
@patient_bp.route('/medical-history')
@profile_required
def medical_history(patient):
    past_appointments = Appointment.query.filter(
        Appointment.patient_id == patient.id,
        Appointment.appointment_date < datetime.now()
    ).order_by(Appointment.appointment_date.desc()).all()
    return render_template('patient/medical_history.html', patient=patient, past_appointments=past_appointments)

@patient_bp.route('/request-records', methods=['GET', 'POST'])
@profile_required
def request_records(patient):
    return render_template('patient/request_records.html', patient=patient)

@patient_bp.route('/contact-support', methods=['GET', 'POST'])
@profile_required
def contact_support(patient):
    if request.method == 'POST':
        flash('Your support request has been submitted. We will contact you shortly.', 'success')
        return redirect(url_for('patient.dashboard'))
    return render_template('patient/contact_support.html', patient=patient)

@patient_bp.route('/view-patient/<int:id>')
@login_required
def view_patient(id):
    patient = Patient.query.get_or_404(id)
    return render_template('patient/patient_view.html', patient=patient)