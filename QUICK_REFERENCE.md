# 🗂️ QUICK REFERENCE GUIDE

## 🌐 URL ROUTES

### Authentication
- `GET/POST /accounts/login/` → User login
- `GET/POST /accounts/signup/` → User registration
- `POST /accounts/logout/` → User logout

### Dashboard & Home
- `GET /` → Landing page (public)

### Teacher Routes
| URL | Purpose | Method |
|-----|---------|--------|
| `/teachers/dashboard/` | Teacher dashboard | GET |
| `/teachers/profile/` | View/edit teacher profile | GET, POST |
| `/teachers/manage-students/` | List all students | GET |
| `/teachers/add-student/` | Add new student | GET, POST |
| `/teachers/edit-student/<id>/` | Edit student | GET, POST |
| `/teachers/delete-student/<id>/` | Delete student | POST |
| `/teachers/mark-attendance/` | Mark attendance | GET, POST |
| `/teachers/view-attendance/` | View attendance records | GET |
| `/teachers/add-marks/` | Add marks | GET, POST |
| `/teachers/view-marks/` | View all marks | GET |

### Student Routes
| URL | Purpose | Method |
|-----|---------|--------|
| `/students/dashboard/` | Student dashboard | GET |
| `/students/profile/` | View/edit profile | GET, POST |
| `/students/attendance/` | View own attendance | GET |
| `/students/results/` | View own results | GET |

### Course Routes
| URL | Purpose | Method |
|-----|---------|--------|
| `/courses/` | List courses | GET |
| `/courses/add/` | Add course | GET, POST |
| `/courses/edit/<id>/` | Edit course | GET, POST |
| `/courses/delete/<id>/` | Delete course | POST |

### Attendance Routes
| URL | Purpose | Method |
|-----|---------|--------|
| `/attendance/report/` | Attendance report (teacher) | GET |
| `/attendance/my-attendance/` | My attendance (student) | GET |

### Marks/Results Routes
| URL | Purpose | Method |
|-----|---------|--------|
| `/marks/add/` | Add result | GET, POST |
| `/marks/teacher/` | View all results | GET |
| `/marks/edit/<id>/` | Edit result | GET, POST |
| `/marks/delete/<id>/` | Delete result | POST |

---

## 🎯 QUICK TEST PATH

### 1️⃣ As Teacher (teacher1/teacher123)
```
1. Go to /teachers/dashboard/ → See stats
2. Go to /teachers/manage-students/ → View student1
3. Go to /teachers/add-student/ → Add new student
4. Go to /teachers/mark-attendance/ → Mark attendance
5. Go to /marks/add/ → Add marks for student
```

### 2️⃣ As Student (student1/student123)
```
1. Go to /students/dashboard/ → See quick stats
2. Go to /students/attendance/ → View attendance records
3. Go to /students/results/ → View marks and grades
```

### 3️⃣ As Admin (admin/admin123)
```
1. Go to /admin/ → Django admin panel
2. Manage all users, courses, attendance, marks
```

---

## 📊 MODELS QUICK REFERENCE

### User (accounts.User)
```python
- email (unique)
- username (unique)
- first_name
- last_name
- role (1=Teacher, 2=Student)
- is_active
- is_staff
```

### TeacherProfile
```python
- user (OneToOne)
- employee_id
- subject
- qualification
- experience
- bio
- profile_picture
```

### StudentProfile
```python
- user (OneToOne)
- roll_number
- college_id
- course (FK)
- about
- profile_picture
```

### Course
```python
- name
- code
- duration_months
- description
```

### Subject
```python
- course (FK)
- name
- code
```

### Attendance
```python
- student (FK)
- date
- is_present
- remarks
- created_at
- updated_at
```

### Result
```python
- student (FK)
- subject (FK)
- marks (0-100)
- grade (auto-calculated: A/B/C/D/F)
- remarks
- created_at
- updated_at
```

---

## 🔑 KEY FUNCTIONS

### Authentication
```python
request.user.is_teacher()  # Check if teacher
request.user.is_student()  # Check if student
authenticate(username, password)  # Login
```

### Decorators Used
```python
@login_required(login_url='login')  # Require login
@require_http_methods(["GET", "POST"])  # Restrict methods
```

### Queries
```python
# Get all students
StudentProfile.objects.all()

# Get student by user
StudentProfile.objects.get(user=request.user)

# Get attendance for date
Attendance.objects.filter(date=date_value)

# Get results for student
Result.objects.filter(student=student)
```

---

## 🎨 TEMPLATE STRUCTURE

### Base Template (`base.html`)
- Navigation bar
- User info
- Messages display
- CSS Bootstrap 5

### Other Templates
```
accounts/
  ├── login.html
  ├── signup.html
  └── home.html

teachers/
  ├── dashboard.html
  ├── manage_students.html
  ├── add_student.html
  ├── edit_student.html
  ├── mark_attendance.html
  ├── view_attendance.html
  ├── add_marks.html
  ├── view_marks.html
  └── profile.html

students/
  ├── dashboard.html
  ├── profile.html
  ├── attendance.html
  └── results.html

courses/
  ├── list.html
  └── form.html
```

---

## 🚀 PERFORMANCE TIPS

✅ Using `.select_related()` for foreign keys
✅ Using `.filter()` instead of looping
✅ Database queries in views
✅ Templates with efficient loops

---

## 🔒 SECURITY CHECKLIST

✅ CSRF tokens on all forms
✅ Login required on protected views
✅ Role-based access control
✅ XSS protection (template escaping)
✅ No hardcoded credentials
✅ Password hashing (Django)
✅ SQL injection protection (ORM)

---

## 📱 RESPONSIVE DESIGN

✅ Bootstrap 5 grid system
✅ Mobile-friendly tables
✅ Hamburger menu (auto from Bootstrap)
✅ Flexible card layouts
✅ Touch-friendly buttons

---

## 💡 CUSTOMIZATION TIPS

### Change landing page:
Edit `/templates/accounts/home.html`

### Modify color scheme:
Add custom CSS in base.html `<style>` tag

### Add new fields to models:
1. Edit model in `models.py`
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`
4. Update forms and templates

### Add new view:
1. Create function in `views.py`
2. Add to `urls.py`
3. Create template
4. Add link in navigation

---

## 📞 TROUBLESHOOTING

| Error | Solution |
|-------|----------|
| "Page not found (404)" | Check URL spelling and names in urls.py |
| "Not Authorized (403)" | Check if user has correct role |
| "Template not found" | Check template path and file exists |
| "No such table" | Run `python manage.py migrate` |
| "Module not found" | Check imports and INSTALLED_APPS |

---

## 🎓 LEARNING RESOURCES

- [Django Official Docs](https://docs.djangoproject.com/)
- [Bootstrap 5](https://getbootstrap.com/)
- [Python Official](https://www.python.org/)

---

*Happy Learning! 🚀*
