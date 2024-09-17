# Customer Management System

## Introduction

The **Customer Management System** is a robust platform designed to help businesses manage their customer base, orders, and support queries. The system provides an admin panel for managing customers, orders, and products, as well as a user interface for customers to track their own orders and profile settings. It is ideal for businesses that want to streamline operations and improve customer satisfaction.

**Features** include:
- **Customer Profiles**: View and update customer details and track their order history.
- **Order Management**: Create, update, and delete customer orders, and track the status of each order.
- **Support Portal**: Provide efficient customer support by integrating a contact form that sends queries to the support team.
- **User Authentication**: Secure login and registration system with role-based access for admins and customers.

Explore the live application here: [Deployed Site](#)

Read more about the development of this project: [Final Project Blog Article](#)

Connect with me: [LinkedIn](#)

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/customer-management-system.git
  
2. Navigate into the project directory:
   ```
   cd customer-management-system
3. Set up a virtual environment:
   ```
   python3 -m venv env
    source env/bin/activate   # On Windows, use `env\Scripts\activate`
4. Install the required dependencies
   ```
   pip install -r requirements.txt
5. Set up environment variables by creating a .env file and adding:
   ```
     DEBUG=True
    SECRET_KEY=your_secret_key
    EMAIL_HOST=your_smtp_server
    EMAIL_HOST_USER=your_email
    EMAIL_HOST_PASSWORD=your_email_password
    SUPPORT_EMAIL=support_email@example.com

6. Apply migrations
   ```
   python manage.py migrate
7. Create a superuser for accessing the admin panel
   ```
   python manage.py createsuperuser
8. Run the development server:
   ```
   python manage.py runserver

## Usage
  ### Key Features
    Customer Profiles: Each user has a profile page where they can view and update their personal details. 
    Admins can also view and update customer profiles.
    Order Management: Admins can create, update, or delete orders for any customer. 
    The status of orders (e.g., delivered, pending, out for delivery) is tracked in the system.
    Support Portal: Customers can submit support requests using the contact form. These requests are emailed directly to the support team.

## Usage Guidelines
   Log in with your credentials.
   
   For admins, you can access the Dashboard to manage customers, products, and orders.
  
   For customers, you can view and update your personal information via the Account Settings page, track your orders, and contact support if needed.

## License
  This project is licensed under the MIT License.


