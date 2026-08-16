# 🎓 Student Academic Success Predictor

A machine learning web application that predicts a student's expected **HSSC-II academic grade** using academic performance, attendance, and family educational background.

Built with **Python, scikit-learn, and Streamlit**.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![scikit--learn](https://img.shields.io/badge/scikit--learn-ML-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Overview

This project demonstrates an end-to-end machine learning workflow:

- Exploratory Data Analysis (EDA)
- Data cleaning and preprocessing
- Feature engineering and feature selection
- Class imbalance handling using SMOTE
- Training and comparing classification models
- Random Forest classification
- Interactive Streamlit web application

---

## ✨ Features

- 🎓 Academic grade prediction
- 📊 Prediction confidence for all grade classes
- 📝 Student input summary
- 🤖 Machine learning powered predictions
- 🎨 Custom Streamlit interface
- 📈 Transparent prediction results

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Language | Python 3.10+ |
| Machine Learning | scikit-learn |
| Data Processing | pandas, numpy |
| Class Balancing | imbalanced-learn (SMOTE) |
| Visualization | matplotlib, seaborn |
| Web Application | Streamlit |
| Model Persistence | joblib |

---

## 📁 Project Structure

```text
Student-Academic-Success-Predictor/
│
├── .streamlit/
│   └── config.toml
│
├── .gitignore
├── Student_Performance.ipynb
├── student_performance.csv
├── app.py
│
├── student_grade_model.pkl
├── preprocessor.pkl
├── scaler.pkl
├── selected_features.pkl
│
├── requirements.txt
├── LICENSE
└── README.md
```

---

## ⚙️ How to Run

### 1. Open the project folder

Open the project folder in **VS Code** or Command Prompt.

### 2. Install Streamlit

```bash
python -m pip install streamlit
```

### 3. Run the application

```bash
python -m streamlit run app.py
```

The application will open in your browser at:

```text
http://localhost:8501
```

### To stop the application

Press:

```text
Ctrl + C
```

---

## 📊 Machine Learning Workflow

The project follows these main steps:

**Data → Preprocessing → Feature Engineering → Feature Selection → SMOTE → Model Training → Prediction**

### Feature Selection

Three methods were used:

- Random Forest Feature Importance
- Chi-Square
- Mutual Information

### Class Balancing

**SMOTE (Synthetic Minority Oversampling Technique)** was applied to help handle class imbalance in the training data.

---

## 🤖 Model

The final prediction model is a:

**Random Forest Classifier**

- 100 trees
- Maximum depth: 22
- SMOTE for class balancing
- Selected features used for prediction

The trained model and preprocessing components are saved using **joblib** so the Streamlit application can make predictions without retraining the model.

---

## ⚠️ Model Limitation

The dataset contains **6 grade classes**, meaning random guessing gives a baseline of approximately **16.7% accuracy**.

The current model achieves approximately **17% accuracy**, which is only slightly above this baseline.

This suggests that the available dataset has a weak statistical relationship between the input features and the target grade.

This limitation is documented in the machine learning notebook rather than hidden.

---

## 🚀 Future Improvements

- Use a larger and more reliable dataset
- Improve feature engineering
- Experiment with XGBoost and LightGBM
- Add prediction confidence warnings
- Add SHAP-based model explainability
- Improve overall prediction performance

---

## 📄 License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.

---

## 👩‍💻 Author

**Tooba Hashim**

Student Academic Success Prediction System  
Machine Learning Project