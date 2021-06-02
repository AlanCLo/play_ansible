import os
os.environ['DATABASE_URI'] = 'postgresql:///postgres:admin123@postgres:5432/demo'

import sys
sys.path.insert(0, '/var/www/demo')

from app import app as application
