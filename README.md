# 🚀 AWS Serverless Task Manager

A cloud-native task management application built using AWS serverless architecture with secure authentication, scalable APIs, and CI/CD automation.

---

## 📌 Overview

This project is a fully serverless task management application that allows users to securely manage their personal tasks.

Users can:

- Add tasks
- View tasks
- Update tasks
- Delete tasks

Each user can only access their own data using secure authentication.

---

## 🧱 Architecture

![Architecture](images/Architecture_diagram.png.png)

### Flow:

- Frontend hosted on **Amazon S3** and delivered via **CloudFront**
- **API Gateway** handles HTTP requests and validates JWT tokens
- **AWS Lambda** executes backend logic
- **DynamoDB** stores task data
- **Cognito** manages user authentication

---

## 🔐 Authentication Flow

1. User logs in via Amazon Cognito
2. Cognito returns a JWT token
3. Frontend stores the token
4. Token is sent in API requests
5. API Gateway validates the token
6. Lambda extracts user identity from the token

---

## 🔄 API Endpoints

| Method | Endpoint | Description         |
| ------ | -------- | ------------------- |
| POST   | /tasks   | Create a task       |
| GET    | /tasks   | Retrieve user tasks |
| PUT    | /tasks   | Update a task       |
| DELETE | /tasks   | Delete a task       |

---

## 🗄️ Database Design

**Table: TasksTable**

| Attribute | Type   |
| --------- | ------ |
| taskId    | String |
| task      | String |
| taskOwner | String |

### Global Secondary Index (GSI):

- Partition Key: `taskOwner`
- Enables efficient querying of user-specific tasks

---

## ⚡ Performance Optimization

- Replaced DynamoDB `scan()` with `query()`
- Implemented GSI for user-specific queries
- Reduced response latency by ~60–70%

---

## 🔐 Security

- Cognito JWT tokens used for API authorization
- User-specific data isolation using DynamoDB partition key
- Protected endpoints via API Gateway authorizer

---

## 🔄 CI/CD Pipeline

- Implemented using **GitHub Actions**
- On every push:
  - Lambda function is zipped
  - Automatically deployed to AWS

---

## 🌐 Deployment

- Frontend: **Amazon S3 + CloudFront**
- Backend: **AWS Lambda + API Gateway**

---

## 📸 Screenshots

![App Screenshot](images/login.png)
![App Screenshot](images/task_manger.png)

---

## 🎯 Key Features

- Secure user authentication (Cognito)
- Multi-user support
- Full CRUD operations
- Serverless architecture
- Automated deployment pipeline

---

## 🧠 Technologies Used

- AWS Lambda
- Amazon API Gateway
- Amazon DynamoDB
- Amazon Cognito
- Amazon S3
- Amazon CloudFront
- GitHub Actions
- Python (boto3)
- JavaScript (Fetch API)

---

## 🎤 Project Summary

Built a fully serverless task management application using AWS services including Cognito, API Gateway, Lambda, and DynamoDB. Implemented JWT-based authentication and enforced user-level access control for secure multi-user data isolation. Optimized database performance using a Global Secondary Index (GSI), reducing query latency by ~60%, and automated deployments using GitHub Actions CI/CD pipeline.

---

## 👨‍💻 Author

**Dhaksin Kaarthick**

---

## ⭐ Future Improvements

- Add task deadlines
- Add task status (completed/pending)
- Improve UI/UX
- Add notifications

---
