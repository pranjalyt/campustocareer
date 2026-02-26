import os

BASE_DIR = os.path.join(os.path.dirname(__file__), 'templates')

def write_file(path, content):
    full_path = os.path.join(BASE_DIR, path)
    with open(full_path, 'w') as f:
        f.write(content.strip() + '\n')

write_file('user/profile.html', """
{% extends 'user/base.html' %}
{% block page_title %}My Profile{% endblock %}
{% block content %}
<div class="card border-0 shadow-sm" style="max-width:800px;">
  <div class="card-body p-4">
    <form method="POST" enctype="multipart/form-data">
        <div class="row">
            <div class="col-md-6 mb-3">
                <label class="font-weight-bold small">Full Name</label>
                <input type="text" name="fullname" class="form-control" value="{{ user.FullName }}" required>
            </div>
            <div class="col-md-6 mb-3">
                <label class="font-weight-bold small">Mobile Number</label>
                <input type="number" name="mobile" class="form-control" value="{{ user.MobileNumber }}" required>
            </div>
            <div class="col-md-6 mb-3">
                <label class="font-weight-bold small">Gender</label>
                <select name="gender" class="form-control" required>
                    <option value="Male" {% if user.Gender=='Male' %}selected{% endif %}>Male</option>
                    <option value="Female" {% if user.Gender=='Female' %}selected{% endif %}>Female</option>
                    <option value="Other" {% if user.Gender=='Other' %}selected{% endif %}>Other</option>
                </select>
            </div>
            <div class="col-md-6 mb-3">
                <label class="font-weight-bold small">Date of Birth</label>
                <input type="date" name="dob" class="form-control" value="{{ user.DOB }}">
            </div>
            <div class="col-12 mb-3">
                <label class="font-weight-bold small">Address</label>
                <textarea name="address" class="form-control" rows="3">{{ user.Address }}</textarea>
            </div>
            <div class="col-12 mb-4">
                <label class="font-weight-bold small">Profile Image (Optional)</label>
                <input type="file" name="image" class="form-control-file border p-2 rounded w-100" accept="image/*">
                {% if user.Image %}
                <div class="mt-2"><img src="{{ url_for('static', filename='uploads/' + user.Image) }}" height="60" class="rounded shadow-sm"></div>
                {% endif %}
            </div>
        </div>
        <button type="submit" class="btn btn-primary px-4">Update Profile</button>
    </form>
  </div>
</div>
{% endblock %}
""")

write_file('user/education.html', """
{% extends 'user/base.html' %}
{% block page_title %}Education Details{% endblock %}
{% block content %}
<div class="card border-0 shadow-sm mb-4">
  <div class="card-body p-4">
    {% if edu %}
    <h5 class="mb-3">Secondary Education (10th)</h5>
    <div class="row mb-4 bg-light p-3 rounded mx-0">
        <div class="col-md-3"><strong>Board:</strong><br>{{ edu.SecondaryBoard }}</div>
        <div class="col-md-3"><strong>Year:</strong><br>{{ edu.SecondaryBoardyop }}</div>
        <div class="col-md-3"><strong>Percentage:</strong><br>{{ edu.SecondaryBoardper }}%</div>
        <div class="col-md-3"><strong>CGPA:</strong><br>{{ edu.SecondaryBoardcgpa }}</div>
    </div>
    <h5 class="mb-3">Senior Secondary (12th)</h5>
    <div class="row mb-4 bg-light p-3 rounded mx-0">
        <div class="col-md-3"><strong>Board:</strong><br>{{ edu.SSecondaryBoard }}</div>
        <div class="col-md-3"><strong>Year:</strong><br>{{ edu.SSecondaryBoardyop }}</div>
        <div class="col-md-3"><strong>Percentage:</strong><br>{{ edu.SSecondaryBoardper }}%</div>
        <div class="col-md-3"><strong>CGPA:</strong><br>{{ edu.SSecondaryBoardcgpa }}</div>
    </div>
    <h5 class="mb-3">Graduation</h5>
    <div class="row mb-4 bg-light p-3 rounded mx-0">
        <div class="col-md-3"><strong>University:</strong><br>{{ edu.GraUni }}</div>
        <div class="col-md-3"><strong>Year:</strong><br>{{ edu.GraUniyop }}</div>
        <div class="col-md-3"><strong>Percentage:</strong><br>{{ edu.GraUnidper }}%</div>
        <div class="col-md-3"><strong>CGPA:</strong><br>{{ edu.GraUnicgpa }}</div>
    </div>
    
    <div class="mt-4">
        <a href="{{ url_for('user_edit_education') }}" class="btn btn-primary px-4"><i class="fas fa-edit mr-2"></i>Edit Education Info</a>
    </div>
    {% else %}
    <div class="text-center py-5">
        <h4 class="text-muted">No education details found</h4>
        <p>You haven't added your qualification records yet.</p>
        <a href="{{ url_for('user_add_education') }}" class="btn btn-primary mt-3"><i class="fas fa-plus mr-2"></i>Add Education</a>
    </div>
    {% endif %}
  </div>
</div>
{% endblock %}
""")

write_file('user/add_education.html', """
{% extends 'user/base.html' %}
{% block page_title %}{% if edu %}Edit{% else %}Add{% endif %} Education Details{% endblock %}
{% block content %}
<div class="card border-0 shadow-sm" style="max-width:900px;">
  <div class="card-body p-4">
    <form method="POST">
        <h6 class="text-primary font-weight-bold mb-3 border-bottom pb-2">10th Standard</h6>
        <div class="row">
            <div class="col-md-3 mb-3"><label class="small text-muted">Board Name</label><input type="text" name="sec_board" class="form-control form-control-sm" value="{{ edu.SecondaryBoard if edu else '' }}" required></div>
            <div class="col-md-3 mb-3"><label class="small text-muted">Passing Year</label><input type="text" name="sec_yop" class="form-control form-control-sm" value="{{ edu.SecondaryBoardyop if edu else '' }}" required></div>
            <div class="col-md-3 mb-3"><label class="small text-muted">Percentage</label><input type="text" name="sec_per" class="form-control form-control-sm" value="{{ edu.SecondaryBoardper if edu else '' }}" required></div>
            <div class="col-md-3 mb-3"><label class="small text-muted">CGPA</label><input type="text" name="sec_cgpa" class="form-control form-control-sm" value="{{ edu.SecondaryBoardcgpa if edu else '' }}"></div>
        </div>
        
        <h6 class="text-primary font-weight-bold mb-3 mt-3 border-bottom pb-2">12th Standard</h6>
        <div class="row">
            <div class="col-md-3 mb-3"><label class="small text-muted">Board Name</label><input type="text" name="ssec_board" class="form-control form-control-sm" value="{{ edu.SSecondaryBoard if edu else '' }}" required></div>
            <div class="col-md-3 mb-3"><label class="small text-muted">Passing Year</label><input type="text" name="ssec_yop" class="form-control form-control-sm" value="{{ edu.SSecondaryBoardyop if edu else '' }}" required></div>
            <div class="col-md-3 mb-3"><label class="small text-muted">Percentage</label><input type="text" name="ssec_per" class="form-control form-control-sm" value="{{ edu.SSecondaryBoardper if edu else '' }}" required></div>
            <div class="col-md-3 mb-3"><label class="small text-muted">CGPA</label><input type="text" name="ssec_cgpa" class="form-control form-control-sm" value="{{ edu.SSecondaryBoardcgpa if edu else '' }}"></div>
        </div>
        
        <h6 class="text-primary font-weight-bold mb-3 mt-3 border-bottom pb-2">Graduation</h6>
        <div class="row">
            <div class="col-md-3 mb-3"><label class="small text-muted">University</label><input type="text" name="gra_uni" class="form-control form-control-sm" value="{{ edu.GraUni if edu else '' }}" required></div>
            <div class="col-md-3 mb-3"><label class="small text-muted">Passing Year</label><input type="text" name="gra_yop" class="form-control form-control-sm" value="{{ edu.GraUniyop if edu else '' }}" required></div>
            <div class="col-md-3 mb-3"><label class="small text-muted">Percentage</label><input type="text" name="gra_per" class="form-control form-control-sm" value="{{ edu.GraUnidper if edu else '' }}" required></div>
            <div class="col-md-3 mb-3"><label class="small text-muted">CGPA</label><input type="text" name="gra_cgpa" class="form-control form-control-sm" value="{{ edu.GraUnicgpa if edu else '' }}"></div>
        </div>

        <button class="btn btn-primary px-4 mt-4">Save Information</button>
    </form>
  </div>
</div>
{% endblock %}
""")

write_file('user/view_application.html', """
{% extends 'user/base.html' %}
{% block page_title %}Application Status{% endblock %}
{% block content %}
<div class="card border-0 shadow-sm mb-4">
    <div class="card-body">
        <h5 class="font-weight-bold">{{ app.JobTitle }} <span class="badge badge-light ml-2">{{ app.CompanyName }}</span></h5>
        <div class="text-muted small mb-4">Applied on: {{ app.ApplyDate }}</div>
        
        <h6 class="border-bottom pb-2 mb-3">Status</h6>
        {% if app.Status == 'Selected' %}
        <div class="alert alert-success"><i class="fas fa-check-circle mr-2"></i> Congratulations! You have been <strong>Selected</strong> for this role.</div>
        {% elif app.Status == 'Rejected' %}
        <div class="alert alert-danger"><i class="fas fa-times-circle mr-2"></i> Unfortunately, your application was <strong>Rejected</strong>.</div>
        {% elif app.Status == 'Sorted' %}
        <div class="alert alert-info"><i class="fas fa-filter mr-2"></i> You have been <strong>Shortlisted</strong>! The company will contact you soon.</div>
        {% else %}
        <div class="alert alert-warning"><i class="fas fa-clock mr-2"></i> Your application is still <strong>Under Review</strong>.</div>
        {% endif %}
        
        {% if msgs %}
        <h6 class="border-bottom pb-2 mb-3 mt-4">Messages from HR</h6>
        <ul class="list-group list-group-flush mb-4">
            {% for m in msgs %}
            <li class="list-group-item px-0">
                <div class="d-flex justify-content-between">
                    <strong>{{ m.Status }}</strong>
                    <small class="text-muted">{{ m.ResponseDate }}</small>
                </div>
                <p class="mb-0 mt-1">{{ m.Message }}</p>
            </li>
            {% endfor %}
        </ul>
        {% endif %}
    </div>
</div>
{% endblock %}
""")

write_file('company/profile.html', """
{% extends 'company/base.html' %}
{% block page_title %}Company Profile{% endblock %}
{% block content %}
<div class="card border-0 shadow-sm" style="max-width:800px;">
  <div class="card-body p-4">
    <form method="POST" enctype="multipart/form-data">
        <div class="row">
            <div class="col-md-6 mb-3"><label class="font-weight-bold small">Company Name</label><input type="text" name="company_name" class="form-control" value="{{ comp.CompanyName }}" required></div>
            <div class="col-md-6 mb-3"><label class="font-weight-bold small">Contact Person</label><input type="text" name="contact_person" class="form-control" value="{{ comp.ContactPerson }}" required></div>
            <div class="col-md-6 mb-3"><label class="font-weight-bold small">Website URL</label><input type="text" name="company_url" class="form-control" value="{{ comp.CompanyUrl }}"></div>
            <div class="col-md-6 mb-3"><label class="font-weight-bold small">Mobile</label><input type="number" name="mobile" class="form-control" value="{{ comp.MobileNumber }}" required></div>
            <div class="col-12 mb-3"><label class="font-weight-bold small">Headquarters Address</label><textarea name="address" class="form-control" rows="2" required>{{ comp.CompanyAddress }}</textarea></div>
            <div class="col-12 mb-4"><label class="font-weight-bold small">Company Logo</label>
                <input type="file" name="logo" class="form-control-file border p-2 rounded w-100" accept="image/*">
                {% if comp.CompanyLogo %}
                <div class="mt-2"><img src="{{ url_for('static', filename='uploads/' + comp.CompanyLogo) }}" height="60" class="rounded shadow-sm"></div>
                {% endif %}
            </div>
        </div>
        <button type="submit" class="btn btn-primary px-4">Save Changes</button>
    </form>
  </div>
</div>
{% endblock %}
""")

write_file('company/view_application.html', """
{% extends 'company/base.html' %}
{% block page_title %}Process Application{% endblock %}
{% block content %}
<div class="row">
    <div class="col-lg-7">
        <div class="card border-0 shadow-sm mb-4">
            <div class="card-header bg-white font-weight-bold">Candidate Information</div>
            <div class="card-body">
                <div class="row mb-3">
                    <div class="col-sm-4 text-muted">Name</div><div class="col-sm-8 font-weight-bold">{{ app.FullName }}</div>
                </div>
                <div class="row mb-3">
                    <div class="col-sm-4 text-muted">Email</div><div class="col-sm-8"><a href="mailto:{{ app.UserEmail }}">{{ app.UserEmail }}</a></div>
                </div>
                <div class="row mb-3">
                    <div class="col-sm-4 text-muted">Mobile</div><div class="col-sm-8">{{ app.UserMobile }}</div>
                </div>
                <div class="row mb-3">
                    <div class="col-sm-4 text-muted">Applied For</div><div class="col-sm-8 text-primary">{{ app.JobTitle }}</div>
                </div>
                <div class="row mb-3">
                    <div class="col-sm-4 text-muted">Resume</div>
                    <div class="col-sm-8">
                        {% if app.Resume %}
                        <a href="{{ url_for('static', filename='uploads/' + app.Resume) }}" class="btn btn-sm btn-outline-primary" target="_blank"><i class="fas fa-file-download mr-1"></i> Download Resume</a>
                        {% else %}
                        <span class="text-danger">No resume attached</span>
                        {% endif %}
                    </div>
                </div>
                <div class="row">
                    <div class="col-sm-4 text-muted">Cover Letter</div>
                    <div class="col-sm-8 bg-light p-3 rounded" style="white-space:pre-line;">{{ app.Message or 'No message provided.' }}</div>
                </div>
            </div>
        </div>
        
        {% if edu %}
        <div class="card border-0 shadow-sm">
            <div class="card-header bg-white font-weight-bold">Academic Record</div>
            <div class="card-body p-0">
                <table class="table mb-0 table-sm text-center">
                    <thead class="bg-light"><tr><th>Level</th><th>Board/Uni</th><th>Year</th><th>Score</th></tr></thead>
                    <tbody>
                        <tr><td>10th</td><td>{{ edu.SecondaryBoard }}</td><td>{{ edu.SecondaryBoardyop }}</td><td>{{ edu.SecondaryBoardper }}% ({{ edu.SecondaryBoardcgpa }} CGPA)</td></tr>
                        <tr><td>12th</td><td>{{ edu.SSecondaryBoard }}</td><td>{{ edu.SSecondaryBoardyop }}</td><td>{{ edu.SSecondaryBoardper }}% ({{ edu.SSecondaryBoardcgpa }} CGPA)</td></tr>
                        <tr><td>UG</td><td>{{ edu.GraUni }}</td><td>{{ edu.GraUniyop }}</td><td>{{ edu.GraUnidper }}% ({{ edu.GraUnicgpa }} CGPA)</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
        {% endif %}
    </div>

    <div class="col-lg-5">
        <div class="card border-0 shadow-sm mb-4">
            <div class="card-header bg-white font-weight-bold">Update Application Status</div>
            <div class="card-body bg-light">
                <form method="POST">
                    <div class="form-group">
                        <label class="font-weight-bold small">Current Status</label>
                        <select name="status" class="form-control" required>
                            <option value="New" {% if not app.Status %}selected{% endif %}>Under Review</option>
                            <option value="Sorted" {% if app.Status=='Sorted' %}selected{% endif %}>Shortlist (Sorted)</option>
                            <option value="Selected" {% if app.Status=='Selected' %}selected{% endif %}>Select Candidate</option>
                            <option value="Rejected" {% if app.Status=='Rejected' %}selected{% endif %}>Reject Candidate</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="font-weight-bold small">Message to Candidate (Visible to them)</label>
                        <textarea name="message" class="form-control" rows="3" placeholder="Provide feedback or next steps..."></textarea>
                    </div>
                    <button class="btn btn-primary btn-block">Confirm Status Update</button>
                </form>
            </div>
        </div>
        
        {% if msgs %}
        <div class="card border-0 shadow-sm">
            <div class="card-header bg-white font-weight-bold">Status History</div>
            <ul class="list-group list-group-flush small">
                {% for m in msgs %}
                <li class="list-group-item">
                    <div class="d-flex justify-content-between font-weight-bold">
                        <span>{{ m.Status }}</span><span class="text-muted">{{ m.ResponseDate }}</span>
                    </div>
                    <div class="mt-1">{{ m.Message }}</div>
                </li>
                {% endfor %}
            </ul>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}
""")

write_file('admin/view_company.html', """
{% extends 'admin/base.html' %}
{% block page_title %}{{ comp.CompanyName }}{% endblock %}
{% block content %}
<div class="row">
    <div class="col-md-4 mb-4">
        <div class="card border-0 shadow-sm text-center p-4">
            {% if comp.CompanyLogo %}
            <img src="{{ url_for('static', filename='uploads/' + comp.CompanyLogo) }}" class="mx-auto mb-3 rounded shadow-sm" style="width:100px; height:100px; object-fit:cover;">
            {% else %}
            <div class="bg-light text-muted mx-auto rounded d-flex align-items-center justify-content-center mb-3" style="width:100px; height:100px; font-size:2rem;"><i class="fas fa-building"></i></div>
            {% endif %}
            <h5 class="font-weight-bold">{{ comp.CompanyName }}</h5>
            <p class="text-muted small">{{ comp.CompanyAddress }}</p>
            <hr>
            <div class="text-left small">
                <div class="mb-2"><i class="fas fa-user text-primary mr-2" style="width:15px;"></i> {{ comp.ContactPerson }}</div>
                <div class="mb-2"><i class="fas fa-envelope text-primary mr-2" style="width:15px;"></i> {{ comp.CompanyEmail }}</div>
                <div class="mb-2"><i class="fas fa-phone text-primary mr-2" style="width:15px;"></i> {{ comp.MobileNumber }}</div>
                <div><i class="fas fa-globe text-primary mr-2" style="width:15px;"></i> <a href="{{ comp.CompanyUrl }}" target="_blank">Website</a></div>
            </div>
            <hr>
            <form action="{{ url_for('admin_delete_company', comp_id=comp.ID) }}" method="POST"><button class="btn btn-outline-danger btn-block btn-sm" onclick="return confirm('Are you sure you want to permanently delete this company and all its jobs?');"><i class="fas fa-trash mr-1"></i> Delete Company</button></form>
        </div>
    </div>
    <div class="col-md-8">
        <div class="card border-0 shadow-sm">
            <div class="card-header bg-white font-weight-bold">Posted Vacancies</div>
            <div class="card-body p-0">
                <table class="table table-hover align-middle mb-0">
                    <thead class="bg-light text-muted small"><tr><th>Job Title</th><th>Location</th><th>Salary</th><th>Openings</th><th>Deadline</th></tr></thead>
                    <tbody>
                        {% for v in vacs %}
                        <tr>
                            <td class="font-weight-bold">{{ v.JobTitle }}</td>
                            <td>{{ v.JobLocation }}</td>
                            <td>{{ v.MonthlySalary }}</td>
                            <td>{{ v.NoofOpenings }}</td>
                            <td class="text-danger">{{ v.LastDate }}</td>
                        </tr>
                        {% else %}
                        <tr><td colspan="5" class="text-center py-4 text-muted">No vacancies posted yet.</td></tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""")

write_file('admin/companies.html', """
{% extends 'admin/base.html' %}
{% block page_title %}Management: Companies{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
    <h5 class="mb-0">All Companies</h5>
    <a href="{{ url_for('admin_add_company') }}" class="btn btn-primary"><i class="fas fa-plus mr-1"></i> Add Company</a>
</div>
<div class="card border-0 shadow-sm"><div class="card-body p-0">
<table class="table table-hover align-middle mb-0">
  <thead class="bg-light"><tr><th>Logo</th><th>Company Name</th><th>Contact Person</th><th>Email</th><th>Actions</th></tr></thead>
  <tbody>
    {% for row in comps %}
    <tr>
      <td>{% if row.CompanyLogo %}<div style="width:40px;height:40px;background:#eee;border-radius:4px;overflow:hidden;"><img src="{{ url_for('static', filename='uploads/' + row.CompanyLogo) }}" class="w-100 h-100" style="object-fit:cover;"></div>{% else %}<div style="width:40px;height:40px;background:#eee;border-radius:4px;display:flex;align-items:center;justify-content:center;"><i class="fas fa-building text-muted"></i></div>{% endif %}</td>
      <td><div class="font-weight-bold">{{ row.CompanyName }}</div></td>
      <td>{{ row.ContactPerson }}</td>
      <td><a href="mailto:{{ row.CompanyEmail }}">{{ row.CompanyEmail }}</a></td>
      <td class="d-flex gap-2">
        <a href="{{ url_for('admin_view_company', comp_id=row.ID) }}" class="btn btn-sm btn-light text-primary mr-2"><i class="fas fa-eye"></i> View</a>
        <form action="{{ url_for('admin_delete_company', comp_id=row.ID) }}" method="POST"><button onclick="return confirm('Delete this company completely?');" class="btn btn-sm btn-light text-danger"><i class="fas fa-trash"></i></button></form>
      </td>
    </tr>
    {% else %}
    <tr><td colspan="100%" class="text-center py-4 text-muted">No records found.</td></tr>
    {% endfor %}
  </tbody>
</table>
</div></div>
{% endblock %}
""")

write_file('admin/add_company.html', """
{% extends 'admin/base.html' %}
{% block page_title %}Add New Company{% endblock %}
{% block content %}
<div class="card border-0 shadow-sm" style="max-width:800px;">
  <div class="card-body p-4">
    <form method="POST">
        <div class="row">
            <div class="col-md-6 mb-3"><label class="small font-weight-bold">Company Name</label><input type="text" name="company_name" class="form-control" required></div>
            <div class="col-md-6 mb-3"><label class="small font-weight-bold">Contact Person</label><input type="text" name="contact_person" class="form-control" required></div>
            <div class="col-md-6 mb-3"><label class="small font-weight-bold">Website URL</label><input type="text" name="company_url" class="form-control"></div>
            <div class="col-md-6 mb-3"><label class="small font-weight-bold">Mobile</label><input type="number" name="mobile" class="form-control" required></div>
            <div class="col-12 mb-3"><label class="small font-weight-bold">Headquarters Address</label><textarea name="address" class="form-control" rows="2" required></textarea></div>
            <div class="col-md-6 mb-4"><label class="small font-weight-bold">Login Email</label><input type="email" name="email" class="form-control" required></div>
            <div class="col-md-6 mb-4"><label class="small font-weight-bold">Default Password</label><input type="text" name="password" class="form-control" value="12345" required></div>
        </div>
        <button type="submit" class="btn btn-primary px-5">Register Company</button>
    </form>
  </div>
</div>
{% endblock %}
""")

write_file('admin/view_user.html', """
{% extends 'admin/base.html' %}
{% block page_title %}Candidate Profile{% endblock %}
{% block content %}
<div class="row">
    <div class="col-md-4 mb-4">
        <div class="card border-0 shadow-sm p-4 text-center">
            {% if user.Image %}
            <img src="{{ url_for('static', filename='uploads/' + user.Image) }}" class="mx-auto mb-3 rounded-circle shadow-sm" style="width:100px; height:100px; object-fit:cover;">
            {% else %}
            <div class="bg-primary text-white mx-auto rounded-circle d-flex align-items-center justify-content-center mb-3 font-weight-bold" style="width:100px; height:100px; font-size:2rem;">{{ user.FullName[0] }}</div>
            {% endif %}
            <h5 class="font-weight-bold">{{ user.FullName }}</h5>
            <div class="badge badge-light border mb-3">ID: {{ user.StudentID }}</div>
            <div class="text-left small bg-light p-3 rounded">
                <div class="mb-2"><strong>Email:</strong> {{ user.Email }}</div>
                <div class="mb-2"><strong>Mobile:</strong> {{ user.MobileNumber }}</div>
                <div class="mb-2"><strong>Gender:</strong> {{ user.Gender }}</div>
                <div class="mb-2"><strong>DOB:</strong> {{ user.DOB }}</div>
            </div>
            <form action="{{ url_for('admin_delete_user', user_id=user.ID) }}" method="POST"><button onclick="return confirm('Delete this user?');" class="btn btn-outline-danger btn-sm btn-block mt-3"><i class="fas fa-trash mr-1"></i> Delete Candidate</button></form>
        </div>
    </div>
    <div class="col-md-8 mb-4">
        <div class="card border-0 shadow-sm mb-4">
            <div class="card-header bg-white font-weight-bold">Academic Record</div>
            <div class="card-body p-0">
                {% if edu %}
                <table class="table mb-0 text-center">
                    <thead class="bg-light small"><tr><th>Level</th><th>Board/Uni</th><th>Year</th><th>Score</th></tr></thead>
                    <tbody>
                        <tr><td>10th</td><td>{{ edu.SecondaryBoard }}</td><td>{{ edu.SecondaryBoardyop }}</td><td>{{ edu.SecondaryBoardper }}%</td></tr>
                        <tr><td>12th</td><td>{{ edu.SSecondaryBoard }}</td><td>{{ edu.SSecondaryBoardyop }}</td><td>{{ edu.SSecondaryBoardper }}%</td></tr>
                        <tr><td>UG</td><td>{{ edu.GraUni }}</td><td>{{ edu.GraUniyop }}</td><td>{{ edu.GraUnidper }}%</td></tr>
                    </tbody>
                </table>
                {% else %}
                <div class="p-4 text-center text-muted">No education records provided by candidate.</div>
                {% endif %}
            </div>
        </div>
        
        <div class="card border-0 shadow-sm">
            <div class="card-header bg-white font-weight-bold">Recent Applications</div>
            <div class="list-group list-group-flush">
                {% for app in apps %}
                <div class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <div class="text-primary font-weight-bold">{{ app.JobTitle }}</div>
                        <span class="small text-muted">{{ app.ApplyDate }}</span>
                    </div>
                    <div class="small text-muted">{{ app.CompanyName }} &bull; Status: <strong>{{ app.Status or 'Under Review' }}</strong></div>
                </div>
                {% else %}
                <div class="p-4 text-center text-muted">Candidate hasn't applied to any jobs yet.</div>
                {% endfor %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
""")

print("Successfully flushed pending template updates!")
