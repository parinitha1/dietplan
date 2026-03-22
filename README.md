# 🥗 Diet Plan Management System

A web-based application built with **Flask** and **SQLAlchemy** to help users track their health metrics and access personalized diet recommendations. The system calculates **Body Mass Index (BMI)** and provides specific meal plans based on dietary preferences (**Vegetarian, Non-Vegetarian, or Vegan**).

---

## Features

* **User Authentication**
  Secure registration and login system.

* **Health Profiles**
  Store user details including age, height, and weight.

* **BMI Analysis**
  Automated calculation and classification of health status:

  * Underweight
  * Normal
  * Overweight
  * Obese

* **Personalized Diet Plans**
  Specific meal guides for **12 different categories**
  *(4 BMI levels × 3 diet types)*

* **Database Management**
  Built-in **SQLite integration** to save and update user progress over time.

---

## Project Structure

```
├── main.py                # Flask application logic and database models
├── instance/
│   └── users.db           # SQLite database file
├── static/
│   └── images/            # UI assets and illustrations
└── templates/             # HTML Frontend
    ├── create_account.html
    ├── login.html
    ├── home1.html          # Profile input form
    ├── update_details.html # Update existing metrics
    ├── dietplan.html       # Diet selection matrix
    ├── result.html         # BMI output display
    └── [category]_[diet].html # 12 specific diet plan pages
```

---

## ⚙️ Setup and Installation

### 1. Prerequisites

Ensure you have **Python 3.x** installed on your system.

### 2. Install Dependencies

Run the following command:

```bash
pip install flask flask-sqlalchemy
```

### 3. Run the Application

```bash
python main.py
```

Open your browser and navigate to:

```
http://127.0.0.1:5000
```

---

##  Usage Guide

* **Register**
  Create an account with a username and password.

* **Input Metrics**
  Enter your:

  * Age
  * Height (cm)
  * Weight (kg)
  * Gender

* **View Results**
  The system calculates your **BMI** and displays your weight category.

* **Choose Diet**
  Navigate to the diet plan matrix and select **"Show"** for your category and preferred diet type:

  * Veg
  * Non-Veg
  * Vegan

* **Update Details**
  Use the **"Update Details"** feature if your metrics change to get a recalculated plan.

---

##  Tech Stack

* **Backend:** Flask
* **Database:** SQLite (via SQLAlchemy)
* **Frontend:** HTML, CSS
