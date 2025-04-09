from app import db, app

def reset_database():
    with app.app_context():
        # Drop all tables
        db.drop_all()
        print("Dropped all tables.")
        
        # Create all tables with new schema
        db.create_all()
        print("Created all tables with new schema.")
        
        print("Database reset complete!")

if __name__ == '__main__':
    reset_database() 