use flight_analytics;
use table aircraft;

SELECT * FROM aircraft;



SELECT 
    a.model,
    COUNT(f.flight_id) AS total_flights
FROM aircraft a
JOIN flights f
    ON a.registration = f.aircraft_registration
GROUP BY a.model;



SELECT 
    a.registration,
    a.model,
    COUNT(f.flight_id) AS total_flights
FROM aircraft a
JOIN flights f
    ON a.registration = f.aircraft_registration
GROUP BY a.registration, a.model
HAVING COUNT(f.flight_id) > 5;



SELECT 
    ap.name,
    COUNT(f.flight_id) AS outbound_flights
FROM airport ap
JOIN flights f
    ON ap.iata_code = f.origin_iata
GROUP BY ap.iata_code, ap.name
HAVING COUNT(f.flight_id) > 5;



SELECT 
    ap.name,
    ap.city,
    COUNT(f.flight_id) AS arriving_flights
FROM airport ap
JOIN flights f
    ON ap.iata_code = f.destination_iata
GROUP BY ap.iata_code, ap.name, ap.city
ORDER BY arriving_flights DESC
LIMIT 3;


SELECT 
    f.flight_number,
    a.registration AS aircraft,
    origin.name AS departure_airport,
    f.actual_arrival AS arrival_time
FROM flights f
JOIN aircraft a
    ON f.aircraft_registration = a.registration
JOIN airport origin
    ON f.origin_iata = origin.iata_code
WHERE f.destination_iata = 'DEL'
ORDER BY f.actual_arrival DESC
LIMIT 5;



SELECT 
    f.flight_number,
    a.registration AS aircraft,
    origin.name AS departure_airport,
    f.actual_arrival AS arrival_time
FROM flights f
JOIN aircraft a
    ON f.aircraft_registration = a.registration
JOIN airport origin
    ON f.origin_iata = origin.iata_code
WHERE f.destination_iata = 'DEL'
ORDER BY f.actual_arrival DESC
LIMIT 5;


SELECT 
    ap.iata_code,
    ap.name,
    ap.city
FROM airport ap
LEFT JOIN flights f
    ON ap.iata_code = f.destination_iata
WHERE f.flight_id IS NULL;



SELECT 
    f.airline_code,

    SUM(CASE 
        WHEN f.status = 'On Time' THEN 1 
        ELSE 0 
    END) AS on_time_flights,

    SUM(CASE 
        WHEN f.status = 'Delayed' THEN 1 
        ELSE 0 
    END) AS delayed_flights,

    SUM(CASE 
        WHEN f.status = 'Cancelled' THEN 1 
        ELSE 0 
    END) AS cancelled_flights

FROM flights f
GROUP BY f.airline_code;




SELECT 
    f.flight_number,
    a.registration AS aircraft,
    origin.name AS departure_airport,
    destination.name AS arrival_airport,
    f.scheduled_departure
FROM flights f
JOIN aircraft a
    ON f.aircraft_registration = a.registration
JOIN airport origin
    ON f.origin_iata = origin.iata_code
JOIN airport destination
    ON f.destination_iata = destination.iata_code
WHERE f.status = 'Cancelled'
ORDER BY f.scheduled_departure DESC;



SELECT 
    origin.city AS origin_city,
    destination.city AS destination_city,
    COUNT(DISTINCT a.model) AS different_aircraft_models
FROM flights f
JOIN airport origin
    ON f.origin_iata = origin.iata_code
JOIN airport destination
    ON f.destination_iata = destination.iata_code
JOIN aircraft a
    ON f.aircraft_registration = a.registration
GROUP BY origin.city, destination.city
HAVING COUNT(DISTINCT a.model) > 2;


SELECT 
    ap.name,
    ap.city,
    COUNT(f.flight_id) AS total_arrivals,

    SUM(CASE 
        WHEN f.status = 'Delayed' THEN 1 
        ELSE 0 
    END) AS delayed_flights,

    ROUND(
        100.0 * SUM(CASE 
            WHEN f.status = 'Delayed' THEN 1 
            ELSE 0 
        END) / COUNT(f.flight_id),
        2
    ) AS delayed_percentage

FROM airport ap
JOIN flights f
    ON ap.iata_code = f.destination_iata
GROUP BY ap.iata_code, ap.name, ap.city
ORDER BY delayed_percentage DESC;
    
    