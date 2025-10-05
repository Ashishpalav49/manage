# Hospital Management System

A comprehensive web-based hospital management system built with Flask that allows efficient management of patients, doctors, and appointments with role-based access control.

## Features

### 🏥 Multi-Role System
- **Admin Panel**: Complete system management and oversight
- **Doctor Dashboard**: Appointment management and patient consultation
- **Patient Portal**: Profile management and appointment booking

### 👨‍⚕️ Doctor Management
- Add, edit, and manage doctor profiles
- Specialization tracking
- Availability status management
- User account linking for doctors

### 👤 Patient Management
- Patient registration and profile management
- Medical history tracking
- Contact information and personal details
- Age calculation and profile viewing

### 📅 Appointment System
- Online appointment booking with date/time validation
- Doctor-patient appointment matching
- Appointment status tracking (Scheduled, Completed, Cancelled)
- Doctor notes and appointment history

### 🔐 Authentication & Security
- Secure user authentication with Flask-Login
- Role-based access control (Admin, Doctor, Patient)
- Password hashing with Werkzeug
- Session management

### 📊 Admin Features
- Dashboard with system statistics
- Complete CRUD operations for all entities
- Appointment oversight and management
- System reports and analytics

## Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Forms**: Flask-WTF with WTForms validation
- **Authentication**: Flask-Login
- **Security**: Werkzeug password hashing

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd manage
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv hospital_env
   
   # On Windows
   hospital_env\Scripts\activate
   
   # On macOS/Linux
   source hospital_env/bin/activate
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```bash
   python setup_db.py
   ```
   This will create the SQLite database and initial admin user.

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Access the application**
   Open your web browser and navigate to: `http://localhost:5000`

## Default Login Credentials

After running `setup_db.py`, you can log in with:
- **Username**: admin
- **Password**: admin123
- **Role**: Administrator

## Project Structure

```
manage/
├── app/
│   ├── routes/
│   │   ├── __init__.py          # Blueprint registration
│   │   ├── auth_routes.py       # Authentication routes
│   │   ├── admin_routes.py      # Admin management routes
│   │   ├── doctor_routes.py     # Doctor dashboard routes
│   │   ├── patient_routes.py    # Patient portal routes
│   │   └── forms.py            # Additional form definitions
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css       # Custom styles
│   │   └── js/
│   │       └── main.js         # JavaScript functionality
│   ├── templates/
│   │   ├── admin/              # Admin panel templates
│   │   ├── auth/               # Authentication templates
│   │   ├── doctor/             # Doctor dashboard templates
│   │   ├── patient/            # Patient portal templates
│   │   └── base.html           # Base template
│   ├── __init__.py             # Flask app factory
│   ├── config.py               # Configuration settings
│   ├── forms.py                # WTForms form definitions
│   └── models.py               # Database models
├── config.py                   # Main configuration
├── run.py                      # Application entry point
├── setup_db.py                 # Database setup script
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## Database Models

### User
- Base user authentication
- Role-based access (admin, doctor, patient)
- Linked to Doctor or Patient profiles

### Doctor
- Personal information and specialization
- Availability status
- Linked to user account
- Appointment relationships

### Patient
- Complete patient profile
- Medical information (blood group, DOB)
- Contact details and address
- Appointment history

### Appointment
- Doctor-patient appointment linking
- Date/time scheduling with validation
- Status tracking and notes
- Booking timestamps

## API Routes

### Authentication (`/auth`)
- `/login` - User login
- `/register` - New user registration
- `/logout` - User logout

### Admin Panel (`/admin`)
- `/dashboard` - Admin overview
- `/doctors` - Doctor management
- `/patients` - Patient management
- `/appointments` - Appointment oversight

### Doctor Dashboard (`/doctor`)
- `/dashboard` - Doctor overview
- `/appointments` - Appointment management

### Patient Portal (`/patient`)
- `/dashboard` - Patient overview
- `/book-appointment` - Appointment booking
- `/profile` - Profile management

## Features in Detail

### Appointment Booking
- **Time Validation**: Only future appointments allowed
- **Business Hours**: 8 AM - 6 PM, weekdays only
- **24-hour Notice**: Minimum advance booking time
- **Doctor Availability**: Only available doctors shown

### Form Validation
- **Email Validation**: Proper email format checking
- **Password Security**: Secure password hashing
- **Data Integrity**: Comprehensive field validation
- **User Experience**: Clear error messaging

### Security Features
- **Session Management**: Secure user sessions
- **Role-based Access**: Route protection by user role
- **Password Hashing**: Werkzeug security
- **CSRF Protection**: Flask-WTF CSRF tokens

## Configuration

### Environment Variables
- `SECRET_KEY`: Flask secret key for sessions
- `DATABASE_URL`: Database connection string

### Default Configuration
- **Database**: SQLite (`instance/hospital.db`)
- **Debug Mode**: Enabled in development
- **Session Security**: Random secret key generation

## Development

### Adding New Features
1. Create/modify models in `app/models.py`
2. Create forms in `app/forms.py`
3. Add routes in appropriate route files
4. Create/update templates
5. Update database if needed

### Database Migrations
For schema changes, you may need to:
1. Delete the existing database file
2. Run `python setup_db.py` again
3. Or implement proper migration scripts

## Troubleshooting

### Common Issues

**Database not found**: Run `python setup_db.py`

**Import errors**: Ensure all requirements are installed with `pip install -r requirements.txt`

**Permission denied**: Make sure you're in the correct directory and have proper permissions

**Port already in use**: Change the port in `run.py` or stop the conflicting service

### Debug Mode
The application runs in debug mode by default, which provides:
- Detailed error messages
- Automatic reloading on code changes
- Interactive debugger in browser

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is developed for educational and healthcare management purposes.

## Support

For questions or issues:
1. Check the troubleshooting section
2. Review the code documentation
3. Ensure all dependencies are properly installed
4. Verify database setup is complete

---

**Note**: This system is designed for educational purposes and should be properly secured and tested before use in a production healthcare environment.