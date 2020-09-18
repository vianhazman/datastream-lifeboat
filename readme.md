## Lifeboat
Backfill service for datastream

## Scheduling
Job is scheduled with ofelia (open source container scheduler).
To change scheduler settings, open `docker-compose.yml`

## Backfilling Job
This service will do backfilling with replay strategy. We manually
parse Postgres input into Avro-equivalent payload. The job configuration
is in `configs/<jobname>.yml`

Job requires custom logic to parse Postgres result set into Avro payload.
The payload may be loaded from `transformation` package.

## Running Job 

There are two modes in running backfilling jobs with lifeboat.
- Daily Mode: For scheduled job, searches missing ID sequence from InfluxDB and querying it up in Postgres
``` 
python app.py --job_name scele --mode daily --start_time "now()" --end_time 1d  
```

- Manual Mode: For special backfilling purpose, directly query to Postgres with provided time range
```
 python app.py --job_name scele --mode manual --start_time "2020-08-01" --end_time "2020-08-02"
```