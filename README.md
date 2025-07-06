# 🚗 Yoyo Car AI

Yoyo Car AI is a Flask-based web application designed to predict vehicle-related values using NLP-powered models. It utilizes `spaCy` and `NLTK` to process input text and returns predictions in structured JSON format. Additionally, it generates various visual plots for enhanced data interpretation.

---

## 🧠 Features

- 🔍 **NLP Processing** using `spaCy` and `nltk`
- 🧾 **Prediction Output** in clean JSON format
- 📊 **Plot Generation** for insights (matplotlib/seaborn/plotly)
- 🌐 **Web Interface** powered by Flask
- 📁 Organized dataset and virtual environment support

---

## 📁 Project Structure

```

yoyo-car-ai/
├── .vscode/                 # VS Code settings
├── Dataset/                # Training or testing data
├── Include/...             # Python include files
├── Lib/site-packages/      # Installed packages (venv)
├── New folder/             # Placeholder folder (optional)
├── **pycache**/            # Compiled Python cache
├── .gitattributes          # Git configuration
├── README.md               # You're reading this!
├── pyenv.cfg               # Python virtual environment config
├── requirements.txt.txt    # Dependency list (rename properly)

````

---

## ⚙️ Setup Instructions

### 1. 🔧 Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate    # or .\venv\Scripts\activate on Windows
````

### 2. 📦 Install Dependencies

```bash
pip install -r requirements.txt.txt
```

> ⚠️ Rename the file to `requirements.txt` if needed.

---

## 🚀 Run the Flask App

```bash
python app.py
```

Access it in your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📤 Sample Output

```json
{
  "prediction": "High resale value",
  "confidence": 0.87,
  "brand": "Toyota",
  "year": 2021,
  "analysis": {
    "sentiment": "positive",
    "keywords": ["engine", "fuel efficiency"]
  }
}
```

---

## 📊 Plots Generated

* Price distribution per brand
* Year vs Value regression
* Keyword frequency histograms

---

## 🧪 Dependencies

* Flask
* spaCy
* nltk
* matplotlib / seaborn / plotly (based on config)
* pandas, numpy, etc.

---

## ✍️ Author

Developed by Jayasimma D
📧 Email: jayasimmamomdad@gmail.com (mailto:jayasimma@gmail.com)

---

## 📜 License

This project is licensed under the MIT License.

```

---

Would you like me to export this `README.md` into a downloadable file or also generate a sample `app.py` for the Flask interface?
```

 
