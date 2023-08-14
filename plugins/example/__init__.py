#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Demonstrate `plugin:example` and `example:{label}`.
"""

### List dependencies here, e.g. 'pandas>=1.3.5'.
### You may also create `requirements.txt`.
required = []


####################
# example:{label}) #
####################

from meerschaum.connectors import make_connector
from .example_connector import ExampleConnector


### If you don't want to bother with a custom connector,
### you can define `fetch()` (or `sync()`) at the module-level
### and use the connector `plugin:example`.

##################
# plugin:example #
##################

from datetime import datetime
import meerschaum as mrsm
from meerschaum.utils.typing import SuccessTuple, List, Dict, Any, Optional

def fetch(
        pipe: mrsm.Pipe,
        begin: Optional[datetime] = None,
        end: Optional[datetime] = None,
        **kwargs: Any
    ) -> List[Dict[str, Any]]:
    """
    Return a list of dictionaries.
    May also return a Pandas DataFrame, list of dictionaries, or generator (yield chunks).
    """
    docs = []

    return docs
