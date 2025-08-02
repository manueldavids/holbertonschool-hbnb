#!/usr/bin/env python3
"""
Script to initialize the database for HBnB application.
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import user, place, amenity, review

def init_database():
    """Initialize the database with all tables."""
    try:
        # Create Flask app
        app = create_app('development')
        
        # Create application context
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✅ Database initialized successfully!")
            print("📁 Database file: instance/hbnb_dev.db")
            
            # List all tables
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📋 Created tables: {', '.join(tables)}")
            
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🔧 Initializing HBnB Database...")
    print("=" * 40)
    
    # Ensure instance directory exists
    os.makedirs('instance', exist_ok=True)
    
    if init_database():
        print("=" * 40)
        print("🎉 Database initialization completed!")
    else:
        print("=" * 40)
        print("💥 Database initialization failed!")
        sys.exit(1) 