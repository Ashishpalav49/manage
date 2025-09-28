import os
import sys

# Add current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Doctor, Patient, Appointment

def create_database():
    app = create_app()

    # Ensure the instance directory exists
    instance_folder = 'instance'
    if not os.path.exists(instance_folder):
        os.makedirs(instance_folder)
        print(f"Created instance directory at: {instance_folder}")

    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database and tables created successfully.")

        # Check if admin already exists
        if not User.query.filter_by(email='admin@example.com').first():
            admin = User(username='admin', email='admin@example.com', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            print("Admin user created.")
        else:
            print("Admin user already exists. Skipping creation.")

        # Check if doctors already exist to avoid duplicates
        if not Doctor.query.first():
            doctors = [
                Doctor(first_name='John', last_name='Smith', specialization='Cardiology',
                       contact_number='555-1234', email='john.smith@hospital.com'),
                Doctor(first_name='Sarah', last_name='Johnson', specialization='Neurology',
                       contact_number='555-5678', email='sarah.johnson@hospital.com'),
                Doctor(first_name='Robert', last_name='Davis', specialization='Pediatrics',
                       contact_number='555-9876', email='robert.davis@hospital.com')
            ]
            db.session.add_all(doctors)
            print("Sample doctors added.")
        else:
            print("Doctors already exist. Skipping creation.")

        db.session.commit()

if __name__ == '__main__':
    create_database()
