# **Creating an API with FastAPI**

## **Introduction**
This project involves developing an API using **FastAPI** to encapsulate data processing and machine learning model execution logic. The API uses the famous Iris dataset from Kaggle to predict flower classes.

The API follows fundamental **REST** principles and includes advanced features such as JWT authentication, user management, Firestore integration, error handling, rate limiting, and API versioning.

![alt text](<TP2 and  3/data/images/vue_ensemble.png>)

---

## **Core Features**
1. **Data Processing**
   - Load and clean data from the Iris dataset.
   - Split data into training and testing sets.
   - Train and save a machine learning model.
   - Generate predictions using the trained model.

2. **Firestore Integration**
   - Create and manage a Firestore collection for storing model parameters (`n_estimators`, `criterion`).
   - Add, update, and retrieve parameters from Firestore.

3. **Security and Authentication**
   - JWT-based authentication using Firestore.
   - User management, including registration, login, and role-based access control (e.g., admin/user).
   - Rate limiting to protect the API from DoS attacks.

---





