"""
Sample Data Generator for Nirmala Admission Portal
This script populates the database with sample student records for testing
"""

from app import app, db, Student, Staff
from werkzeug.security import generate_password_hash
import random

def create_sample_data():
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        Student.query.delete()
        db.session.commit()
        
        # Sample data
        first_names = [
            "Aarav", "Vivaan", "Aditya", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna",
            "Ishaan", "Shaurya", "Atharv", "Advaith", "Pranav", "Aryan", "Dhruv",
            "Aadhya", "Ananya", "Diya", "Ira", "Pari", "Saanvi", "Sara", "Shanaya",
            "Myra", "Aanya", "Navya", "Kiara", "Riya", "Aarohi", "Mira", "Priya",
            "Aisha", "Kavya", "Avni", "Nisha", "Sneha", "Tanvi", "Divya", "Meera"
        ]
        
        last_names = [
            "Sharma", "Patel", "Kumar", "Singh", "Reddy", "Nair", "Iyer", "Rao",
            "Joshi", "Verma", "Gupta", "Menon", "Pillai", "Krishnan", "Desai"
        ]
        
        cities = [
            "Coimbatore", "Chennai", "Bangalore", "Mumbai", "Delhi", "Hyderabad",
            "Pune", "Kochi", "Madurai", "Trichy", "Salem", "Tiruppur"
        ]
        
        courses = [
            "B.Sc Computer Science", "B.Sc Mathematics", "B.Sc Physics",
            "B.Sc Chemistry", "B.Com", "B.A English", "B.A Tamil", "BCA", "BBA"
        ]
        
        castes = ["SC", "ST", "OBC", "MBC", "BC", "General"]
        communities = ["Hindu", "Muslim", "Christian", "Sikh", "Jain"]
        
        print("Creating 50 sample students...")
        
        for i in range(50):
            name = f"{random.choice(first_names)} {random.choice(last_names)}"
            
            # Generate realistic marks
            tenth_marks = round(random.uniform(65, 98), 2)
            twelfth_marks = round(random.uniform(65, 98), 2)
            
            student = Student(
                application_id=f"NAP{i+1:05d}",
                name=name,
                email=f"student{i+1}@example.com",
                phone=f"98{random.randint(10000000, 99999999)}",
                dob=f"{random.randint(2003, 2006)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                gender=random.choice(["Male", "Female"]),
                tenth_marks=tenth_marks,
                twelfth_marks=twelfth_marks,
                caste=random.choice(castes),
                community=random.choice(communities),
                address=f"{random.randint(1, 999)} Main Street, {random.choice(['Anna Nagar', 'RS Puram', 'Gandhipuram', 'Saibaba Colony'])}",
                city=random.choice(cities),
                state="Tamil Nadu",
                pincode=f"{random.randint(600000, 699999)}",
                course=random.choice(courses),
                admission_status=random.choice(["Pending", "Pending", "Pending", "Approved", "Rejected"])
            )
            
            # Calculate merit score
            student.calculate_merit_score()
            
            db.session.add(student)
        
        db.session.commit()
        print("✓ Successfully created 50 sample students!")
        
        # Display some statistics
        print("\n=== Statistics ===")
        print(f"Total Students: {Student.query.count()}")
        print(f"Pending: {Student.query.filter_by(admission_status='Pending').count()}")
        print(f"Approved: {Student.query.filter_by(admission_status='Approved').count()}")
        print(f"Rejected: {Student.query.filter_by(admission_status='Rejected').count()}")
        
        # Top 5 students
        print("\n=== Top 5 Students by Merit ===")
        top_students = Student.query.order_by(Student.merit_score.desc()).limit(5).all()
        for idx, student in enumerate(top_students, 1):
            print(f"{idx}. {student.name} - {student.merit_score:.2f} ({student.course})")
        
        # Category-wise counts
        print("\n=== Category-wise Distribution ===")
        for caste in castes:
            count = Student.query.filter_by(caste=caste).count()
            print(f"{caste}: {count}")
        
        print("\n✓ Sample data generation completed!")

if __name__ == "__main__":
    create_sample_data()
