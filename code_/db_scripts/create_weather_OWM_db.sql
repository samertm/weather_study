-- *****************
-- 20140421
-- 
-- Script to populate Weather Study project database.
--
-- Run as
--     sqlite3 weather_data_OWM.db < 
--                       CODE/DB_SCRIPTS/create_weather_OWM_db.sql
--
-- *****************

DROP TABLE IF EXISTS locations;
CREATE TABLE locations (
    id TEXT PRIMARY KEY UNIQUE,
    name TEXT,
    lat NUMBER,
    lon NUMBER,
    country TEXT
);

DROP TABLE IF EXISTS downloads_inserted;
-- Maintain records about which download-directories have been used to populate 
--     table "owm_values".
CREATE TABLE downloads_inserted (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    directory_name TEXT UNIQUE
);

DROP TABLE IF EXISTS owm_values;
-- Forecast and observed-data values from the Open Weather Map project.
CREATE TABLE owm_values (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id TEXT,
    -- We make target_date an integer so that calculations can be done with it.
    target_date INTEGER,
    -- Numerical value fields follow this format:
    --     <type>_<displacement>
    --   where "type" is maxt (temperature), mint (temperature), or rain;
    --   and where "displacement" is the number of days away from target_date.
    -- When displacement = 0, the value is actual observed data; in other
    --   cases, the value is forecast data.
    -- We expect 
    --     `maxt` and `mint` to be supplied in degrees Celsius and 
    --     `rain` and `snow` to be supplied in cm.
    maxt_0 NUMBER,
    mint_0 NUMBER,
    rain_0 NUMBER,
    snow_0 NUMBER,
    maxt_1 NUMBER,
    mint_1 NUMBER,
    rain_1 NUMBER,
    snow_1 NUMBER,
    maxt_2 NUMBER,
    mint_2 NUMBER,
    rain_2 NUMBER,
    snow_2 NUMBER,
    maxt_3 NUMBER,
    mint_3 NUMBER,
    rain_3 NUMBER,
    snow_3 NUMBER,
    maxt_4 NUMBER,
    mint_4 NUMBER,
    rain_4 NUMBER,
    snow_4 NUMBER,
    maxt_5 NUMBER,
    mint_5 NUMBER,
    rain_5 NUMBER,
    snow_5 NUMBER,
    maxt_6 NUMBER,
    mint_6 NUMBER,
    rain_6 NUMBER,
    snow_6 NUMBER,
    maxt_7 NUMBER,
    mint_7 NUMBER,
    rain_7 NUMBER,
    snow_7 NUMBER,
    maxt_8 NUMBER,
    mint_8 NUMBER,
    rain_8 NUMBER,
    snow_8 NUMBER,
    maxt_9 NUMBER,
    mint_9 NUMBER,
    rain_9 NUMBER,
    snow_9 NUMBER,
    maxt_10 NUMBER,
    mint_10 NUMBER,
    rain_10 NUMBER,
    snow_10 NUMBER,
    maxt_11 NUMBER,
    mint_11 NUMBER,
    rain_11 NUMBER,
    snow_11 NUMBER,
    maxt_12 NUMBER,
    mint_12 NUMBER,
    rain_12 NUMBER,
    snow_12 NUMBER,
    maxt_13 NUMBER,
    mint_13 NUMBER,
    rain_13 NUMBER,
    snow_13 NUMBER,
    maxt_14 NUMBER,
    mint_14 NUMBER,
    rain_14 NUMBER,
    snow_14 NUMBER,
    UNIQUE (location_id, target_date),
    FOREIGN KEY (location_id) REFERENCES locations(id)
);

SELECT * FROM sqlite_master WHERE type='table';
