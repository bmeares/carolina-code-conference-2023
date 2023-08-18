# Carolina Code Conference 2023

This [Meerschaum Compose](https://meerschaum.io/reference/compose/) project accompanies my talk [The Wonderful World of Incremental Time-Series ETL](https://blog.carolina.codes/p/meet-the-speakers-bennet-meares) and demonstrates practical syncing strategies I use daily.

## How Do I Use This?

To demonstrate secrets management, create a file `.env` and paste these variables:

```bash
export MRSM_SQL_ETL='{
  "flavor": "timescaledb",
  "username": "mrsm",
  "password": "mrsm",
  "database": "meerschaum",
  "port": 5432,
  "host": "localhost"
}'

export MRSM_MONGODB_LOCAL='{
  "uri": "mongodb://localhost:27017",
  "database": "etl"
}'
```

This defines two [connectors](https://meerschaum.io/reference/connectors/):

- `sql:etl`  
  These are the default credentials for `sql:main`, but to demonstrate, we've aliased it as `sql:etl`. To start this database, install `meerschaum` on your host machine and run
  ```bash
  mrsm stack up -d db
  ```

- `mongodb:local`  
  A service `mongodb` is added to this project's `docker-compose.yaml` to represent a heterogenous database fleet that you'll encounter in the wild.
  ```bash
  docker compose up -d mongodb
  ```


### Start the Container

Build your image, start the container, and exec into it.

```bash
docker compose build
docker compose up -d
docker compose exec mrsm-compose bash
```

### Example the Compose Project

Like `docker-compose.yaml`, the file `mrsm-compose.yaml` defines our project state.

Let's examine our project:

```bash
mrsm compose explain
```

This project contains five pipes:

1. `Pipe('plugin:noaa', 'weather', 'sc')`  
  Sync raw weather data from SC stations into PostgreSQL.
2. `Pipe('plugin:noaa', 'weather', 'nc')`  
  Sync raw weather data from NC stations into MongoDB.
3. `Pipe('plugin:clone', 'weather')`  
  Consolidate these parent pipes together into PostgreSQL.
4. `Pipe('sql:etl', 'weather', 'fahrenheit')`  
  Perform basic ETL on the combined weather data, converting temperature into Fahrenheit and only keeping desired columns.
5. `Pipe('sql:etl', 'weather', 'avg')`  
  Chain additional ETL onto the previous table, calculating the daily average temperature.

In addition to the connectors we defined in `.env`, some connectors are [plugins](https://meerschaum.io/reference/plugins/), namely the public plugins [`noaa`](https://github.com/bmeares/noaa) and [`clone`](https://github.com/bmeares/clone).

Run the intial syncs on these pipes, one-at-a-time, like so:

```bash
mrsm compose run
```

Now your tables should be built and ready to go! Next, let's set up automatic syncs so our tables will be updated as soon as new data are available:

```bash
mrsm compose up
```

Now the pipes are syncing in the background, sleeping every 30 seconds as set by `min_seconds`.

Like Docker Compose, stop the jobs like this (similarly, adding `-v` will also delete the pipes):

```bash
mrsm compose down
```

## Now Its's Your Turn

There's the beginning of another project in the file `carolina-compose.yaml`. It contains one pipe with the connector `plugin:fake`, which you can find in the `plugins/` directory (mounted as `/app/plugins`).

Examine `fake.py` and `example/example_connector.py`.

### Challenge

Can you write your own plugin and build your own pipes? See the [Writing Your Own Plugins guide](https://meerschaum.io/reference/plugins/writing-plugins/) for reference!