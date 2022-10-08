# Description

<!-- [![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier) -->

> This is a e-commerce website i developed while learning Django webframework.

## Overview
<img src="https://raw.githubusercontent.com/clevrf0x/BlueBag/main/git_assets/bluebag_overview.gif">

---

### Technologies :
- Django
- Bootstrap
- PostgreSQL
- RazorPay Payment Gateway

### Features :
> User 
- Login, Signup and Reset Password
- Search Functionality
- Pagination
- Product Filter (Category based)
- Product Variation
- Payment Gateway (Razorpay)
- View Previous Orders and Bills
- Cancel Orders (User)
- Change Password

> Admin
- Ban and Unban Users
- Add, Delete and Update Products
- Add, Delete and Update Categories
- Add, Delete and Update Variations
- Order Management (Status Update)
- Change Password


# Setup project locally

## Prerequisits

Before cloning/forking this project, make sure you have the following tools installed:

- [Git](https://git-scm.com/downloads)
- [PostgreSQL](https://www.postgresql.org/download/)
- [Python 3.7+](https://www.python.org/downloads/)


## Installation

1. Clone the project\
>`git clone https://github.com/clevrf0x/BlueBag`
2. Create a .env file in BlueBag directory (create inside the directory where settings.py resides)
>Format :\
\
`SECRET_KEY=<DJANGO_SECRET_KEY>`\
`DATABASE_NAME=<DB_NAME>`\
`DATABASE_USER=<DB_USERNAME>`\
`DATABASE_PASS=<DB_USER_PASSWORD>`\
`DATABASE_HOST=<DB_HOST>`\
`DATABASE_PORT=<DB_PORT>`\
`EMAIL_HOST_USER=<EMAIL_HOST_ADDRESS (GMAIl)>`\
`EMAIL_HOST_PASS=<GMAIL_APP_PASSWORD>`\
`RAZOR_KEY_ID=<RAZORPAY_API_KEY>`\
`RAZOR_KEY_SECRET=<RAZORPAY_API_SECRET_KEY>`\
\
`# Add Values without <> brackets`
3. Setup PostgreSQL according to .env file (Create DB, Change user password...etc)
4. Navigate to the project directory
>`cd BlueBag`
5. Create a virtual environment and activate it
> `# for windows`\
  `python -m venv env`\
  `env\Scripts\activate.ps1`\
  \
  `# for linux or mac`\
  `python3 -m venv env`\
  `source env/bin/activate`\
  \
  `# to exit virtual environment type 'deactivate'`
6. Install Dependancies using pip
> `pip install -r requirements.txt`
7. Migrate Database Models
> `python manage.py migrate`
8. Create a Super User Account
> `python manage.py createsuperuser`
9. Start Application
> `python manage.py runserver`

---

## Contributors

[//]: contributor-faces

<a href="https://github.com/clevrf0x"><img src="https://avatars.githubusercontent.com/u/52382725?v=4" style="border-radius: 50px" title="Favas M" width="80" height="80"></a>

[//]: contributor-faces