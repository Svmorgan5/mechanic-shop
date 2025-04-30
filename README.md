Mechanic Shop Management System
The Mechanic Shop Management System is a Python-based application designed to streamline the operations of a mechanic shop. It provides features for managing service tickets, mechanics, inventory, and more. The project includes a robust backend powered by Flask, SQLAlchemy, and Marshmallow for database management and API serialization. It also integrates with GitHub Actions for continuous integration and deployment.


Features
Service Ticket Management:

Create, update, and delete service tickets.
Assign mechanics and inventory parts to service tickets.
Mechanic Management:

Add, update, and remove mechanics.
Track mechanics assigned to service tickets.
Inventory Management:

Manage inventory items such as parts and tools.
Assign inventory items to service tickets.
Continuous Integration and Deployment:

Automated testing using unittest.
CI/CD pipeline with GitHub Actions for building, testing, and deploying the application.


Technologies Used
Backend:

Python
Flask
SQLAlchemy (ORM)
Marshmallow (Serialization and Validation)
Database:

SQLite (or any SQLAlchemy-supported database)
Testing:

unittest for unit testing.
CI/CD:

GitHub Actions for automated build, test, and deployment workflows.


GitHub Actions Workflow
The project includes a GitHub Actions workflow for CI/CD:

Build:

Installs dependencies and prepares the application environment.
Test:

Runs unit tests using unittest.
Deploy:

Deploys the application to production using the Render platform.
