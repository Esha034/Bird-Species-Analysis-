CREATE TABLE bird_data (
    admin_unit_code TEXT,
    sub_unit_code TEXT,
    site_name TEXT,
    plot_name TEXT,
    location_type TEXT,
    year INT,
    date DATE,
    observer TEXT,
    visit INT,
    interval_length TEXT,
    id_method TEXT,
    distance TEXT,
    flyover_observed BOOLEAN,
    sex TEXT,
    common_name TEXT,
    scientific_name TEXT,
    acceptedtsn FLOAT,
    npstaxoncode FLOAT,
    aou_code TEXT,
    pif_watchlist_status BOOLEAN,
    regional_stewardship_status BOOLEAN,
    temperature FLOAT,
    humidity FLOAT,
    sky TEXT,
    wind TEXT,
    disturbance TEXT,
    initial_three_min_cnt BOOLEAN,
    month INT,
    season TEXT,
    habitat TEXT
);

SELECT *
FROM bird_data
LIMIT 10;

SELECT habitat, COUNT(*) 
FROM bird_data 
GROUP BY habitat;

SELECT habitat, COUNT(DISTINCT scientific_name)
FROM bird_data
GROUP BY habitat;

SELECT common_name, COUNT(*) 
FROM bird_data
GROUP BY common_name
ORDER BY COUNT(*) DESC
LIMIT 10;

SELECT year, COUNT(*) 
FROM bird_data
GROUP BY year
ORDER BY year;

SELECT month, COUNT(*) 
FROM bird_data
GROUP BY month
ORDER BY month;

SELECT season, COUNT(*) 
FROM bird_data
GROUP BY season;

SELECT id_method, COUNT(*) 
FROM bird_data
GROUP BY id_method;

SELECT distance, COUNT(*) 
FROM bird_data
GROUP BY distance;

SELECT flyover_observed, COUNT(*) 
FROM bird_data
GROUP BY flyover_observed;

SELECT temperature, humidity 
FROM bird_data;

SELECT plot_name, COUNT(DISTINCT scientific_name)
FROM bird_data
GROUP BY plot_name
ORDER BY COUNT DESC
LIMIT 10;

SELECT pif_watchlist_status, COUNT(*)
FROM bird_data
GROUP BY pif_watchlist_status;

SELECT regional_stewardship_status, COUNT(*)
FROM bird_data
GROUP BY regional_stewardship_status;

SELECT observer, COUNT(*)
FROM bird_data
GROUP BY observer
ORDER BY COUNT DESC
LIMIT 10;

SELECT sex, COUNT(*)
FROM bird_data
GROUP BY sex;