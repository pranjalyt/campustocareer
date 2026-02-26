"""
Campus to Career — Flask App
Run:  python app.py
"""
import os, hashlib
from datetime import date, datetime, timedelta
from functools import wraps
from werkzeug.utils import secure_filename
from flask import (Flask, render_template, request, redirect,
                   url_for, session, flash, g)
from db import get_db

app = Flask(__name__)
app.secret_key = 'campus2career_secret_2024'

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
ALLOWED_IMG  = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_DOC  = {'pdf', 'doc', 'docx'}
try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
except Exception:
    pass

# ─────────────── helpers ───────────────
def md5(text):
    return hashlib.md5(text.encode()).hexdigest()

def allowed_file(filename, kind='img'):
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    return ext in (ALLOWED_IMG if kind == 'img' else ALLOWED_DOC)

def save_file(file, kind='img'):
    if file and file.filename and allowed_file(file.filename, kind):
        fname = secure_filename(file.filename)
        path  = os.path.join(UPLOAD_FOLDER, fname)
        file.save(path)
        return fname
    return None

# ─────────────── auth guards ───────────────
def user_required(f):
    @wraps(f)
    def decorated(*a, **kw):
        if not session.get('user_id'):
            return redirect(url_for('user_login'))
        return f(*a, **kw)
    return decorated

def company_required(f):
    @wraps(f)
    def decorated(*a, **kw):
        if not session.get('company_id'):
            return redirect(url_for('company_login'))
        return f(*a, **kw)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*a, **kw):
        if not session.get('admin_id'):
            return redirect(url_for('admin_login'))
        return f(*a, **kw)
    return decorated

# ══════════════════════════════════════════
#           PUBLIC ROUTES
# ══════════════════════════════════════════

@app.route('/')
def home():
    db   = get_db()
    kw   = request.args.get('keyword', '').strip()
    loc  = request.args.get('location', '').strip()
    sql  = """SELECT v.*, c.CompanyName FROM tblvacancy v
              JOIN tblcompany c ON c.ID = v.CompanyID WHERE 1=1"""
    params = []
    if kw:
        sql += " AND v.JobTitle LIKE ?"
        params.append(f'%{kw}%')
    if loc:
        sql += " AND v.JobLocation LIKE ?"
        params.append(f'%{loc}%')
    sql += " ORDER BY v.ID DESC LIMIT 6"
    jobs = db.execute(sql, params).fetchall()
    
    fallback = False
    if not jobs and (kw or loc):
        fallback = True
        jobs = db.execute("""SELECT v.*, c.CompanyName FROM tblvacancy v 
                             JOIN tblcompany c ON c.ID = v.CompanyID 
                             ORDER BY v.ID DESC LIMIT 6""").fetchall()
                             
    return render_template('index.html', jobs=jobs, keyword=kw, location=loc, fallback=fallback)
@app.route('/about')
def about():
    db  = get_db()
    row = db.execute("SELECT * FROM tblpage WHERE PageType='aboutus'").fetchone()
    return render_template('about.html', page=row)

@app.route('/contact', methods=['GET','POST'])
def contact():
    db  = get_db()
    row = db.execute("SELECT * FROM tblpage WHERE PageType='contactus'").fetchone()
    if request.method == 'POST':
        flash('Thank you for contacting us. We will get back to you soon!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', page=row)

@app.route('/jobs')
def jobs_listed():
    db   = get_db()
    kw   = request.args.get('keyword', '').strip()
    loc  = request.args.get('location', '').strip()
    sql  = """SELECT v.*, c.CompanyName FROM tblvacancy v
              JOIN tblcompany c ON c.ID = v.CompanyID WHERE 1=1"""
    params = []
    if kw:
        sql += " AND v.JobTitle LIKE ?"
        params.append(f'%{kw}%')
    if loc:
        sql += " AND v.JobLocation LIKE ?"
        params.append(f'%{loc}%')
    sql += " ORDER BY v.ID DESC"
    jobs = db.execute(sql, params).fetchall()
    
    fallback = False
    if not jobs and (kw or loc):
        fallback = True
        jobs = db.execute("""SELECT v.*, c.CompanyName FROM tblvacancy v 
                             JOIN tblcompany c ON c.ID = v.CompanyID 
                             ORDER BY v.ID DESC""").fetchall()

    return render_template('jobs.html', jobs=jobs, keyword=kw, location=loc, fallback=fallback)
@app.route('/job/<int:job_id>')
def job_detail(job_id):
    db  = get_db()
    job = db.execute("""SELECT v.*, c.CompanyName, c.CompanyUrl, c.CompanyAddress, c.MobileNumber as CompMobile
                        FROM tblvacancy v JOIN tblcompany c ON c.ID=v.CompanyID
                        WHERE v.ID=?""", (job_id,)).fetchone()
    if not job:
        flash('Job not found.', 'danger')
        return redirect(url_for('jobs_listed'))
    return render_template('job_detail.html', job=job)


# ══════════════════════════════════════════
#           USER PORTAL
# ══════════════════════════════════════════

@app.route('/user/login', methods=['GET','POST'])
def user_login():
    if session.get('user_id'):
        return redirect(url_for('user_dashboard'))
    if request.method == 'POST':
        email = request.form['email'].strip()
        pwd   = md5(request.form['password'])
        db    = get_db()
        user  = db.execute("SELECT * FROM tbluser WHERE Email=? AND Password=?",
                           (email, pwd)).fetchone()
        if user:
            session['user_id']   = user['ID']
            session['user_name'] = user['FullName']
            flash(f"Welcome back, {user['FullName']}!", 'success')
            return redirect(url_for('user_dashboard'))
        flash('Invalid email or password.', 'danger')
    return render_template('user/login.html')

@app.route('/user/register', methods=['GET','POST'])
def user_register():
    if request.method == 'POST':
        db = get_db()
        fullname  = request.form['fullname'].strip()
        email     = request.form['email'].strip()
        mobile    = request.form['mobile'].strip()
        studentid = request.form['studentid'].strip()
        gender    = request.form['gender']
        password  = md5(request.form['password'])
        exists = db.execute("SELECT ID FROM tbluser WHERE Email=?", (email,)).fetchone()
        if exists:
            flash('Email already registered.', 'warning')
        else:
            db.execute("""INSERT INTO tbluser (FullName,Email,MobileNumber,StudentID,Gender,Password)
                          VALUES (?,?,?,?,?,?)""",
                       (fullname, email, mobile, studentid, gender, password))
            db.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('user_login'))
    return render_template('user/register.html')

@app.route('/user/logout')
def user_logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    return redirect(url_for('home'))

@app.route('/user/forgot-password', methods=['GET','POST'])
def user_forgot():
    if request.method == 'POST':
        db    = get_db()
        email = request.form['email'].strip()
        user  = db.execute("SELECT * FROM tbluser WHERE Email=?", (email,)).fetchone()
        if user:
            pwd_hash = hashlib.md5("12345".encode()).hexdigest()
            db.execute("UPDATE tbluser SET Password=? WHERE Email=?", (pwd_hash, email))
            db.commit()
            flash(f'Your password has been successfully reset to: 12345', 'success')
            return redirect(url_for('user_login'))
        else:
            flash('No account found with that email.', 'danger')
    return render_template('user/forgot_password.html')

@app.route('/user/dashboard')
@user_required
def user_dashboard():
    db  = get_db()
    uid = session['user_id']
    total_vacancies   = db.execute("SELECT COUNT(*) FROM tblvacancy").fetchone()[0]
    total_applied     = db.execute("SELECT COUNT(*) FROM tblapplyjob WHERE UserId=?", (uid,)).fetchone()[0]
    today_applied     = db.execute("SELECT COUNT(*) FROM tblapplyjob WHERE UserId=? AND date(ApplyDate)=date('now')", (uid,)).fetchone()[0]
    yesterday_applied = db.execute("SELECT COUNT(*) FROM tblapplyjob WHERE UserId=? AND date(ApplyDate)=date('now','-1 day')", (uid,)).fetchone()[0]
    week_applied      = db.execute("SELECT COUNT(*) FROM tblapplyjob WHERE UserId=? AND date(ApplyDate)>=date('now','-7 days')", (uid,)).fetchone()[0]
    return render_template('user/dashboard.html',
        total_vacancies=total_vacancies,
        total_applied=total_applied,
        today_applied=today_applied,
        yesterday_applied=yesterday_applied,
        week_applied=week_applied)

@app.route('/user/profile', methods=['GET','POST'])
@user_required
def user_profile():
    db  = get_db()
    uid = session['user_id']
    if request.method == 'POST':
        fullname = request.form['fullname'].strip()
        mobile   = request.form['mobile'].strip()
        gender   = request.form['gender']
        dob      = request.form['dob']
        address  = request.form['address'].strip()
        img_file = request.files.get('image')
        img_name = save_file(img_file, 'img')
        if img_name:
            db.execute("UPDATE tbluser SET FullName=?,MobileNumber=?,Gender=?,DOB=?,Address=?,Image=? WHERE ID=?",
                       (fullname,mobile,gender,dob,address,img_name,uid))
        else:
            db.execute("UPDATE tbluser SET FullName=?,MobileNumber=?,Gender=?,DOB=?,Address=? WHERE ID=?",
                       (fullname,mobile,gender,dob,address,uid))
        db.commit()
        session['user_name'] = fullname
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('user_profile'))
    user = db.execute("SELECT * FROM tbluser WHERE ID=?", (uid,)).fetchone()
    return render_template('user/profile.html', user=user)

@app.route('/user/change-password', methods=['GET','POST'])
@user_required
def user_change_password():
    db  = get_db()
    uid = session['user_id']
    if request.method == 'POST':
        old = md5(request.form['old_password'])
        new = request.form['new_password']
        cnf = request.form['confirm_password']
        user = db.execute("SELECT * FROM tbluser WHERE ID=? AND Password=?", (uid, old)).fetchone()
        if not user:
            flash('Current password is incorrect.', 'danger')
        elif new != cnf:
            flash('New passwords do not match.', 'danger')
        else:
            db.execute("UPDATE tbluser SET Password=? WHERE ID=?", (md5(new), uid))
            db.commit()
            flash('Password changed successfully.', 'success')
    return render_template('user/change_password.html')

@app.route('/user/education')
@user_required
def user_education():
    db  = get_db()
    uid = session['user_id']
    edu = db.execute("SELECT * FROM tbleducation WHERE UserID=?", (uid,)).fetchone()
    return render_template('user/education.html', edu=edu)

@app.route('/user/add-education', methods=['GET','POST'])
@user_required
def user_add_education():
    db  = get_db()
    uid = session['user_id']
    existing = db.execute("SELECT ID FROM tbleducation WHERE UserID=?", (uid,)).fetchone()
    if existing:
        flash('Education details already exist. Use edit.', 'info')
        return redirect(url_for('user_education'))
    if request.method == 'POST':
        f = request.form
        db.execute("""INSERT INTO tbleducation
            (UserID,SecondaryBoard,SecondaryBoardyop,SecondaryBoardper,SecondaryBoardcgpa,
             SSecondaryBoard,SSecondaryBoardyop,SSecondaryBoardper,SSecondaryBoardcgpa,
             GraUni,GraUniyop,GraUnidper,GraUnicgpa,
             PGUni,PGUniyop,PGUniper,PGUnicgpa,ExtraCurriculars,OtherAchivement)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (uid, f.get('sec_board'), f.get('sec_yop'), f.get('sec_per'), f.get('sec_cgpa'),
             f.get('ssec_board'), f.get('ssec_yop'), f.get('ssec_per'), f.get('ssec_cgpa'),
             f.get('gra_uni'), f.get('gra_yop'), f.get('gra_per'), f.get('gra_cgpa'),
             f.get('pg_uni'), f.get('pg_yop'), f.get('pg_per'), f.get('pg_cgpa'),
             f.get('extra'), f.get('other')))
        db.commit()
        flash('Education details added.', 'success')
        return redirect(url_for('user_education'))
    return render_template('user/add_education.html')

@app.route('/user/edit-education', methods=['GET','POST'])
@user_required
def user_edit_education():
    db  = get_db()
    uid = session['user_id']
    edu = db.execute("SELECT * FROM tbleducation WHERE UserID=?", (uid,)).fetchone()
    if not edu:
        return redirect(url_for('user_add_education'))
    if request.method == 'POST':
        f = request.form
        db.execute("""UPDATE tbleducation SET
            SecondaryBoard=?,SecondaryBoardyop=?,SecondaryBoardper=?,SecondaryBoardcgpa=?,
            SSecondaryBoard=?,SSecondaryBoardyop=?,SSecondaryBoardper=?,SSecondaryBoardcgpa=?,
            GraUni=?,GraUniyop=?,GraUnidper=?,GraUnicgpa=?,
            PGUni=?,PGUniyop=?,PGUniper=?,PGUnicgpa=?,ExtraCurriculars=?,OtherAchivement=?
            WHERE UserID=?""",
            (f.get('sec_board'), f.get('sec_yop'), f.get('sec_per'), f.get('sec_cgpa'),
             f.get('ssec_board'), f.get('ssec_yop'), f.get('ssec_per'), f.get('ssec_cgpa'),
             f.get('gra_uni'), f.get('gra_yop'), f.get('gra_per'), f.get('gra_cgpa'),
             f.get('pg_uni'), f.get('pg_yop'), f.get('pg_per'), f.get('pg_cgpa'),
             f.get('extra'), f.get('other'), uid))
        db.commit()
        flash('Education details updated.', 'success')
        return redirect(url_for('user_education'))
    return render_template('user/add_education.html', edu=edu)

@app.route('/user/view-jobs')
@user_required
def user_view_jobs():
    db  = get_db()
    kw  = request.args.get('keyword', '').strip()
    loc = request.args.get('location', '').strip()
    sql = """SELECT v.*, c.CompanyName FROM tblvacancy v
             JOIN tblcompany c ON c.ID=v.CompanyID WHERE 1=1"""
    params = []
    if kw:
        sql += " AND v.JobTitle LIKE ?"; params.append(f'%{kw}%')
    if loc:
        sql += " AND v.JobLocation LIKE ?"; params.append(f'%{loc}%')
    sql += " ORDER BY v.ID DESC"
    jobs = db.execute(sql, params).fetchall()
    return render_template('user/view_jobs.html', jobs=jobs, keyword=kw, location=loc)

@app.route('/user/apply-job/<int:job_id>', methods=['GET','POST'])
@user_required
def user_apply_job(job_id):
    db  = get_db()
    uid = session['user_id']
    job = db.execute("SELECT v.*, c.CompanyName FROM tblvacancy v JOIN tblcompany c ON c.ID=v.CompanyID WHERE v.ID=?", (job_id,)).fetchone()
    if not job:
        flash('Job not found.', 'danger')
        return redirect(url_for('user_view_jobs'))
    already = db.execute("SELECT ID FROM tblapplyjob WHERE UserId=? AND JobId=?", (uid, job_id)).fetchone()
    if already:
        flash('You have already applied for this job.', 'warning')
        return redirect(url_for('user_applications'))
    if request.method == 'POST':
        msg   = request.form.get('message','').strip()
        rfile = request.files.get('resume')
        fname = save_file(rfile, 'doc') or ''
        db.execute("INSERT INTO tblapplyjob (UserId,JobId,Resume,Message) VALUES (?,?,?,?)",
                   (uid, job_id, fname, msg))
        db.commit()
        flash('Application submitted successfully!', 'success')
        return redirect(url_for('user_applications'))
    return render_template('user/apply_job.html', job=job)

@app.route('/user/applications')
@user_required
def user_applications():
    db  = get_db()
    uid = session['user_id']
    apps = db.execute("""SELECT a.*, v.JobTitle, v.JobLocation, c.CompanyName
                         FROM tblapplyjob a
                         JOIN tblvacancy v ON v.ID=a.JobId
                         JOIN tblcompany c ON c.ID=v.CompanyID
                         WHERE a.UserId=? ORDER BY a.ID DESC""", (uid,)).fetchall()
    return render_template('user/applications.html', apps=apps)

@app.route('/user/view-application/<int:app_id>')
@user_required
def user_view_application(app_id):
    db  = get_db()
    uid = session['user_id']
    app_ = db.execute("""SELECT a.*, v.JobTitle, v.JobLocation, v.MonthlySalary, v.JobDescriptions,
                                 c.CompanyName, c.CompanyEmail
                          FROM tblapplyjob a
                          JOIN tblvacancy v ON v.ID=a.JobId
                          JOIN tblcompany c ON c.ID=v.CompanyID
                          WHERE a.ID=? AND a.UserId=?""", (app_id, uid)).fetchone()
    if not app_:
        flash('Application not found.', 'danger')
        return redirect(url_for('user_applications'))
    msgs = db.execute("SELECT * FROM tblmessage WHERE AppID=? ORDER BY ID DESC", (app_id,)).fetchall()
    return render_template('user/view_application.html', app=app_, msgs=msgs)


# ══════════════════════════════════════════
#           COMPANY PORTAL
# ══════════════════════════════════════════

@app.route('/company/login', methods=['GET','POST'])
def company_login():
    if session.get('company_id'):
        return redirect(url_for('company_dashboard'))
    if request.method == 'POST':
        email = request.form['email'].strip()
        pwd   = md5(request.form['password'])
        db    = get_db()
        comp  = db.execute("SELECT * FROM tblcompany WHERE CompanyEmail=? AND Password=?",
                           (email, pwd)).fetchone()
        if comp:
            session['company_id']   = comp['ID']
            session['company_name'] = comp['CompanyName']
            flash(f"Welcome, {comp['CompanyName']}!", 'success')
            return redirect(url_for('company_dashboard'))
        flash('Invalid email or password.', 'danger')
    return render_template('company/login.html')

@app.route('/company/register', methods=['GET','POST'])
def company_register():
    if request.method == 'POST':
        db = get_db()
        name    = request.form['company_name'].strip()
        contact = request.form['contact_person'].strip()
        url_    = request.form['company_url'].strip()
        addr    = request.form['address'].strip()
        mobile  = request.form['mobile'].strip()
        email   = request.form['email'].strip()
        pwd     = md5(request.form['password'])
        exists  = db.execute("SELECT ID FROM tblcompany WHERE CompanyEmail=?", (email,)).fetchone()
        if exists:
            flash('Email already registered.', 'warning')
        else:
            db.execute("""INSERT INTO tblcompany
                (CompanyName,ContactPerson,CompanyUrl,CompanyAddress,MobileNumber,CompanyEmail,Password)
                VALUES (?,?,?,?,?,?,?)""",
                (name,contact,url_,addr,mobile,email,pwd))
            db.commit()
            flash('Company registered! Please login.', 'success')
            return redirect(url_for('company_login'))
    return render_template('company/register.html')

@app.route('/company/logout')
def company_logout():
    session.pop('company_id', None)
    session.pop('company_name', None)
    return redirect(url_for('home'))

@app.route('/company/forgot-password', methods=['GET','POST'])
def company_forgot():
    if request.method == 'POST':
        flash('Password reset link sent. (Demo: password unchanged)', 'info')
    return render_template('company/forgot_password.html')

@app.route('/company/dashboard')
@company_required
def company_dashboard():
    db  = get_db()
    cid = session['company_id']
    total_vac  = db.execute("SELECT COUNT(*) FROM tblvacancy WHERE CompanyID=?", (cid,)).fetchone()[0]
    total_apps = db.execute("""SELECT COUNT(*) FROM tblapplyjob a
                               JOIN tblvacancy v ON v.ID=a.JobId WHERE v.CompanyID=?""", (cid,)).fetchone()[0]
    new_apps   = db.execute("""SELECT COUNT(*) FROM tblapplyjob a
                               JOIN tblvacancy v ON v.ID=a.JobId
                               WHERE v.CompanyID=? AND (a.Status IS NULL OR a.Status='')""", (cid,)).fetchone()[0]
    sorted_apps   = db.execute("""SELECT COUNT(*) FROM tblapplyjob a JOIN tblvacancy v ON v.ID=a.JobId
                               WHERE v.CompanyID=? AND a.Status='Sorted'""", (cid,)).fetchone()[0]
    selected_apps = db.execute("""SELECT COUNT(*) FROM tblapplyjob a JOIN tblvacancy v ON v.ID=a.JobId
                               WHERE v.CompanyID=? AND a.Status='Selected'""", (cid,)).fetchone()[0]
    rejected_apps = db.execute("""SELECT COUNT(*) FROM tblapplyjob a JOIN tblvacancy v ON v.ID=a.JobId
                               WHERE v.CompanyID=? AND a.Status='Rejected'""", (cid,)).fetchone()[0]
    return render_template('company/dashboard.html',
        total_vac=total_vac, total_apps=total_apps, new_apps=new_apps,
        sorted_apps=sorted_apps, selected_apps=selected_apps, rejected_apps=rejected_apps)

@app.route('/company/profile', methods=['GET','POST'])
@company_required
def company_profile():
    db  = get_db()
    cid = session['company_id']
    if request.method == 'POST':
        name    = request.form['company_name'].strip()
        contact = request.form['contact_person'].strip()
        url_    = request.form['company_url'].strip()
        addr    = request.form['address'].strip()
        mobile  = request.form['mobile'].strip()
        logo    = request.files.get('logo')
        lg_name = save_file(logo, 'img')
        if lg_name:
            db.execute("UPDATE tblcompany SET CompanyName=?,ContactPerson=?,CompanyUrl=?,CompanyAddress=?,MobileNumber=?,CompanyLogo=? WHERE ID=?",
                       (name,contact,url_,addr,mobile,lg_name,cid))
        else:
            db.execute("UPDATE tblcompany SET CompanyName=?,ContactPerson=?,CompanyUrl=?,CompanyAddress=?,MobileNumber=? WHERE ID=?",
                       (name,contact,url_,addr,mobile,cid))
        db.commit()
        session['company_name'] = name
        flash('Profile updated.', 'success')
        return redirect(url_for('company_profile'))
    comp = db.execute("SELECT * FROM tblcompany WHERE ID=?", (cid,)).fetchone()
    return render_template('company/profile.html', comp=comp)

@app.route('/company/change-password', methods=['GET','POST'])
@company_required
def company_change_password():
    db  = get_db()
    cid = session['company_id']
    if request.method == 'POST':
        old = md5(request.form['old_password'])
        new = request.form['new_password']
        cnf = request.form['confirm_password']
        comp = db.execute("SELECT * FROM tblcompany WHERE ID=? AND Password=?", (cid, old)).fetchone()
        if not comp: flash('Current password is incorrect.', 'danger')
        elif new != cnf: flash('New passwords do not match.', 'danger')
        else:
            db.execute("UPDATE tblcompany SET Password=? WHERE ID=?", (md5(new), cid))
            db.commit()
            flash('Password changed.', 'success')
    return render_template('company/change_password.html')

@app.route('/company/add-vacancy', methods=['GET','POST'])
@company_required
def company_add_vacancy():
    db  = get_db()
    cid = session['company_id']
    if request.method == 'POST':
        f = request.form
        db.execute("""INSERT INTO tblvacancy
            (CompanyID,JobTitle,MonthlySalary,JobDescriptions,NoofOpenings,JobLocation,ApplyDate,LastDate)
            VALUES (?,?,?,?,?,?,?,?)""",
            (cid, f['job_title'], f['salary'], f['description'], f['openings'],
             f['location'], f['apply_date'], f['last_date']))
        db.commit()
        flash('Vacancy posted successfully!', 'success')
        return redirect(url_for('company_manage_vacancies'))
    return render_template('company/add_vacancy.html')

@app.route('/company/edit-vacancy/<int:vac_id>', methods=['GET','POST'])
@company_required
def company_edit_vacancy(vac_id):
    db  = get_db()
    cid = session['company_id']
    vac = db.execute("SELECT * FROM tblvacancy WHERE ID=? AND CompanyID=?", (vac_id, cid)).fetchone()
    if not vac:
        flash('Vacancy not found.', 'danger')
        return redirect(url_for('company_manage_vacancies'))
    if request.method == 'POST':
        f = request.form
        db.execute("""UPDATE tblvacancy SET JobTitle=?,MonthlySalary=?,JobDescriptions=?,
                      NoofOpenings=?,JobLocation=?,ApplyDate=?,LastDate=? WHERE ID=? AND CompanyID=?""",
                   (f['job_title'], f['salary'], f['description'], f['openings'],
                    f['location'], f['apply_date'], f['last_date'], vac_id, cid))
        db.commit()
        flash('Vacancy updated.', 'success')
        return redirect(url_for('company_manage_vacancies'))
    return render_template('company/edit_vacancy.html', vac=vac)

@app.route('/company/delete-vacancy/<int:vac_id>')
@company_required
def company_delete_vacancy(vac_id):
    db  = get_db()
    cid = session['company_id']
    db.execute("DELETE FROM tblvacancy WHERE ID=? AND CompanyID=?", (vac_id, cid))
    db.commit()
    flash('Vacancy deleted.', 'success')
    return redirect(url_for('company_manage_vacancies'))

@app.route('/company/manage-vacancies')
@company_required
def company_manage_vacancies():
    db   = get_db()
    cid  = session['company_id']
    vacs = db.execute("SELECT * FROM tblvacancy WHERE CompanyID=? ORDER BY ID DESC", (cid,)).fetchall()
    return render_template('company/manage_vacancies.html', vacs=vacs)

def company_get_apps(status_filter=None):
    db  = get_db()
    cid = session['company_id']
    sql = """SELECT a.*, v.JobTitle, u.FullName, u.Email as UserEmail
             FROM tblapplyjob a
             JOIN tblvacancy v ON v.ID=a.JobId
             JOIN tbluser u ON u.ID=a.UserId
             WHERE v.CompanyID=?"""
    params = [cid]
    if status_filter == 'new':
        sql += " AND (a.Status IS NULL OR a.Status='')"
    elif status_filter:
        sql += " AND a.Status=?"
        params.append(status_filter)
    sql += " ORDER BY a.ID DESC"
    return db.execute(sql, params).fetchall()

@app.route('/company/applications')
@company_required
def company_all_applications():
    apps = company_get_apps()
    return render_template('company/applications.html', apps=apps, title='All Applications', filter='all')

@app.route('/company/new-applications')
@company_required
def company_new_applications():
    apps = company_get_apps('new')
    return render_template('company/applications.html', apps=apps, title='New Applications', filter='new')

@app.route('/company/sorted-applications')
@company_required
def company_sorted_applications():
    apps = company_get_apps('Sorted')
    return render_template('company/applications.html', apps=apps, title='Sort-listed Applications', filter='Sorted')

@app.route('/company/selected-applications')
@company_required
def company_selected_applications():
    apps = company_get_apps('Selected')
    return render_template('company/applications.html', apps=apps, title='Selected Applications', filter='Selected')

@app.route('/company/rejected-applications')
@company_required
def company_rejected_applications():
    apps = company_get_apps('Rejected')
    return render_template('company/applications.html', apps=apps, title='Rejected Applications', filter='Rejected')

@app.route('/company/view-application/<int:app_id>', methods=['GET','POST'])
@company_required
def company_view_application(app_id):
    db  = get_db()
    cid = session['company_id']
    app_ = db.execute("""SELECT a.*, v.JobTitle, v.JobLocation,
                                 u.FullName, u.Email as UserEmail, u.MobileNumber as UserMobile
                          FROM tblapplyjob a
                          JOIN tblvacancy v ON v.ID=a.JobId
                          JOIN tbluser u ON u.ID=a.UserId
                          WHERE a.ID=? AND v.CompanyID=?""", (app_id, cid)).fetchone()
    if not app_:
        flash('Application not found.', 'danger')
        return redirect(url_for('company_all_applications'))
    edu = db.execute("SELECT * FROM tbleducation WHERE UserID=?", (app_['UserId'],)).fetchone()
    if request.method == 'POST':
        status  = request.form['status']
        message = request.form.get('message','').strip()
        db.execute("UPDATE tblapplyjob SET Status=?,Remark=? WHERE ID=?",
                   (status, message, app_id))
        if message:
            db.execute("INSERT INTO tblmessage (AppID,Message,Status,IsRead) VALUES (?,?,?,?)",
                       (app_id, ' '+message, status, '1'))
        db.commit()
        flash(f'Application marked as {status}.', 'success')
        return redirect(url_for('company_view_application', app_id=app_id))
    msgs = db.execute("SELECT * FROM tblmessage WHERE AppID=? ORDER BY ID DESC", (app_id,)).fetchall()
    return render_template('company/view_application.html', app=app_, edu=edu, msgs=msgs)


# ══════════════════════════════════════════
#           ADMIN PORTAL
# ══════════════════════════════════════════

@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if session.get('admin_id'):
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        username = request.form['username'].strip()
        pwd      = md5(request.form['password'])
        db       = get_db()
        admin    = db.execute("SELECT * FROM tbladmin WHERE UserName=? AND Password=?",
                              (username, pwd)).fetchone()
        if admin:
            session['admin_id']   = admin['ID']
            session['admin_name'] = admin['AdminName']
            flash('Welcome, Admin!', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials.', 'danger')
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    session.pop('admin_name', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    db = get_db()
    companies   = db.execute("SELECT COUNT(*) FROM tblcompany").fetchone()[0]
    users       = db.execute("SELECT COUNT(*) FROM tbluser").fetchone()[0]
    vacancies   = db.execute("SELECT COUNT(*) FROM tblvacancy").fetchone()[0]
    total_apps  = db.execute("SELECT COUNT(*) FROM tblapplyjob").fetchone()[0]
    new_apps    = db.execute("SELECT COUNT(*) FROM tblapplyjob WHERE Status IS NULL OR Status=''").fetchone()[0]
    sorted_apps = db.execute("SELECT COUNT(*) FROM tblapplyjob WHERE Status='Sorted'").fetchone()[0]
    selected    = db.execute("SELECT COUNT(*) FROM tblapplyjob WHERE Status='Selected'").fetchone()[0]
    rejected    = db.execute("SELECT COUNT(*) FROM tblapplyjob WHERE Status='Rejected'").fetchone()[0]
    return render_template('admin/dashboard.html',
        companies=companies, users=users, vacancies=vacancies,
        total_apps=total_apps, new_apps=new_apps, sorted_apps=sorted_apps,
        selected=selected, rejected=rejected)

@app.route('/admin/companies')
@admin_required
def admin_companies():
    db    = get_db()
    comps = db.execute("SELECT * FROM tblcompany ORDER BY ID DESC").fetchall()
    return render_template('admin/companies.html', comps=comps)

@app.route('/admin/view-company/<int:comp_id>')
@admin_required
def admin_view_company(comp_id):
    db   = get_db()
    comp = db.execute("SELECT * FROM tblcompany WHERE ID=?", (comp_id,)).fetchone()
    vacs = db.execute("SELECT * FROM tblvacancy WHERE CompanyID=? ORDER BY ID DESC", (comp_id,)).fetchall()
    return render_template('admin/view_company.html', comp=comp, vacs=vacs)

@app.route('/admin/users')
@admin_required
def admin_users():
    db    = get_db()
    users = db.execute("SELECT * FROM tbluser ORDER BY ID DESC").fetchall()
    return render_template('admin/users.html', users=users)

@app.route('/admin/view-user/<int:user_id>')
@admin_required
def admin_view_user(user_id):
    db   = get_db()
    user = db.execute("SELECT * FROM tbluser WHERE ID=?", (user_id,)).fetchone()
    edu  = db.execute("SELECT * FROM tbleducation WHERE UserID=?", (user_id,)).fetchone()
    apps = db.execute("""SELECT a.*, v.JobTitle, c.CompanyName FROM tblapplyjob a
                          JOIN tblvacancy v ON v.ID=a.JobId
                          JOIN tblcompany c ON c.ID=v.CompanyID
                          WHERE a.UserId=? ORDER BY a.ID DESC""", (user_id,)).fetchall()
    return render_template('admin/view_user.html', user=user, edu=edu, apps=apps)

@app.route('/admin/delete-user/<int:user_id>', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    db = get_db()
    db.execute("DELETE FROM tbluser WHERE ID=?", (user_id,))
    db.execute("DELETE FROM tbleducation WHERE UserID=?", (user_id,))
    # Delete their applications
    db.execute("DELETE FROM tblapplyjob WHERE UserId=?", (user_id,))
    db.commit()
    flash('User and all related records have been deleted.', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/add-company', methods=['GET', 'POST'])
@admin_required
def admin_add_company():
    if request.method == 'POST':
        cname = request.form['company_name'].strip()
        cperson = request.form['contact_person'].strip()
        curl = request.form.get('company_url', '').strip()
        address = request.form['address'].strip()
        mobile = request.form['mobile'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        pwd_hash = hashlib.md5(password.encode()).hexdigest()
        
        db = get_db()
        chk = db.execute("SELECT ID FROM tblcompany WHERE CompanyEmail=?", (email,)).fetchone()
        if chk:
            flash('This email is already registered to a company.', 'danger')
        else:
            db.execute('''INSERT INTO tblcompany 
                          (CompanyName,ContactPerson,CompanyUrl,CompanyAddress,MobileNumber,CompanyEmail,Password) 
                          VALUES (?,?,?,?,?,?,?)''',
                       (cname, cperson, curl, address, mobile, email, pwd_hash))
            db.commit()
            flash('New Company added successfully.', 'success')
            return redirect(url_for('admin_companies'))
    return render_template('admin/add_company.html')

@app.route('/admin/delete-company/<int:comp_id>', methods=['POST'])
@admin_required
def admin_delete_company(comp_id):
    db = get_db()
    db.execute("DELETE FROM tblcompany WHERE ID=?", (comp_id,))
    db.execute("DELETE FROM tblvacancy WHERE CompanyID=?", (comp_id,))
    db.commit()
    flash('Company and all its job postings have been permanently deleted.', 'success')
    return redirect(url_for('admin_companies'))

@app.route('/admin/jobs')
@admin_required
def admin_jobs():
    db   = get_db()
    jobs = db.execute("""SELECT v.*, c.CompanyName FROM tblvacancy v
                         JOIN tblcompany c ON c.ID=v.CompanyID ORDER BY v.ID DESC""").fetchall()
    return render_template('admin/jobs.html', jobs=jobs)

@app.route('/admin/applications')
@admin_required
def admin_applications():
    db   = get_db()
    filt = request.args.get('filter', 'all')
    sql  = """SELECT a.*, v.JobTitle, u.FullName, c.CompanyName FROM tblapplyjob a
              JOIN tblvacancy v ON v.ID=a.JobId
              JOIN tbluser u ON u.ID=a.UserId
              JOIN tblcompany c ON c.ID=v.CompanyID"""
    params = []
    if filt == 'new':
        sql += " WHERE (a.Status IS NULL OR a.Status='')"
    elif filt in ('Sorted','Selected','Rejected'):
        sql += " WHERE a.Status=?"; params.append(filt)
    sql += " ORDER BY a.ID DESC"
    apps = db.execute(sql, params).fetchall()
    return render_template('admin/applications.html', apps=apps, filter=filt)

@app.route('/admin/change-password', methods=['GET','POST'])
@admin_required
def admin_change_password():
    db  = get_db()
    aid = session['admin_id']
    if request.method == 'POST':
        old = md5(request.form['old_password'])
        new = request.form['new_password']
        cnf = request.form['confirm_password']
        adm = db.execute("SELECT * FROM tbladmin WHERE ID=? AND Password=?", (aid, old)).fetchone()
        if not adm: flash('Current password is incorrect.', 'danger')
        elif new != cnf: flash('Passwords do not match.', 'danger')
        else:
            db.execute("UPDATE tbladmin SET Password=? WHERE ID=?", (md5(new), aid))
            db.commit()
            flash('Password changed.', 'success')
    return render_template('admin/change_password.html')

# ─────────────── run ───────────────
if __name__ == '__main__':
    app.run(debug=True, port=5000)
