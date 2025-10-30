CREATE DATABASE hospital_db;
USE hospital_db;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role ENUM('admin', 'doctor', 'receptionist') NOT NULL
);

CREATE TABLE patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    contact VARCHAR(20),
    diagnosis TEXT,
    anonymized_name VARCHAR(100),
    anonymized_contact VARCHAR(30),
    date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_modified_by INT,
    FOREIGN KEY (last_modified_by) REFERENCES users(user_id)
        ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    role VARCHAR(20),
    action VARCHAR(50),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    details TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE SET NULL ON UPDATE CASCADE
);

INSERT INTO users (username, password, role) VALUES
('admin', 'admin123', 'admin'),
('Dr. Bob', 'doc123', 'doctor'),
('Alice_recep', 'rec123', 'receptionist');

DELIMITER $$
CREATE TRIGGER trg_after_patient_insert
AFTER INSERT ON patients
FOR EACH ROW
BEGIN
    INSERT INTO logs (user_id, role, action, details)
    VALUES (
        NEW.last_modified_by,
        (SELECT role FROM users WHERE user_id = NEW.last_modified_by),
        'INSERT',
        CONCAT('Added patient: ', NEW.name)
    );
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER trg_after_patient_update
AFTER UPDATE ON patients
FOR EACH ROW
BEGIN
    INSERT INTO logs (user_id, role, action, details)
    VALUES (
        NEW.last_modified_by,
        (SELECT role FROM users WHERE user_id = NEW.last_modified_by),
        'UPDATE',
        CONCAT('Updated patient: ', NEW.name)
    );
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER trg_after_patient_delete
AFTER DELETE ON patients
FOR EACH ROW
BEGIN
    INSERT INTO logs (user_id, role, action, details)
    VALUES (
        OLD.last_modified_by,
        (SELECT role FROM users WHERE user_id = OLD.last_modified_by),
        'DELETE',
        CONCAT('Deleted patient: ', OLD.name)
    );
END$$
DELIMITER ;