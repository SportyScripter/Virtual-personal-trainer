# Virtual Personal Trainer (VPT)

<p align="center">
  <img src="https://placehold.co/800x200/1a202c/718096?text=Virtual+Personal+Trainer" alt="Project Banner">
</p>

<p align="center">
  <i>A modern web application designed to connect trainers and users, enabling personalized workout plans, technique analysis, and progress tracking.</i>
  <br>
  <br>
  <a href="#about-the-project">About The Project</a> •
  <a href="#built-with">Built With</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#usage">Usage</a>
</p>

---

## About The Project

**Virtual Personal Trainer (VPT)** is a full-stack application that bridges the gap between fitness trainers and individuals seeking expert guidance. Trainers can upload instructional videos for various exercises, manage their clients, and create tailored workout routines. Users can browse a comprehensive library of exercises, view demonstrations, and will soon be able to upload their own videos for technique comparison and analysis.

This project aims to provide a seamless and interactive platform for remote personal training.

### Key Features:

* **Role-based access:** Separate dashboards and functionalities for Trainers and Users.
* **Exercise Management:** Trainers can create, update, and delete exercises, including instructional videos.
* **User Exercise Library:** Users can browse exercises filtered by body part.
* **Account Management:** Users can customize their profile, including changing their profile picture and password.
* **Secure Authentication:** JWT-based authentication to protect user data and routes.

---

## Built With

This project is built with a modern tech stack, containerized for easy setup and deployment.

<p align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React">
  <img src="https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS">
</p>

---

## Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

Make sure you have the following software installed:
* **Docker** and **Docker Compose**
* **Node.js** and **npm** (or yarn)

### Installation & Running the App

The backend and database are managed by Docker, while the frontend runs on a local development server.

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/your-username/Virtual-personal-trainer.git](https://github.com/your-username/Virtual-personal-trainer.git)
    cd Virtual-personal-trainer
    ```

2.  **Run the Backend and Database:**
    The first time you run the application, you need to build the Docker images.
    ```sh
    docker-compose up --build
    ```
    For all subsequent runs, you can start the containers without rebuilding:
    ```sh
    docker-compose up
    ```
    The backend API will be available at `http://localhost:8080`.

3.  **Run the Frontend:**
    Open a **new terminal window**, navigate to the `frontend` directory, install dependencies, and start the development server.
    ```sh
    cd frontend
    npm install
    npm run dev
    ```
    The frontend application will be available at `http://localhost:5173`.

---

## Usage

Once both the backend and frontend are running, you can open `http://localhost:5173` in your browser to use the application.

* **Register** a new account as either a "User" or a "Trainer".
* **Log in** to access your personalized dashboard.
* **Trainers** can add new exercises, upload videos, and manage their content.
* **Users** can browse exercises by body part and view instructional videos.

Enjoy your virtual training experience!
