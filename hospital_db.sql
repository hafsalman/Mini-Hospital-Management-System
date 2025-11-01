CREATE DATABASE IF NOT EXISTS hospital_db;
USE hospital_db;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,  -- bcrypt hash stored here
    role ENUM('admin', 'doctor', 'receptionist') NOT NULL
);

CREATE TABLE patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    contact VARCHAR(20),
    diagnosis VARCHAR(255),
    anonymized_name VARCHAR(100),
    anonymized_contact VARCHAR(20),
    date_added DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    role VARCHAR(20),
    action VARCHAR(50),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    details VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

INSERT INTO users (username, password, role) VALUES
('admin', 'admin123', 'admin'),
('dr_bob', 'doc123', 'doctor'),
('alice_r', 'rec123', 'receptionist');

SELECT * FROM users;
SELECT * FROM patients;
SELECT * FROM logs;