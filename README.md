# CareerCatalyst – College Placement Management System

## Overview

CareerCatalyst is a web-based College Placement Management System developed to automate and streamline the placement process within educational institutions. The platform acts as a centralized hub connecting students, placement officers, and recruiting companies.

The system eliminates manual placement management by providing digital workflows for job postings, student applications, applicant tracking, and recruitment monitoring.

Built using Flask, SQLAlchemy, HTML, CSS, and JavaScript, CareerCatalyst offers an efficient, transparent, and organized placement management experience.

---

## Key Features

### Student Module

Students can:

* Register and log in securely
* Manage personal and academic profiles
* View available companies and job opportunities
* Apply for eligible positions
* Track application progress and status
* Receive personalized company recommendations

### Company Management Module

The system allows administrators to:

* Add and manage company information
* Maintain company profiles and recruitment details
* Define eligibility criteria and job requirements
* Display company-specific information to students
* Manage recruitment opportunities

### Admin Module

Placement administrators can:

* Manage student records
* Manage company profiles
* Monitor student applications
* Track recruitment activities
* Maintain placement-related data
* Access placement statistics and reports

### Application Management

* Online job application system
* Centralized application tracking
* Organized applicant management
* Efficient recruitment workflow

### Authentication System

* Secure user registration
* Login and logout functionality
* Role-based access control
* Protected dashboard access
* Session management and authentication

### Dashboard System

#### Student Dashboard

* View available companies
* Access recommended opportunities
* Monitor application activities
* Manage profile information

#### Admin Dashboard

* Overview of registered students
* Company management interface
* Placement monitoring tools
* Recruitment statistics and insights

---

## Project Objectives

* Automate the college placement process
* Reduce paperwork and administrative workload
* Improve communication between students and placement officers
* Provide transparency throughout recruitment activities
* Centralize placement-related information
* Enhance efficiency and data accuracy

---

## Technology Stack

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python
* Flask

### Database

* SQLite
* SQLAlchemy ORM

---

## System Architecture

CareerCatalyst follows a three-tier architecture:

### Presentation Layer

* HTML Templates
* CSS Styling
* JavaScript Functionality

### Application Layer

* Flask Framework
* Business Logic
* Authentication System
* Routing and Request Handling

### Data Layer

* SQLite Database
* SQLAlchemy ORM
* Data Models and Relationships

---

## Project Structure

```text
CareerCatalyst/
│
├── app.py
├── models.py
├── forms.py
├── requirements.txt
├── README.md
├── .gitignore
├── LICENSE
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── script.js
│   │
│   └── images/
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── student_dashboard.html
│   ├── admin_dashboard.html
│   ├── companies.html
│   ├── company_detail.html
│   └── recommendation.html
│
└── instance/
```

---

## Template Overview

### `index.html`

Landing page of the application that introduces the platform and provides navigation to authentication pages.

### `login.html`

Allows registered users to securely access the system.

### `register.html`

Provides new users with account registration functionality.

### `student_dashboard.html`

Displays student-specific information, available companies, recommendations, and application-related activities.

### `admin_dashboard.html`

Provides administrators with placement management tools, statistics, and system monitoring capabilities.

### `companies.html`

Displays a list of available companies participating in the placement process.

### `company_detail.html`

Shows detailed information about a selected company, including recruitment details and eligibility criteria.

### `recommendation.html`

Provides personalized company recommendations based on student profiles and qualifications.

### `base.html`

Common layout template used across all pages to maintain consistent design and navigation.

---

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/CareerCatalyst.git
```

### Navigate to Project Directory

```bash
cd CareerCatalyst
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python app.py
```

### Access the Application

Open your browser and visit:

```text
http://127.0.0.1:5000
```

---

## Benefits of the System

* Streamlined placement management
* Faster recruitment workflow
* Improved data organization
* Reduced manual errors
* Better tracking of placement activities
* Enhanced transparency and accessibility
* Centralized information management

---

## Future Enhancements

* Email notifications and alerts
* Resume upload and management
* Resume parsing and screening
* Interview scheduling system
* Advanced placement analytics
* AI-powered job recommendations
* Company portal integration
* Exportable placement reports

---

## Learning Outcomes

This project demonstrates practical knowledge of:

* Full Stack Web Development
* Flask Framework
* Database Design and Management
* SQLAlchemy ORM
* Authentication and Authorization
* Template Inheritance
* Software Engineering Principles
* Web Application Development

---
