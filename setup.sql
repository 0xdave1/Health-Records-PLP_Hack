CREATE DATABASE school_health;

USE school_health;

CREATE TABLE schools (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255)
);

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    age INT,
    class_name VARCHAR(50)
);

CREATE TABLE health_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    health_issue VARCHAR(255),
    date DATE
);
