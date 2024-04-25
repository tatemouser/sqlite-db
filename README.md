# SQLITE LIBRARY DATABASE

## Table of Contents

- [Features](#features)
- [Project Description](#project-description)
- [Installation](#installation)
- [License](#license)
- [Contact](#contact)
  
## Features
- Role-based access control for librarians and patrons.
- Various techniques to prevent SQL injection
- Password hashing 
- Backend built with Flask framework.
- Integration of SQLite as backend database management system.
- AJAX requests for dynamic frontend interaction.
- Database initialization with user, item, and checkout tables.
- Dummy data insertion for demonstration purposes.
- HTML templates for frontend rendering.
- AJAX requests for dynamic interaction.
- Additional error handling measures for system robustness.


## Project Description
Simple database application for library management system. System has two types of users: Librarian and Patron.

**Database Initialization:**
Upon initialization, the system creates essential tables for users, items, and checkouts. 
Dummy data is inserted to demonstrate functionality.

**Security Measures:** 
The system incorporates robust security measures to safeguard sensitive data, including role-based access control to prevent unauthorized 
access. All inputs are safeguarded with parameterized queries and input validation to prevent SQL injection.
User passwords are protected with strong hashing techniques.

**Backend Architecture:**
Built with the Flask framework in Python, the backend seamlessly integrates SQLite as the database management system, ensuring 
efficient data storage and retrieval.

**Frontend Interface:**
The frontend utilizes HTML templates for rendering, providing a user-friendly interface for librarians and patrons. AJAX requests enable 
dynamic interaction and seamless page updates.



#### Patron Functions:
  - Search for library items by title.
  - Checkout library items.
  - View checked out items.
#### Librarian Functions:
  - Manage user accounts, library items, and checkouts.
  - Add librarian accounts and patron accounts.
  - Search for library items by title.
  - Add various types of library items, including books, CDs, and DVDs.
  - Display all users, including librarians and patrons.
  - Search for users by library ID.
  - View user checkout items.

#### User Interface

<div style="display: flex; justify-content: space-between;">
    <img src="https://github.com/tatemouser/sqlite-db/blob/master/Assets/LibraryPage1.png" alt="LibraryPage1" width="300" height="250">
    <img src="https://github.com/tatemouser/sqlite-db/blob/master/Assets/LibraryPage2.png" alt="LibraryPage2" width="300" height="250">
    <img src="https://github.com/tatemouser/sqlite-db/blob/master/Assets/LibraryPage3.png" alt="LibraryPage3" width="300" height="250">
</div>

  
## Installation
    git clone https://github.com/tatemouser/sqlite-db.git

## License
None.


## Contact
tatesmouser@gmail.com

https://tatemouser.com/
 
