# Meerschaum Compose Project Template

This template is for quickly building Dockerized [Meerschaum Compose](https://meerschaum.io/reference/compose/) projects. For a more detailed example, refer to the [Tech Slam 'N Eggs example repository](https://github.com/bmeares/techslamneggs).

> Docker is not required but `docker/Dockerfile` is provided for convenience.

### Plugins

Meerschaum's [plugin system](https://meerschaum.io/reference/plugins/) allows you to do the following:
- **Quickly ingest data**  
  [`fetch()`](https://meerschaum.io/reference/plugins/writing-plugins/#the-fetch-function) or [`sync()`](https://meerschaum.io/reference/plugins/writing-plugins/#the-sync-function)
- **Add custom connectors**  
  [`@make_connector`](https://meerschaum.io/reference/connectors/#-environment-connectors)
- **Define custom actions**  
  [`@make_action`](https://meerschaum.io/reference/plugins/writing-plugins/#the-make_action-decorator)
- **Add command-line arguments**  
  [`add_plugin_argument()`](https://meerschaum.io/reference/plugins/writing-plugins/#custom-command-line-options)
- **Extend the web API**  
  [`@api_plugin`](https://meerschaum.io/reference/plugins/writing-plugins/#the-api_plugin-decorator)

Consult the [plugins documentation](https://meerschaum.io/reference/plugins/writing-plugins/) for how to write your own plugins. The plugin `example` has been added as reference for `plugin:example` and `example:{label}`.

## Getting Started

Build and start the container:

```bash
docker compose up --build -d
```

Jump into a shell:

```bash
docker compose exec -it mrsm-compose bash
```

Once inside the container, you may now make changes and begin your development process. Here are some useful commands to get started:

```bash
mrsm compose explain
```

This will parse your compose file and print your current environment and state of the pipes.

```bash
mrsm compose run
```

The default command in `docker/bootstrap.sh` is `mrsm compose run` because it does the following:
- Register and update the parameters for your pipes.
- Sync them one-by-one.

Flags you pass to `compose run` are passed to `sync pipes`, including custom arguments added via [`add_plugin_argument()`](https://meerschaum.io/reference/plugins/writing-plugins/#custom-command-line-options).

Other useful `compose` commands:

- `compose down -v`  
  Stop any running jobs and delete the pipes (`-v` or `--drop`).
- `compose up --dry`  
  Register or update the pipes' registrations (`--dry` prevents syncing from happening).
- `compose ps`  
  Print the currently running jobs (started by `compose up`).

All other commands are executed within the context of the isolated environment (with the flag `--tags` appended as well). You may manage your pipes as usual with any regular `mrsm` commands.

## `fetch()` vs `sync()`

In most cases, a simple `fetch()` function is all that's needed to get the job done. `fetch()` returns data or a generator of chunks to be passed into `Pipe.sync()`:

```python
import meerschaum as mrsm
from meerschaum.utils.typing import List, Dict, Any

def fetch(
        pipe: mrsm.Pipe,
        **kwargs: Any
    ) -> List[Dict[str, Any]]:
    """
    Return any of the following:

    - Pandas DataFrame
    - List of dictionaries
    - Dictionary of lists
    - A generator of the following (yield chunks)
    """
    return [
        {
            'datetime': '2023-01-01',
            'id': 1,
            'value': 100.0,
        },
        {
            'datetime': '2023-01-01',
            'id': 2,
            'value': 200.0,
        },
    ]
```

For more fine-grained control, `sync()` expects a `SuccessTuple` (`bool` and `str`). `sync()` overrides `fetch()`, so you may use `fetch()` within `sync()`. Consider this example which resyncs days with different rowcounts:

```python
from datetime import datetime, timedelta
import meerschaum as mrsm
from meerschaum.utils.typing import Any, SuccessTuple
from meerschaum.utils.misc import round_time

required = ['python-dateutil']

def sync(
        pipe: mrsm.Pipe,
        begin: Optional[datetime] = None,
        end: Optional[datetime] = None,
        **kwargs: Any
    ) -> SuccessTuple:
    """
    Custom syncing strategy: resync days with different rowcounts.
    """
    from dateutil.rrule import rrule, DAILY

    begin = begin or datetime(2023, 1, 1)
    end = end or datetime(2024, 1, 1)

    days_synced = 0
    for day in rrule(freq=DAILY, dtstart=begin, until=end):
        chunk_begin = day
        chunk_end = day + timedelta(days=1)

        pipe_rowcount = pipe.get_rowcount(begin=chunk_begin, end=chunk_end)
        remote_rowcount = get_remote_rowcount(pipe, begin=chunk_begin, end=chunk_end)
        
        if pipe_rowcount == remote_rowcount:
            continue

        docs = fetch(pipe, begin, end)
        chunk_success, chunk_msg = pipe.sync(docs, **kwargs)
        if not chunk_success:
            return chunk_success, f"Failed to sync {day}:\n" + chunk_msg

        days_synced += 1
    
    return True, f"Successfully synced {days_synced} days."


def get_remote_rowcount(
        pipe: mrsm.Pipe,
        begin: datetime,
        end: datetime,
    ) -> int:
    ...


def fetch(
        pipe: mrsm.Pipe,
        begin: datetime,
        end: datetime,
    ) -> List[Dict[str, Any]]:
    ...
```

## Publishing Your Plugins

If you choose to publish your plugins to the public repository, make an account at https://api.mrsm.io and run `register plugin`, e.g. (assuming `my-awesome-plugin.py` exists):

```bash
mrsm compose login api:mrsm
mrsm compose register plugin my-awesome-plugin
```

You can view your published plugin at https://api.mrsm.io/dash/plugins.

You may also publish your plugins to your private repository with `--repository` or `-r`:

```bash
### Define api:private through the wizard.
### On your repository's host, start the repository with `mrsm start api`.
mrsm compose bootstrap connector
mrsm compose register plugin my-awesome-plugin -r api:private
```

To remove the plugin from the repository, run `mrsm delete plugin`:

```bash
mrsm compose delete plugin my-awesome-plugin
```