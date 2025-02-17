# **📊 Momo API App**  

The **Momo API App** is a Django-based application that allows users to **upload their SMS transaction data (XML files)** and analyze their transactions. Users can view insightful **charts and summaries** of their mobile money transactions using **AJAX, Chart.js, and Django**.

---

## **🚀 Features**  
✔️ **User Authentication** (Register/Login)  
✔️ **Upload SMS Data (XML file)**  
✔️ **Automatic Transaction Processing & Analysis**  
✔️ **Visualize Data Using Charts** (Bar, Pie, Line, etc.)  
✔️ **Filter & View Transaction Details**  
✔️ **Secure SQLite Database Integration**  

---

## **🛠️ Technologies Used**  

- **Backend:** Python, Django, SQLite  
- **Frontend:** HTML, CSS, JavaScript, AJAX  
- **Charts:** Chart.js  
- **Data Processing:** XML Parsing  

---

## **🔧 Installation Guide**  

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/Phinatech/MTN_momo_project.git
cd MTN_momo_project
```

### **2️⃣ Create a Virtual Environment**  
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### **3️⃣ Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **4️⃣ Configure Database**

### **5️⃣ Apply Migrations**  
```bash
python manage.py migrate
```

### **6️⃣ Create a Superuser**  
```bash
python manage.py createsuperuser
```

### **7️⃣ Start the Development Server**  

```bash
python manage.py runserver
```
Visit **http://127.0.0.1:8000/** in your browser to access the app.

---

## **📂 Usage Instructions**  

1. **Register/Login** to your account.  
2. **Upload your XML file** containing SMS transaction data.  
3. The system will **process and analyze** your transactions.  
4. View transaction **history, summaries, and charts**.  

---

## **📊 Charts & Analysis**  

- **Bar Chart** → Transaction categories breakdown 
- **Donut Chart** → Number of transactions based on type  
- **Pie Chart** → Percentage distribution of transactions
- **Histogram Chart** → Frequency distribution of transactions  
- **Line Chart** → Spending trends over time  
- **Scatter Chart** → Amount variations  

---

## **🤝 Contributors**  

Tawe Kelvin
Charles Iheke
Chinemerem Judith Ugbo
shimwe Olivier
---

## **🛠️ Troubleshooting**  

## **📜 License**  
This project is licensed under the **MIT License**.  

---

Enjoy using **Momo API App**! 🎉🚀
