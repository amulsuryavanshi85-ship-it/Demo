CREATE DATABASE flight_analytics;

USE flight_analytics;

CREATE TABLE airport (
    airport_id INT PRIMARY KEY AUTO_INCREMENT,
    icao_code VARCHAR(10) UNIQUE,
    iata_code VARCHAR(10) UNIQUE,
    name VARCHAR(150),
    city VARCHAR(100),
    country VARCHAR(100),
    continent VARCHAR(50),
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7),
    timezone VARCHAR(100)
);

CREATE TABLE aircraft (
    aircraft_id INT PRIMARY KEY AUTO_INCREMENT,
    registration VARCHAR(20) UNIQUE,
    model VARCHAR(100),
    manufacturer VARCHAR(100),
    icao_type_code VARCHAR(20),
    owner VARCHAR(150)
);

CREATE TABLE flights (
    flight_id VARCHAR(50) PRIMARY KEY,
    flight_number VARCHAR(20),
    aircraft_registration VARCHAR(20),
    origin_iata VARCHAR(10),
    destination_iata VARCHAR(10),
    scheduled_departure DATETIME,
    actual_departure DATETIME,
    scheduled_arrival DATETIME,
    actual_arrival DATETIME,
    status VARCHAR(30),
    airline_code VARCHAR(20)
);

CREATE TABLE airport_delays (
    delay_id INT PRIMARY KEY AUTO_INCREMENT,
    airport_iata VARCHAR(3),
    delay_date DATE,
    total_flights INT,
    delayed_flights INT,
    avg_delay_min INT,
    median_delay_min INT,
    canceled_flights INT
);
