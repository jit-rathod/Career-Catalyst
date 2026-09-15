from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Optional

app = Flask(__name__)
app.config['SECRET_KEY'] = 'careercatalyst2026_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placement.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# ================= HARDCODED ADMIN CREDENTIALS =================
ADMIN_EMAIL = "admin@careercatalyst.com"
ADMIN_PASSWORD = "admin123"

# ================= MODELS =================
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(20))
    cgpa = db.Column(db.Float)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    role = db.Column(db.String(100))
    package = db.Column(db.String(50))
    min_cgpa = db.Column(db.Float)
    description = db.Column(db.Text, default="")
    location = db.Column(db.String(100), default="")
    website = db.Column(db.String(200), default="")

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    phone = db.Column(db.String(20))
    cover_letter = db.Column(db.Text)
    resume_link  = db.Column(db.String(200))
    # status: Pending | Scheduled | Placed | Rejected
    status = db.Column(db.String(30), default="Pending")

class Interview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'), unique=True)
    interview_date = db.Column(db.String(50))
    interview_time = db.Column(db.String(20))
    venue = db.Column(db.String(200))
    notes = db.Column(db.Text, default="")

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def create_admin():
    admin = User.query.filter_by(
        email="admin@careercatalyst.com"
    ).first()
    if not admin:
        admin = User(
            name="Admin",
            email="admin@careercatalyst.com",
            password=generate_password_hash("admin123"),
            role="admin",
            cgpa=None
        )
        db.session.add(admin)
        db.session.commit()

# ================= FORMS =================
# Register form — no role field, students only
class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    cgpa = FloatField("CGPA", validators=[Optional()])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class CompanyForm(FlaskForm):
    name = StringField("Company Name", validators=[DataRequired()])
    role = StringField("Job Role", validators=[DataRequired()])
    package = StringField("Package (e.g. 12 LPA)", validators=[DataRequired()])
    min_cgpa = FloatField("Minimum CGPA", validators=[DataRequired()])
    description = TextAreaField("Company Description",   validators=[Optional()])
    location = StringField("Location", validators=[Optional()])
    website = StringField("Website URL", validators=[Optional()])
    submit = SubmitField("Add Company")

class ApplicationForm(FlaskForm):
    phone        = StringField("Phone Number",                         validators=[DataRequired()])
    cover_letter = TextAreaField("Cover Letter",                       validators=[DataRequired()])
    resume_link  = StringField("Resume Link (Google Drive / LinkedIn)", validators=[Optional()])
    submit       = SubmitField("Submit Application")

class ScheduleInterviewForm(FlaskForm):
    interview_date = StringField("Interview Date (e.g. 2025-06-15)", validators=[DataRequired()])
    interview_time = StringField("Interview Time (e.g. 10:00 AM)", validators=[DataRequired()])
    venue = StringField("Venue / Mode (e.g. Online / Room 301)", validators=[DataRequired()])
    notes = TextAreaField("Additional Notes", validators=[Optional()])
    submit = SubmitField("Schedule Interview")

class UpdateStatusForm(FlaskForm):
    status = SelectField("Status", choices=[
        ("Pending",   "Pending"),
        ("Scheduled", "Scheduled for Interview"),
        ("Placed",    "Placed"),
        ("Rejected",  "Rejected"),
    ])
    submit = SubmitField("Update Status")

# ================= ROUTES =================

@app.route("/")
def index():
    top_companies = Company.query.limit(3).all()
    return render_template("index.html", top_companies=top_companies)

# -------- REGISTER (students only) --------
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing = User.query.filter_by(email=form.email.data).first()
        if existing:
            flash("Email already registered. Please login.", "error")
            return redirect(url_for("login"))
        user = User(
            name=form.name.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            cgpa=form.cgpa.data,
            role="student"          # always student from registration
        )
        db.session.add(user)
        db.session.commit()
        flash("Registered successfully!", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

# -------- LOGIN --------
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            email=form.email.data
        ).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            if user.role == "admin":
                flash("Welcome Admin!", "success")
            else:
                flash("Welcome back!", "success")
            return redirect(url_for("dashboard"))
        flash("Invalid email or password.", "error")
    return render_template("login.html", form=form)

# -------- DASHBOARD --------
@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.role == "admin":
        companies  = Company.query.all()
        form       = CompanyForm()
        total_apps = Application.query.count()
        students   = User.query.filter_by(role="student").order_by(User.name).all()

        # All applications with student + company info
        all_applications = []
        for appl in Application.query.all():
            student   = db.session.get(User, appl.student_id)
            company   = db.session.get(Company, appl.company_id)
            interview = Interview.query.filter_by(application_id=appl.id).first()
            if student and company:
                all_applications.append({
                    "application": appl,
                    "student":     student,
                    "company":     company,
                    "interview":   interview,
                })

        sched_form  = ScheduleInterviewForm()
        status_form = UpdateStatusForm()
        return render_template("admin_dashboard.html",
                               companies=companies,
                               form=form,
                               total_apps=total_apps,
                               students=students,
                               all_applications=all_applications,
                               sched_form=sched_form,
                               status_form=status_form)
    else:
        applied_ids = [a.company_id for a in Application.query.filter_by(student_id=current_user.id).all()]
        recommended = Company.query.filter(
            Company.min_cgpa <= (current_user.cgpa or 0)
        ).limit(3).all()
        applications = Application.query.filter_by(student_id=current_user.id).all()
        applied_companies = []
        for appl in applications:
            c         = db.session.get(Company, appl.company_id)
            interview = Interview.query.filter_by(application_id=appl.id).first()
            if c:
                applied_companies.append({
                    'company':   c,
                    'status':    appl.status,
                    'interview': interview,
                })
        return render_template("student_dashboard.html",
                               recommended=recommended,
                               applied_companies=applied_companies,
                               applied_ids=applied_ids)

# -------- COMPANIES LIST --------
@app.route("/companies", methods=["GET", "POST"])
@login_required
def companies():
    form = CompanyForm()
    if current_user.role == "admin" and form.validate_on_submit():
        company = Company(
            name=form.name.data,
            role=form.role.data,
            package=form.package.data,
            min_cgpa=form.min_cgpa.data,
            description=form.description.data or "",
            location=form.location.data or "",
            website=form.website.data or ""
        )
        db.session.add(company)
        db.session.commit()
        flash("Company added successfully!", "success")
        return redirect(url_for("companies"))

    applied_ids = []
    if current_user.role == "student":
        applied_ids = [a.company_id for a in Application.query.filter_by(student_id=current_user.id).all()]

    all_companies = Company.query.order_by(Company.min_cgpa).all()
    return render_template("companies.html", companies=all_companies, form=form, applied_ids=applied_ids)

# -------- COMPANY DETAIL --------
@app.route("/company/<int:id>")
@login_required
def company_detail(id):
    company = Company.query.get_or_404(id)
    form    = ApplicationForm()
    already_applied = False
    eligible        = False
    if current_user.role == "student":
        already_applied = Application.query.filter_by(
            student_id=current_user.id, company_id=id
        ).first() is not None
        eligible = (current_user.cgpa or 0) >= company.min_cgpa
    return render_template("company_detail.html", company=company, form=form,
                           already_applied=already_applied, eligible=eligible)

# -------- APPLY --------
@app.route("/apply/<int:id>", methods=["POST"])
@login_required
def apply(id):
    if current_user.role != "student":
        flash("Only students can apply.", "error")
        return redirect(url_for("companies"))

    company = Company.query.get_or_404(id)

    if (current_user.cgpa or 0) < company.min_cgpa:
        flash(f"You need a minimum CGPA of {company.min_cgpa} to apply.", "error")
        return redirect(url_for("company_detail", id=id))

    already_applied = Application.query.filter_by(student_id=current_user.id, company_id=id).first()
    if already_applied:
        flash("You have already applied to this company.", "error")
        return redirect(url_for("company_detail", id=id))

    form = ApplicationForm()
    if form.validate_on_submit():
        application = Application(
            student_id=current_user.id,
            company_id=id,
            phone=form.phone.data,
            cover_letter=form.cover_letter.data,
            resume_link=form.resume_link.data or ""
        )
        db.session.add(application)
        db.session.commit()
        flash("Application submitted successfully! 🎉", "success")
        return redirect(url_for("dashboard"))

    flash("Please fill all required fields.", "error")
    return redirect(url_for("company_detail", id=id))

# -------- ADMIN: UPDATE APPLICATION STATUS --------
@app.route("/admin/update_status/<int:app_id>", methods=["POST"])
@login_required
def update_status(app_id):
    if current_user.role != "admin":
        return redirect(url_for("dashboard"))
    application = Application.query.get_or_404(app_id)
    new_status  = request.form.get("status", "Pending")
    application.status = new_status
    db.session.commit()
    flash(f"Status updated to '{new_status}'.", "success")
    return redirect(url_for("dashboard"))

# -------- ADMIN: SCHEDULE INTERVIEW --------
@app.route("/admin/schedule_interview/<int:app_id>", methods=["POST"])
@login_required
def schedule_interview(app_id):
    if current_user.role != "admin":
        return redirect(url_for("dashboard"))
    application = Application.query.get_or_404(app_id)
    interview   = Interview.query.filter_by(application_id=app_id).first()
    if not interview:
        interview = Interview(application_id=app_id)
        db.session.add(interview)

    interview.interview_date = request.form.get("interview_date", "")
    interview.interview_time = request.form.get("interview_time", "")
    interview.venue          = request.form.get("venue", "")
    interview.notes          = request.form.get("notes", "")

    # Auto-update application status to Scheduled
    application.status = "Scheduled"
    db.session.commit()
    flash("Interview scheduled successfully! Student status updated to 'Scheduled'.", "success")
    return redirect(url_for("dashboard"))

# -------- RECOMMENDATIONS --------
@app.route("/recommendations")
@login_required
def recommendations():
    if current_user.role != "student":
        return redirect(url_for("dashboard"))
    applied_ids = [a.company_id for a in Application.query.filter_by(student_id=current_user.id).all()]
    recommended = Company.query.filter(
        Company.min_cgpa <= (current_user.cgpa or 0)
    ).all()
    return render_template("recommendations.html", recommended=recommended, applied_ids=applied_ids)

# -------- DELETE COMPANY --------
@app.route("/delete/<int:id>")
@login_required
def delete_company(id):
    if current_user.role != "admin":
        return redirect(url_for("dashboard"))
    company = db.session.get(Company, id)
    if company:
        # Delete associated interviews first
        for appl in Application.query.filter_by(company_id=id).all():
            Interview.query.filter_by(application_id=appl.id).delete()
        Application.query.filter_by(company_id=id).delete()
        db.session.delete(company)
        db.session.commit()
        flash("Company deleted.", "success")
    return redirect(url_for("companies"))

# -------- LOGOUT --------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("index"))

# ================= MAIN =================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_admin()

    app.run(debug=True)
