-- *****************
-- 20140414
-- 
-- Script to populate Weather Study project database.
--
-- Run as
--     sqlite3 weather_data_OWM.db < 
--                       POPULATE_DB/DB_SCRIPTS/create_weather_OWM_db.sql
--
-- *****************

DROP TABLE IF EXISTS locations;
CREATE TABLE locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    lat NUMBER,
    lon NUMBER,
    country TEXT
);

DROP TABLE IF EXISTS owm_values;
-- Forecast and observed-data values from the Open Weather Map project.
CREATE TABLE owm_values (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER,
    target_date INTEGER,
    -- Numerical value fields follow this format:
    --     <type>_<displacement>
    --   where "type" is maxt (temperature), mint (temperature), or rain;
    --   and where "displacement" is the number of days away from target_date.
    -- When displacement = 0, the value is actual observed data; in other
    --   cases, the value is forecast data.
    -- We expect 
    --     `maxt` and `mint` to be supplied in degrees Celsius and 
    --     `rain` to be supplied in cm.
    maxt_0 NUMBER,
    mint_0 NUMBER,
    rain_0 NUMBER,
    maxt_1 NUMBER,
    mint_1 NUMBER,
    rain_1 NUMBER,
    maxt_2 NUMBER,
    mint_2 NUMBER,
    rain_2 NUMBER,
    maxt_3 NUMBER,
    mint_3 NUMBER,
    rain_3 NUMBER,
    maxt_4 NUMBER,
    mint_4 NUMBER,
    rain_4 NUMBER,
    maxt_5 NUMBER,
    mint_5 NUMBER,
    rain_5 NUMBER,
    maxt_6 NUMBER,
    mint_6 NUMBER,
    rain_6 NUMBER,
    maxt_7 NUMBER,
    mint_7 NUMBER,
    rain_7 NUMBER,
    maxt_8 NUMBER,
    mint_8 NUMBER,
    rain_8 NUMBER,
    maxt_9 NUMBER,
    mint_9 NUMBER,
    rain_9 NUMBER,
    maxt_10 NUMBER,
    mint_10 NUMBER,
    rain_10 NUMBER,
    maxt_11 NUMBER,
    mint_11 NUMBER,
    rain_11 NUMBER,
    maxt_12 NUMBER,
    mint_12 NUMBER,
    rain_12 NUMBER,
    maxt_13 NUMBER,
    mint_13 NUMBER,
    rain_13 NUMBER,
    maxt_14 NUMBER,
    mint_14 NUMBER,
    rain_14 NUMBER,
    maxt_15 NUMBER,
    mint_15 NUMBER,
    rain_15 NUMBER,
    maxt_16 NUMBER,
    mint_16 NUMBER,
    rain_16 NUMBER,
    FOREIGN KEY (location_id) REFERENCES locations(id)
);

SELECT * FROM sqlite_master WHERE type='table';