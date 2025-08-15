# 🚗 NovaDrive Rentals

**NovaDrive Rentals** is a full-stack car rental management system built using **Python (Flask)** for the backend and **HTML/CSS** with **Jinja templates** for the frontend. It supports two user roles—**Admin (Company Owner)** and **Regular Users**—for seamless vehicle booking, management, and status tracking.

---


## 🚀 Live Demo

https://nova-drive-rentals.onrender.com

---

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Backend:** Python, Flask
- **Database:** SQLite
- **Tools:** Git, GitHub, Render (for deployment)

---

## 👥 Features

### 🔑 User
- Register & login
- Browse available cars
- Submit car rental requests
- View rental history

### 🧑‍💼 Admin (Company Owner)
- Admin login
- Add, update, and delete cars
- View booking history
- Change car status: "Available", "Renting in Progress", "Car Rented"

---

## 📂 Folder Structure
NovaDriveRentals/
├── static/
│ ├── css/
│ └── images/
├── templates/
│ ├── index.html
│ ├── login.html
│ ├── register.html
│ ├── dashboard.html
│ └── admin_dashboard.html
├── app.py
├── requirements.txt
├── README.md


---

## 🚀 Getting Started (Run Locally)

- Clone this repo: `git clone https://github.com/Panashe2217/NovaDriveRentals.git`
- Navigate inside: `cd NovaDriveRentals`
- (Optional) Set up virtual environment:
  - `python -m venv venv`
  - Activate it:
    - On Windows: `venv\Scripts\activate`
    - On macOS/Linux: `source venv/bin/activate`
- Install packages: `pip install -r requirements.txt`
- Start the app: `python app.py`
- Open your browser and go to: [http://localhost:5000](http://localhost:5000)
🔐 Admin Test Credentials

Email: admin@novadrive.com
Password: admin123
Update or change this in your database as needed.

🎯 To-Do / Future Features
Payment gateway integration (e.g., Stripe)

Email confirmations for bookings

Responsive design for mobile

PDF invoice generation

👩‍💻 Author
Panashe Emma Nkume
💌 panashenkume@gmail.com
🔗 LinkedIn
https://www.linkedin.com/in/panashe-nkume-086215257/
💻 GitHub
https://github.com/Panashe2217/

📄 License
This project is licensed under the MIT License.
