from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3
import os
from functools import wraps
from flask import session, redirect, url_for, flash
app = Flask(__name__)
app.config['SECRET_KEY'] = 'nirmala-admission-portal-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admission.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
from flask import make_response
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'staff_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
@app.route("/download_pdf")

@login_required
def download_pdf():

    students = Student.query.order_by(Student.cutoff_score.desc()).all()

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4

    # TITLE
    p.setFont("Helvetica-Bold", 16)
    p.drawString(220, height - 50, "MERIT LIST")

    # HEADER
    p.setFont("Helvetica-Bold", 10)
    y = height - 100

    p.drawString(50, y, "Rank")
    p.drawString(100, y, "Name")
    p.drawString(280, y, "Course")
    p.drawString(420, y, "Cutoff")

    p.line(50, y - 5, 550, y - 5)

    y -= 25
    p.setFont("Helvetica", 10)

    for i, s in enumerate(students, 1):

        if y < 60:
            p.showPage()
            y = height - 100

            p.setFont("Helvetica-Bold", 10)
            p.drawString(50, y, "Rank")
            p.drawString(100, y, "Name")
            p.drawString(280, y, "Course")
            p.drawString(420, y, "Cutoff")
            p.line(50, y - 5, 550, y - 5)

            y -= 25
            p.setFont("Helvetica", 10)

        p.drawString(50, y, str(i))
        p.drawString(100, y, str(s.name)[:25])
        p.drawString(280, y, str(s.course)[:20])
        p.drawString(420, y, str(s.cutoff_score))

        y -= 18

    p.save()
    buffer.seek(0)

    response = make_response(buffer.read())
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=merit_list.pdf"

    return response
# ── Cutoff Formulas ────────────────────────────────────────────────────────────
CUTOFF_FORMULAS = {
    'B.Sc Mathematics':      {'maths': 50, 'physics': 25, 'chemistry': 25},
    'B.Sc Chemistry':  {'chemistry': 50, 'maths': 25, 'biology': 25},
    'B.Sc Botany':     {'biology': 50, 'chemistry': 50},
    'B.Sc Zoology':    {'biology': 50, 'chemistry': 50},
    'B.Sc Physics':    {'physics': 50, 'maths': 25, 'chemistry': 25},
    'B.Com':   {'commerce': 37.5, 'accountancy': 37.5, 'maths': 25},
    'B.Sc Geography':  {'geography': 50},
    'B.A History':    {'history': 50, 'geography': 50},
    'B.A Economics':  {'economics': 50, 'history': 25, 'maths': 25},
}
COURSE_SUBJECTS = {
    'B.Sc Mathematics':      ['maths', 'physics', 'chemistry'],
    'B.Sc Chemistry':  ['chemistry', 'maths', 'biology'],
    'B.Sc Botany':     ['biology', 'chemistry'],
    'B.Sc Zoology':    ['biology', 'chemistry'],
    'B.Sc Physics':    ['physics', 'maths', 'chemistry'],
    'B.Com':   ['commerce', 'accountancy', 'maths'],
    'B.Sc Geography':  ['geography'],
    'B.A History':    ['history', 'geography'],
    'B.A Economics':  ['economics', 'history', 'maths'],
}
SUBJECT_LABELS = {
    'maths':       'Mathematics',
    'physics':     'Physics',
    'chemistry':   'Chemistry',
    'biology':     'Biology',
    'commerce':    'Commerce',
    'accountancy': 'Accountancy',
    'history':     'History',
    'geography':   'Geography',
    'economics':   'Economics',
}
# ── Models ─────────────────────────────────────────────────────────────────────
class Staff(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name     = db.Column(db.String(100), nullable=False)
    email    = db.Column(db.String(100), unique=True, nullable=False)
class Student(db.Model):
    id             = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.String(20), unique=True, nullable=False)
    name           = db.Column(db.String(100), nullable=False)
    email          = db.Column(db.String(100), nullable=False)
    phone          = db.Column(db.String(15),  nullable=False)
    dob            = db.Column(db.String(10),  nullable=False)
    gender         = db.Column(db.String(10),  nullable=False) 
    twelfth_marks = db.Column(db.Float, nullable=False)
    # 12th Subject Marks (for cutoff calculation)
    maths_marks       = db.Column(db.Float, nullable=True)
    physics_marks     = db.Column(db.Float, nullable=True)
    chemistry_marks   = db.Column(db.Float, nullable=True)
    biology_marks     = db.Column(db.Float, nullable=True)
    commerce_marks    = db.Column(db.Float, nullable=True)
    accountancy_marks = db.Column(db.Float, nullable=True)
    history_marks     = db.Column(db.Float, nullable=True)
    geography_marks   = db.Column(db.Float, nullable=True)
    economics_marks   = db.Column(db.Float, nullable=True)

    religion  = db.Column(db.String(50), nullable=False)
    community = db.Column(db.String(50), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    rc = db.Column(db.String(10))

    merit_score  = db.Column(db.Float, nullable=False)
    cutoff_score = db.Column(db.Float, nullable=True)

    admission_status = db.Column(db.String(20), default='Pending')
    created_at       = db.Column(db.DateTime,   default=db.func.current_timestamp())
    def calculate_merit_score(self):
      self.merit_score = self.twelfth_marks
      return self.merit_score
    def calculate_cutoff_score(self):
        formula = CUTOFF_FORMULAS.get(self.course)
        if not formula:
            self.cutoff_score = None
            return None
        subject_map = {
            'maths':       self.maths_marks,
            'physics':     self.physics_marks,
            'chemistry':   self.chemistry_marks,
            'biology':     self.biology_marks,
            'commerce':    self.commerce_marks,
            'accountancy': self.accountancy_marks,
            'history':     self.history_marks,
            'geography':   self.geography_marks,
            'economics':   self.economics_marks,
        }
        total = 0.0
        for subject, weight in formula.items():
            mark = subject_map.get(subject)
            if mark is None:
                self.cutoff_score = None
                return None
            total += (mark * weight) / 100.0
        self.cutoff_score = round(total, 2)
        return self.cutoff_score
# ── Helpers ────────────────────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'staff_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
def _get_subject(form, name):
    val = form.get(f'{name}_marks')
    return float(val) if val and val.strip() != '' else None
# ── Routes ─────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        staff = Staff.query.filter_by(username=username).first()
        if staff and check_password_hash(staff.password, password):
            session['staff_id'] = staff.id
            session['staff_name'] = staff.name
            flash(f'Welcome {staff.name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'danger')
    return render_template('login.html')
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))
@app.route('/dashboard')
@login_required
def dashboard():
    total_students      = Student.query.count()
    pending_admissions  = Student.query.filter_by(admission_status='Pending').count()
    approved_admissions = Student.query.filter_by(admission_status='Approved').count()
    rejected_admissions = Student.query.filter_by(admission_status='Rejected').count()
    recent_students     = Student.query.order_by(Student.created_at.desc()).limit(5).all()
    return render_template('dashboard.html',
                           total_students=total_students,
                           pending_admissions=pending_admissions,
                           approved_admissions=approved_admissions,
                           rejected_admissions=rejected_admissions,
                           recent_students=recent_students)
@app.route('/students')
@login_required
def students():
    religion_filter  = request.args.get('religion', '')
    community_filter = request.args.get('community', '')
    status_filter    = request.args.get('status', '')
    course_filter    = request.args.get('course', '')
    rc               = request.args.get('rc', '') 
    sort_by          = request.args.get('sort_by', 'cutoff_score')
    order            = request.args.get('order', 'desc')
    query = Student.query
    if religion_filter:
        query = query.filter_by(religion=religion_filter)
    if community_filter:
        query = query.filter_by(community=community_filter)
    if status_filter:
        query = query.filter_by(admission_status=status_filter)
    if course_filter:
        query = query.filter_by(course=course_filter)
    if rc:
        query = query.filter(Student.rc == rc)
    col_map = {
        'cutoff_score': Student.cutoff_score,
        'merit_score':  Student.merit_score,
        'name':         Student.name,
        'date':         Student.created_at,
    }
    col = col_map.get(sort_by, Student.cutoff_score)
    query = query.order_by(col.desc() if order == 'desc' else col.asc())
    students_list = query.all()
    religions   = [r[0] for r in db.session.query(Student.religion).distinct().all()]
    communities = [c[0] for c in db.session.query(Student.community).distinct().all()]
    courses     = [c[0] for c in db.session.query(Student.course).distinct().all()]
    return render_template(
        'students.html',
        students=students_list,
        religions=religions,
        communities=communities,
        courses=courses,
        rc=rc,
        current_filters={
            'religion': religion_filter,
            'community': community_filter,
            'status': status_filter,
            'course': course_filter,
            'sort_by': sort_by,
            'order': order,
            'rc': rc
        }
    )
@app.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        try:
            # Auto-generate-ஐ நீக்கி, form-ல் இருந்து பெறவும்
            app_id = request.form.get('application_id', '').strip()
            # Validation
            if not app_id:
                flash('Application ID கொடுக்கவும்!', 'danger')
                return render_template('add_student.html',
                                       course_subjects=COURSE_SUBJECTS,
                                       cutoff_formulas=CUTOFF_FORMULAS,
                                       subject_labels=SUBJECT_LABELS)
            # Duplicate check
            existing = Student.query.filter_by(application_id=app_id).first()
            if existing:
                flash(f'Application ID "{app_id}" ஏற்கனவே பதிவு செய்யப்பட்டுள்ளது!', 'warning')
                return render_template('add_student.html',
                                       course_subjects=COURSE_SUBJECTS,
                                       cutoff_formulas=CUTOFF_FORMULAS,
                                       subject_labels=SUBJECT_LABELS)
            student = Student(
                application_id=app_id,  # ← form value use ஆகும்
                name=request.form.get('name'),
                email=request.form.get('email'),
                phone=request.form.get('phone'),
                dob=request.form.get('dob'),
                gender=request.form.get('gender'),
                twelfth_marks=float(request.form.get('twelfth_marks')),
                maths_marks=_get_subject(request.form, 'maths'),
                physics_marks=_get_subject(request.form, 'physics'),
                chemistry_marks=_get_subject(request.form, 'chemistry'),
                biology_marks=_get_subject(request.form, 'biology'),
                commerce_marks=_get_subject(request.form, 'commerce'),
                accountancy_marks=_get_subject(request.form, 'accountancy'),
                history_marks=_get_subject(request.form, 'history'),
                geography_marks=_get_subject(request.form, 'geography'),
                economics_marks=_get_subject(request.form, 'economics'),
                religion=request.form.get('religion'),
                community=request.form.get('community'),
                course=request.form.get('course'),
                rc=request.form.get('rc'),
                merit_score=0,
            )
            student.calculate_merit_score()
            student.calculate_cutoff_score()
            db.session.add(student)
            db.session.commit()
            flash(f'Student {student.name} added! Application ID: {app_id}', 'success')
            return redirect(url_for('students'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding student: {str(e)}', 'danger')
    return render_template('add_student.html',
                           course_subjects=COURSE_SUBJECTS,
                           cutoff_formulas=CUTOFF_FORMULAS,
                           subject_labels=SUBJECT_LABELS)
@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        try:
            student.name          = request.form.get('name')
            student.email         = request.form.get('email')
            student.phone         = request.form.get('phone')
            student.dob           = request.form.get('dob')
            student.gender        = request.form.get('gender')
            student.twelfth_marks = float(request.form.get('twelfth_marks'))
            student.maths_marks       = _get_subject(request.form, 'maths')
            student.physics_marks     = _get_subject(request.form, 'physics')
            student.chemistry_marks   = _get_subject(request.form, 'chemistry')
            student.biology_marks     = _get_subject(request.form, 'biology')
            student.commerce_marks    = _get_subject(request.form, 'commerce')
            student.accountancy_marks = _get_subject(request.form, 'accountancy')
            student.history_marks     = _get_subject(request.form, 'history')
            student.geography_marks   = _get_subject(request.form, 'geography')
            student.economics_marks   = _get_subject(request.form, 'economics')
            student.religion = request.form.get('religion')
            student.community = request.form.get('community')
            student.course    = request.form.get('course')
            student.calculate_merit_score()
            student.calculate_cutoff_score()
            db.session.commit()
            flash(f'Student {student.name} updated successfully!', 'success')
            return redirect(url_for('students'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating student: {str(e)}', 'danger')
    return render_template('edit_student.html',
                           student=student,
                           course_subjects=COURSE_SUBJECTS,
                           cutoff_formulas=CUTOFF_FORMULAS,
                           subject_labels=SUBJECT_LABELS)
@app.route('/delete_student/<int:id>')
@login_required
def delete_student(id):
    student = Student.query.get_or_404(id)
    try:
        db.session.delete(student)
        db.session.commit()
        flash(f'Student {student.name} deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting student: {str(e)}', 'danger')
    return redirect(url_for('students'))
@app.route('/view_student/<int:id>')
@login_required
def view_student(id):
    student = Student.query.get_or_404(id)
    formula = CUTOFF_FORMULAS.get(student.course, {})
    return render_template('view_student.html',
                           student=student,
                           formula=formula,
                           subject_labels=SUBJECT_LABELS)
@app.route('/update_admission_status/<int:id>/<status>')
@login_required
def update_admission_status(id, status):
    student = Student.query.get_or_404(id)
    if status in ['Approved', 'Rejected', 'Pending']:
        student.admission_status = status
        db.session.commit()
        flash(f'Admission status for {student.name} updated to {status}!', 'success')
    else:
        flash('Invalid status!', 'danger')
    return redirect(url_for('students'))
@app.route('/merit_list')
@login_required
def merit_list():
    religion_filter  = request.args.get('religion', '')
    community_filter = request.args.get('community', '')
    course_filter    = request.args.get('course', '')
    rank_by          = request.args.get('rank_by', 'cutoff_score')
    rc = request.args.get('rc','')
    query = Student.query
    if religion_filter:
        query = query.filter_by(religion=religion_filter)
    if community_filter:
        query = query.filter_by(community=community_filter)
    if course_filter:
        query = query.filter_by(course=course_filter)
    if rc:
        query = query.filter(Student.rc == rc)
    if rank_by == 'cutoff_score':
        students_list = query.order_by(Student.cutoff_score.desc()).all()
    else:
        students_list = query.order_by(Student.merit_score.desc()).all()
    for rank, student in enumerate(students_list, 1):
        student.rank = rank
    religions   = [r[0] for r in db.session.query(Student.religion).distinct().all()]
    communities = [c[0] for c in db.session.query(Student.community).distinct().all()]
    courses     = [c[0] for c in db.session.query(Student.course).distinct().all()]
    
    return render_template(
        'merit_list.html',
        students=students_list,
        religions=religions,
        communities=communities,
        courses=courses,
        cutoff_formulas=CUTOFF_FORMULAS,
        current_filters={
            'religion': religion_filter,
            'community': community_filter,
            'course': course_filter,
            'rc':rc,
            'rank_by': rank_by
        }
    )
@app.route('/cutoff_list')
@login_required
def cutoff_list():
    religion_filter  = request.args.get('religion', '')
    community_filter = request.args.get('community', '')
    course_filter    = request.args.get('course', '')
    rc = request.args.get('rc', '')
    query = Student.query
    if religion_filter:
        query = query.filter_by(religion=religion_filter)
    if community_filter:
        query = query.filter_by(community=community_filter)
    if course_filter:
        query = query.filter_by(course=course_filter)
    if rc:
        query = query.filter(Student.rc == rc)
    students_list = query.order_by(Student.cutoff_score.desc()).all()
    for rank, s in enumerate(students_list, 1):
        s.rank = rank
    religions   = [r[0] for r in db.session.query(Student.religion).distinct().all()]
    communities = [c[0] for c in db.session.query(Student.community).distinct().all()]
    courses     = [c[0] for c in db.session.query(Student.course).distinct().all()]
    return render_template(
        'cutoff_list.html',
        students=students_list,
        religions=religions,
        communities=communities,
        courses=courses,
        cutoff_formulas=CUTOFF_FORMULAS,
        subject_labels=SUBJECT_LABELS,
        current_filters={
            'religion': religion_filter,
            'community': community_filter,
            'course': course_filter,
            "rc": rc
        }
    )
# ── DB Init + Auto-Migration ───────────────────────────────────────────────────
def migrate_existing_db():
    """Add new columns to existing DB without losing data."""
    NEW_COLUMNS = [
        ('maths_marks',       'FLOAT'),
        ('physics_marks',     'FLOAT'),
        ('chemistry_marks',   'FLOAT'),
        ('biology_marks',     'FLOAT'),
        ('commerce_marks',    'FLOAT'),
        ('accountancy_marks', 'FLOAT'),
        ('history_marks',     'FLOAT'),
        ('geography_marks',   'FLOAT'),
        ('economics_marks',   'FLOAT'),
        ('cutoff_score',      'FLOAT'),
        ('rc','TEXT')
    ]
    # Flask puts the DB inside the 'instance' folder
    db_path = os.path.join(app.instance_path, 'admission.db')

    if not os.path.exists(db_path):
        return  # Fresh install — create_all() will handle it

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(student)")
    existing_cols = {row[1] for row in cursor.fetchall()}

    for col_name, col_type in NEW_COLUMNS:
        if col_name not in existing_cols:
            cursor.execute(f"ALTER TABLE student ADD COLUMN {col_name} {col_type}")
            print(f"[Migration] Added column: {col_name}")
    conn.commit()
    conn.close()
def init_db():
    with app.app_context():
        migrate_existing_db()   # Add missing columns to existing DB first
        db.create_all()         # Create tables if they don't exist yet
        if not Staff.query.filter_by(username='admin').first():
            default_staff = Staff(
                username='admin',
                password=generate_password_hash('admin123'),
                name='Admin',
                email='admin@nirmala.edu'
            )
            db.session.add(default_staff)
            db.session.commit()
            print("Default admin created: username=admin, password=admin123")
if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)