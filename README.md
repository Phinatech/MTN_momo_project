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
cd JudithMomoAPI
```

### **2️⃣ Create a Virtual Environment**  
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### **3️⃣ Install Dependencies**  
```bash
pip install -r requirements.txt  # Install all dependencies using a virtual environment
```

### **4️⃣ Install WeasyPrint**  

#### **For macOS:**  
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install gtk+3
brew install weasyprint
pip install cairocffi pycairo
export DYLD_LIBRARY_PATH="/usr/local/lib:$DYLD_LIBRARY_PATH"
```

#### **For Windows:**  
1. Download and install **GTK+3** from [GTK Windows Installers](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases)
2. Add GTK+3 to the **system PATH**
3. Install WeasyPrint:
   ```bash
   pip install weasyprint cairocffi
   ```

### **5️⃣ Make Migrations**
```bash
python manage.py makemigrations
```

### **6️⃣ Apply Migrations**  
```bash
python manage.py migrate
```

### **7️⃣ Create a Superuser**  
```bash
python manage.py createsuperuser  # Create a superuser with your email and password
```

### **8️⃣ Collect Static Files**  
```bash
python manage.py collectstatic  
```

### **9️⃣ Start the Development Server**  
```bash
python manage.py runserver  # Start the Development Server on the specified port
```
Visit **http://127.0.0.1:8000/** in your browser to access the app. # May be different depending on the port you are using

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

## **🤝 Contributing**  

Want to contribute? Feel free to fork the repo and submit a **Pull Request (PR)**! 🚀  

---

## **🛠️ Troubleshooting**  

---

## **📜 License**  
This project is licensed under the **MIT License**.  

---

Enjoy using **Momo API App**! 🎉🚀