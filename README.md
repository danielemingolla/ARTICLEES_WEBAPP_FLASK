<p align="center">
  <a href="https://www.danielemingolla.site"><img src="https://i.ibb.co/1JXvqLz/mockuplogo.png" alt="mockuplogo" border="0"></a>

  # <u>ARTICLEE</u> - Web App with CRUD functionality
Articlee is a web application using the Python Flask micro-framework that completely supports user authentication and registration. There is a page with a list of all the articles that users are wrote and for each user there's a profile where is possible to create, edit or remove their own articles. It is also possible to upload an avatar to differentiate each user, it's completely responsive and thanks to SQLAlchemy it's adaptable with a long list of different databases. It's also support payments with Stripe and it includes a fake-shop to simulate purchases.

  # Preview
  ![Alt Text](https://media.giphy.com/media/TfdoVc14yKl80pZyQ3/giphy.gif)
</p>

# Next Features
- [X] SLQAlchemy Support
- [X] Add an avatar for each user
- [X] Accepting Payments with Stripe
- [X] Email Support
- [X] Full responsive

# Requirements
```
  Flask==1.1.1


  Flask extension:

  Flask-Email==1.4.4
  Flask-Login==0.4.1
  Flask-Mail==0.9.1
  Flask-Migrate==2.5.2
  Flask-Script==2.0.6


  Data and workers:

  mysql==0.0.2
  mysql-connector-python==8.0.17
  mysqlclient==1.4.4
  Flask-MySQL==1.4.0
  Flask-MySQLdb==0.2.0
  Flask-SQLAlchemy==2.4.0
  SQLAlchemy==1.3.7


  Forms:

  WTForms==2.2.1
  Flask-WTF==0.14.2


  Testing and static analysis:

  flake8==3.7.8


  CLI:

  Click==7.0


  Payments:

  stripe==2.35.1


  Utilities:

  Faker==2.0.1
  Pillow==6.1.0
  passlib==1.7.1
```
# How to running the app
 ```
 python app.py
 ```
