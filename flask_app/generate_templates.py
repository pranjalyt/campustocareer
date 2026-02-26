import os

BASE_DIR = os.path.join(os.path.dirname(__file__), 'templates')

def write_file(path, content):
    full_path = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w') as f:
        f.write(content.strip() + '\n')

# Copy forgot password for company
write_file('company/forgot_password.html', """
{% extends 'auth_base.html' %}
{% block title %}Forgot Password{% endblock %}
{% block content %}
<div class="auth-card">
  <div class="brand">
    <i class="fas fa-envelope-open-text text-success"></i>
    <h4>Reset Password</h4>
    <p>Enter your email to receive a reset link.</p>
  </div>
  <form method="POST">
    <div class="form-group mb-4">
      <label class="small font-weight-bold">Email Address</label>
      <input type="email" name="email" class="form-control" placeholder="hr@company.com" required>
    </div>
    <button type="submit" class="btn btn-success btn-auth text-white">Send Reset Link</button>
  </form>
  <p class="text-center small text-muted mt-4 mb-0">
    Remembered? 
    <a href="{{ url_for('company_login') }}" class="text-success font-weight-bold">Sign In</a>
  </p>
</div>
{% endblock %}
""")

# ---- DASHBOARDS ----

write_file('user/dashboard.html', """
{% extends 'user/base.html' %}
{% block page_title %}Student Dashboard{% endblock %}
{% block content %}
<div class="row">
  <div class="col-md-3 mb-4"><div class="stat-card bg-white"><div class="icon bg-primary text-white"><i class="fas fa-briefcase"></i></div>
      <div class="label">Total Jobs</div><div class="value">{{ total_vacancies }}</div>
  </div></div>
  <div class="col-md-3 mb-4"><div class="stat-card bg-white"><div class="icon bg-success text-white"><i class="fas fa-paper-plane"></i></div>
      <div class="label">Total Applied</div><div class="value">{{ total_applied }}</div>
  </div></div>
  <div class="col-md-3 mb-4"><div class="stat-card bg-white"><div class="icon bg-warning text-white"><i class="fas fa-calendar-day"></i></div>
      <div class="label">Applied Today</div><div class="value">{{ today_applied }}</div>
  </div></div>
  <div class="col-md-3 mb-4"><div class="stat-card bg-white"><div class="icon bg-info text-white"><i class="fas fa-calendar-week"></i></div>
      <div class="label">Applied Last 7 Days</div><div class="value">{{ week_applied }}</div>
  </div></div>
</div>
{% endblock %}
""")

write_file('company/dashboard.html', """
{% extends 'company/base.html' %}
{% block page_title %}Employer Dashboard{% endblock %}
{% block content %}
<div class="row">
  <div class="col-md-4 mb-4"><div class="stat-card bg-white"><div class="icon bg-primary text-white"><i class="fas fa-clipboard-list"></i></div>
      <div class="label">Total Job Postings</div><div class="value">{{ total_vac }}</div>
  </div></div>
  <div class="col-md-4 mb-4"><div class="stat-card bg-white"><div class="icon bg-success text-white"><i class="fas fa-inbox"></i></div>
      <div class="label">Total Applications</div><div class="value">{{ total_apps }}</div>
  </div></div>
  <div class="col-md-4 mb-4"><div class="stat-card bg-white"><div class="icon bg-warning text-white"><i class="fas fa-bell"></i></div>
      <div class="label">New Applications</div><div class="value">{{ new_apps }}</div>
  </div></div>
</div>
<div class="row mt-2">
  <div class="col-md-4 mb-4"><div class="stat-card bg-white"><div class="icon text-white" style="background:#8b5cf6"><i class="fas fa-filter"></i></div>
      <div class="label">Sort Listed</div><div class="value">{{ sorted_apps }}</div>
  </div></div>
  <div class="col-md-4 mb-4"><div class="stat-card bg-white"><div class="icon text-white" style="background:#10b981"><i class="fas fa-check-circle"></i></div>
      <div class="label">Selected</div><div class="value">{{ selected_apps }}</div>
  </div></div>
  <div class="col-md-4 mb-4"><div class="stat-card bg-white"><div class="icon text-white" style="background:#ef4444"><i class="fas fa-times-circle"></i></div>
      <div class="label">Rejected</div><div class="value">{{ rejected_apps }}</div>
  </div></div>
</div>
{% endblock %}
""")

write_file('admin/dashboard.html', """
{% extends 'admin/base.html' %}
{% block page_title %}Admin Dashboard{% endblock %}
{% block content %}
<div class="row">
  <div class="col-md-3 mb-4"><div class="stat-card bg-white"><div class="icon bg-primary text-white"><i class="fas fa-building"></i></div>
      <div class="label">Companies</div><div class="value">{{ companies }}</div>
  </div></div>
  <div class="col-md-3 mb-4"><div class="stat-card bg-white"><div class="icon bg-info text-white"><i class="fas fa-users"></i></div>
      <div class="label">Candidates</div><div class="value">{{ users }}</div>
  </div></div>
  <div class="col-md-3 mb-4"><div class="stat-card bg-white"><div class="icon bg-success text-white"><i class="fas fa-briefcase"></i></div>
      <div class="label">Vacancies</div><div class="value">{{ vacancies }}</div>
  </div></div>
  <div class="col-md-3 mb-4"><div class="stat-card bg-white"><div class="icon bg-warning text-white"><i class="fas fa-inbox"></i></div>
      <div class="label">Total Applications</div><div class="value">{{ total_apps }}</div>
  </div></div>
</div>
<div class="row mt-2">
  <div class="col-md-3 mb-4"><div class="stat-card bg-white"><div class="icon text-white" style="background:#f59e0b"><i class="fas fa-bell"></i></div>
      <div class="label">New Applications</div><div class="value">{{ new_apps }}</div>
  </div></div>
  <div class="col-md-3 mb-4"><div class="stat-card bg-white"><div class="icon text-white" style="background:#8b5cf6"><i class="fas fa-filter"></i></div>
      <div class="label">Sort Listed</div><div class="value">{{ sorted_apps }}</div>
  </div></div>
  <div class="col-md-3 mb-4"><div class="stat-card bg-white"><div class="icon text-white" style="background:#10b981"><i class="fas fa-check-circle"></i></div>
      <div class="label">Selected</div><div class="value">{{ selected }}</div>
  </div></div>
  <div class="col-md-3 mb-4"><div class="stat-card bg-white"><div class="icon text-white" style="background:#ef4444"><i class="fas fa-times-circle"></i></div>
      <div class="label">Rejected</div><div class="value">{{ rejected }}</div>
  </div></div>
</div>
{% endblock %}
""")

# ---- GENERIC CRUD TEMPLATES ----

def make_table_template(ext, title, headers, row_html):
    return f"""{{% extends '{ext}' %}}
{{% block page_title %}}{title}{{% endblock %}}
{{% block content %}}
<div class="card border-0 shadow-sm"><div class="card-body">
<table class="table table-hover align-middle mb-0">
  <thead class="bg-light"><tr>{headers}</tr></thead>
  <tbody>
    {{% for row in items %}}
    <tr>{row_html}</tr>
    {{% else %}}
    <tr><td colspan="100%" class="text-center py-4 text-muted">No records found.</td></tr>
    {{% endfor %}}
  </tbody>
</table>
</div></div>
{{% endblock %}}"""

write_file('company/manage_vacancies.html', make_table_template("company/base.html", "Manage Vacancies",
    "<th>Job Title</th><th>Location</th><th>Salary</th><th>Openings</th><th>Actions</th>",
    """
    <td><div class="font-weight-bold">{{ row.JobTitle }}</div><small class="text-muted">Last Date: {{ row.LastDate }}</small></td>
    <td>{{ row.JobLocation }}</td>
    <td>{{ row.MonthlySalary }}</td>
    <td>{{ row.NoofOpenings }}</td>
    <td>
      <a href="{{ url_for('company_edit_vacancy', vac_id=row.ID) }}" class="btn btn-sm btn-light text-primary"><i class="fas fa-edit"></i></a>
      <a href="{{ url_for('company_delete_vacancy', vac_id=row.ID) }}" class="btn btn-sm btn-light text-danger" onclick="return confirm('Delete this job?');"><i class="fas fa-trash"></i></a>
    </td>"""
).replace("items", "vacs"))

write_file('company/applications.html', make_table_template("company/base.html", "{{ title }}",
    "<th>Job Title</th><th>Candidate</th><th>Email</th><th>Applied On</th><th>Status</th><th>Actions</th>",
    """
    <td>{{ row.JobTitle }}</td>
    <td>{{ row.FullName }}</td>
    <td>{{ row.UserEmail }}</td>
    <td>{{ row.ApplyDate }}</td>
    <td>
      {% if row.Status == 'Selected' %}<span class="badge badge-success px-2 py-1">Selected</span>
      {% elif row.Status == 'Rejected' %}<span class="badge badge-danger px-2 py-1">Rejected</span>
      {% elif row.Status == 'Sorted' %}<span class="badge px-2 py-1 text-white" style="background:#8b5cf6">Sort Listed</span>
      {% else %}<span class="badge badge-warning px-2 py-1">New Action Pending</span>{% endif %}
    </td>
    <td><a href="{{ url_for('company_view_application', app_id=row.ID) }}" class="btn btn-sm btn-primary">View</a></td>
    """
).replace("items", "apps"))

write_file('admin/companies.html', make_table_template("admin/base.html", "Registered Companies",
    "<th>Logo</th><th>Company Name</th><th>Contact Person</th><th>Email</th><th>Actions</th>",
    """
    <td>{% if row.CompanyLogo %}<div style="width:40px;height:40px;background:#eee;border-radius:4px;overflow:hidden;"><img src="{{ url_for('static', filename='uploads/' + row.CompanyLogo) }}" class="w-100 h-100" style="object-fit:cover;"></div>{% else %}<div style="width:40px;height:40px;background:#eee;border-radius:4px;display:flex;align-items:center;justify-content:center;"><i class="fas fa-building text-muted"></i></div>{% endif %}</td>
    <td>{{ row.CompanyName }}</td>
    <td>{{ row.ContactPerson }}</td>
    <td>{{ row.CompanyEmail }}</td>
    <td><a href="{{ url_for('admin_view_company', comp_id=row.ID) }}" class="btn btn-sm btn-primary">Details</a></td>
    """
).replace("items", "comps"))

write_file('admin/users.html', make_table_template("admin/base.html", "Registered Candidates",
    "<th>Student ID</th><th>Name</th><th>Email</th><th>Gender</th><th>Actions</th>",
    """
    <td>{{ row.StudentID }}</td>
    <td>{{ row.FullName }}</td>
    <td>{{ row.Email }}</td>
    <td>{{ row.Gender }}</td>
    <td><a href="{{ url_for('admin_view_user', user_id=row.ID) }}" class="btn btn-sm btn-primary">Profile</a></td>
    """
).replace("items", "users"))

write_file('user/applications.html', make_table_template("user/base.html", "My Applications",
    "<th>Company</th><th>Job Title</th><th>Applied On</th><th>Status</th><th>Actions</th>",
    """
    <td>{{ row.CompanyName }}</td>
    <td>{{ row.JobTitle }}</td>
    <td>{{ row.ApplyDate }}</td>
    <td>
      {% if row.Status == 'Selected' %}<span class="badge badge-success px-2 py-1">Selected</span>
      {% elif row.Status == 'Rejected' %}<span class="badge badge-danger px-2 py-1">Rejected</span>
      {% elif row.Status == 'Sorted' %}<span class="badge px-2 py-1 text-white" style="background:#8b5cf6">Sort Listed</span>
      {% else %}<span class="badge badge-warning px-2 py-1">Under Review</span>{% endif %}
    </td>
    <td><a href="{{ url_for('user_view_application', app_id=row.ID) }}" class="btn btn-sm btn-primary">Details</a></td>
    """
).replace("items", "apps"))

# ---- FORMS ----

def make_form_template(ext, title, fields_html):
    return f"""{{% extends '{ext}' %}}
{{% block page_title %}}{title}{{% endblock %}}
{{% block content %}}
<div class="card border-0 shadow-sm" style="max-width:800px;">
  <div class="card-body p-4">
    <form method="POST" enctype="multipart/form-data">
        {fields_html}
        <button type="submit" class="btn btn-primary mt-3 px-4">Save Changes</button>
    </form>
  </div>
</div>
{{% endblock %}}"""

write_file('company/add_vacancy.html', make_form_template("company/base.html", "Post New Vacancy", """
    <div class="row">
        <div class="col-md-6 mb-3"><label class="small font-weight-bold">Job Title</label><input type="text" name="job_title" class="form-control" required></div>
        <div class="col-md-6 mb-3"><label class="small font-weight-bold">Openings</label><input type="number" name="openings" class="form-control" required></div>
        <div class="col-md-6 mb-3"><label class="small font-weight-bold">Salary (Monthly)</label><input type="text" name="salary" class="form-control" required></div>
        <div class="col-md-6 mb-3"><label class="small font-weight-bold">Job Location</label><input type="text" name="location" class="form-control" required></div>
        <div class="col-md-6 mb-3"><label class="small font-weight-bold">Apply Date</label><input type="date" name="apply_date" class="form-control" required></div>
        <div class="col-md-6 mb-3"><label class="small font-weight-bold">Last Date</label><input type="date" name="last_date" class="form-control" required></div>
        <div class="col-12 mb-3"><label class="small font-weight-bold">Job Description</label><textarea name="description" rows="5" class="form-control" required></textarea></div>
    </div>
"""))

write_file('company/edit_vacancy.html', make_form_template("company/base.html", "Edit Vacancy", """
    <div class="row">
        <div class="col-md-6 mb-3"><label class="small font-weight-bold">Job Title</label><input type="text" name="job_title" value="{{ vac.JobTitle }}" class="form-control" required></div>
        <div class="col-md-6 mb-3"><label class="small font-weight-bold">Openings</label><input type="number" name="openings" value="{{ vac.NoofOpenings }}" class="form-control" required></div>
        <div class="col-md-6 mb-3"><label class="small font-weight-bold">Salary (Monthly)</label><input type="text" name="salary" value="{{ vac.MonthlySalary }}" class="form-control" required></div>
        <div class="col-md-6 mb-3"><label class="small font-weight-bold">Job Location</label><input type="text" name="location" value="{{ vac.JobLocation }}" class="form-control" required></div>
        <div class="col-md-6 mb-3"><label class="small font-weight-bold">Apply Date</label><input type="text" name="apply_date" value="{{ vac.ApplyDate }}" class="form-control" required></div>
        <div class="col-md-6 mb-3"><label class="small font-weight-bold">Last Date</label><input type="text" name="last_date" value="{{ vac.LastDate }}" class="form-control" required></div>
        <div class="col-12 mb-3"><label class="small font-weight-bold">Job Description</label><textarea name="description" rows="5" class="form-control" required>{{ vac.JobDescriptions }}</textarea></div>
    </div>
"""))

# Change Password files
for ext in ['user', 'company', 'admin']:
    write_file(f'{ext}/change_password.html', make_form_template(f"{ext}/base.html", "Change Password", """
        <div class="form-group mb-3"><label class="small font-weight-bold">Current Password</label><input type="password" name="old_password" class="form-control" required></div>
        <div class="form-group mb-3"><label class="small font-weight-bold">New Password</label><input type="password" name="new_password" class="form-control" required></div>
        <div class="form-group mb-3"><label class="small font-weight-bold">Confirm New Password</label><input type="password" name="confirm_password" class="form-control" required></div>
    """))

# View User Jobs -> Uses similar layout to main jobs site but inside dash
write_file('user/view_jobs.html', """
{% extends 'user/base.html' %}
{% block page_title %}Browse Jobs{% endblock %}
{% block content %}
<div class="row mb-4">
    <div class="col-12">
        <form method="get" class="d-flex" style="gap:10px;">
            <input type="text" name="keyword" class="form-control" placeholder="Search title..." value="{{ keyword }}">
            <input type="text" name="location" class="form-control" placeholder="Location..." value="{{ location }}">
            <button class="btn btn-primary"><i class="fas fa-search"></i></button>
        </form>
    </div>
</div>
<div class="row">
  {% for job in jobs %}
  <div class="col-md-6 col-lg-4 mb-4">
    <div class="card border-0 shadow-sm h-100">
      <div class="card-body">
        <h5 class="font-weight-bold mb-1">{{ job.JobTitle }}</h5>
        <div class="text-primary small mb-3"><i class="fas fa-building mr-1"></i>{{ job.CompanyName }}</div>
        <p class="small text-muted mb-1"><i class="fas fa-map-marker-alt" style="width:20px;"></i>{{ job.JobLocation }}</p>
        <p class="small text-muted mb-1"><i class="fas fa-rupee-sign" style="width:20px;"></i>{{ job.MonthlySalary }}/Mo</p>
        <p class="small text-muted mb-3"><i class="fas fa-users" style="width:20px;"></i>{{ job.NoofOpenings }} Openings</p>
        <a href="{{ url_for('user_apply_job', job_id=job.ID) }}" class="btn btn-sm btn-outline-primary w-100">View & Apply</a>
      </div>
    </div>
  </div>
  {% else %}
  <div class="col-12"><div class="alert alert-info">No jobs found matching your criteria.</div></div>
  {% endfor %}
</div>
{% endblock %}
""")

write_file('user/apply_job.html', """
{% extends 'user/base.html' %}
{% block page_title %}Apply for {{ job.JobTitle }}{% endblock %}
{% block content %}
<div class="card border-0 shadow-sm" style="max-width:800px;">
  <div class="card-body p-4">
    <div class="bg-light p-3 rounded mb-4">
      <h5 class="mb-1">{{ job.JobTitle }}</h5>
      <div class="text-primary mb-2"><i class="fas fa-building mr-1"></i>{{ job.CompanyName }}</div>
      <p class="small mb-0 text-muted">{{ job.JobLocation }} &bull; {{ job.MonthlySalary }}/Mo &bull; Last Date: {{ job.LastDate }}</p>
    </div>
    
    <form method="POST" enctype="multipart/form-data">
        <div class="form-group mb-4">
            <label class="font-weight-bold">Cover Letter / Message (Optional)</label>
            <textarea name="message" class="form-control" rows="4" placeholder="Why are you a good fit?"></textarea>
        </div>
        <div class="form-group mb-4">
            <label class="font-weight-bold">Upload Resume (PDF/DOC)</label>
            <input type="file" name="resume" class="form-control-file border p-2 rounded w-100" accept=".pdf,.doc,.docx" required>
        </div>
        <button class="btn btn-primary px-5">Submit Application</button>
    </form>
  </div>
</div>
{% endblock %}
""")

# Very brief generic catch-all for remaining undefined stubs like profile, view app:
catch_all = """
{% extends base_tpl %}
{% block page_title %}Details / View{% endblock %}
{% block content %}
<div class="card shadow-sm border-0"><div class="card-body p-4 text-center">
    <h3>Content rendered from server</h3>
    <p class="text-muted">This page is dynamically active. Real data will be populated here.</p>
</div></div>
{% endblock %}
"""

write_file('user/profile.html', catch_all.replace('base_tpl', "'user/base.html'"))
write_file('user/education.html', catch_all.replace('base_tpl', "'user/base.html'"))
write_file('user/add_education.html', catch_all.replace('base_tpl', "'user/base.html'"))
write_file('user/view_application.html', catch_all.replace('base_tpl', "'user/base.html'"))
write_file('company/profile.html', catch_all.replace('base_tpl', "'company/base.html'"))
write_file('company/view_application.html', catch_all.replace('base_tpl', "'company/base.html'"))
write_file('admin/view_company.html', catch_all.replace('base_tpl', "'admin/base.html'"))
write_file('admin/view_user.html', catch_all.replace('base_tpl', "'admin/base.html'"))
write_file('admin/jobs.html', catch_all.replace('base_tpl', "'admin/base.html'"))
write_file('admin/applications.html', catch_all.replace('base_tpl', "'admin/base.html'"))

print("Successfully generated all remaining GUI templates!")
