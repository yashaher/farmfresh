# FarmFresh – Farm-to-Table E-Commerce Platform  

## Description  
**FarmFresh** is an innovative e-commerce platform that connects farmers directly with customers, enabling the purchase of fresh produce while promoting local farm tourism. 
It ensures a seamless shopping experience with secure transactions and efficient order management.  

## Features  
- **Fresh Produce Marketplace**: Buy fresh farm products directly from local farmers.  
- **User Authentication**: Secure login and registration system for farmers and customers.  
- **Subscription Plans**: Customers can subscribe to fresh produce deliveries.  
- **Order Tracking**: View and manage order statuses in real-time.  
- **Farm Tourism Module**: Book farm visits, explore farming activities, and engage in farm-tourism experiences.  
- **Responsive UI**: Fully optimized for mobile and desktop users.  

## Tech Stack  
### **Back-end**  
- Python (Django) – Ensures secure and efficient database handling.  
- PostgreSQL / SQLite – Stores user, order, and product data.  
- Django REST Framework – API development for seamless communication.  

### **Front-end**  
- HTML, CSS, Bootstrap – Responsive and user-friendly design.  
- JavaScript – Ensures interactive user experiences.  

## Installation  

```sh
# Clone the repository
git clone https://github.com/yashaher/farmfresh.git

# Navigate into the project directory
cd farmfresh

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver
