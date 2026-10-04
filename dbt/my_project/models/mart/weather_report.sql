-- vue horaire detaillee pour le dashboard Superset
select
    city,
    temperature,
    weather_description,
    wind_speed,
    feelslike,
    humidity,
    pressure,
    weather_time_local,
    inserted_at_local
from {{ ref('stg_weather_data') }}
