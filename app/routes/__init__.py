# app/routes/__init__.py

from flask import Blueprint

# 1. Create all blueprints here
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
patient_bp = Blueprint('patient', __name__, url_prefix='/patient')
doctor_bp = Blueprint('doctor', __name__, url_prefix='/doctor') # <-- This line is crucial

# 2. Import the route files AFTER the blueprints are defined.
#    This connects the views to the blueprints.
from . import auth_routes
from . import admin_routes
from . import patient_routes
from . import doctor_routes