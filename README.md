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

## Implemented Endpoints
### 1. Data Processing
- Load Dataset:
Returns the content of the Iris dataset in JSON format.

![alt text](<TP2 and  3/data/images/load_data2.png>)

- Clean Dataset:
Cleans the dataset to prepare it for training.

![alt text](<TP2 and  3/data/images/clean_data2.png>)

- Split Train/Test:
Splits the dataset into training and testing sets.

![alt text](<TP2 and  3/data/images/split_data2.png>)


- Train Model:
Trains a classification model and saves it.

![alt text](<TP2 and  3/data/images/train_data2.png>)

- Predict:
Generates predictions using the saved model.

![alt text](<TP2 and  3/data/images/predict_data2.png>)


## Firestore Integration
- Create Firestore Collection:
Creates a Firestore collection parameters with a document containing n_estimators and criterion.

![alt text](<TP2 and  3/data/images/create_collection.png>)

- Retrieve Parameters:
Returns parameters stored in Firestore.

![alt text](<TP2 and  3/data/images/params.png>)

- Update Parameters:
Updates or adds parameters in Firestore.

![alt text](<TP2 and  3/data/images/param_1.png>)

![alt text](<TP2 and  3/data/images/param2_aprèsModif.png>)

## Authentication
- Register User:
Registers a new user with a specific role.
(there are sensitive data (password, token) I prefer not to put a capture )

- User Login:
Authenticates a user and generates a JWT token.

(there are sensitive data (password, token) I prefer not to put a capture )

- List Users (Admin Only):
Returns a list of users, accessible only to administrators.

![alt text](<TP2 and  3/data/images/list_user.png>)


4. Error Handling
- Custom 404 Error:
Custom error responses provide meaningful messages for 404 errors.

(see code in app.py)

5. DoS Protection
- Rate Limiting:
Limits the number of requests a user can make within a given time frame.

(see code in app.py)

6. API testing