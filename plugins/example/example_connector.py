#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Define `fetch()` for `example:{label}`.

You may instantiate this connector with `mrsm.get_connector()`, e.g.:

    >>> import meerschaum as mrsm
    >>> conn = mrsm.get_connector('example', 'foo', username='foo', password='bar')

If `MRSM_EXAMPLE_SECRET` is defined:
    >>> conn = mrsm.get_connector('example', 'secret')
"""

from datetime import datetime
import meerschaum as mrsm
from meerschaum.connectors import make_connector, Connector
from meerschaum.utils.typing import Optional, Any, List, Dict

@make_connector
class ExampleConnector(Connector):

    REQUIRED_ATTRIBUTES = ['username', 'password']

    def fetch(
            self,
            pipe: mrsm.Pipe,
            begin: Optional[datetime] = None,
            end: Optional[datetime] = None,
            **kwargs: Any
        ) -> List[Dict[str, Any]]:
        """
        This connector method `fetch()` behaves the same as the plugin-level,
        but now we have access to `self` where we may store secrets.

        Like before, we may return any of the following:
        - Pandas DataFrame
        - List of dictionaries
        - Dictionary of lists
        - Generator of the above (yield chunks)
        """
        docs = []

        ### The required connector attributes are stored in `self.__dict__`.
        creds = {
            'username': self.username,
            'password': self.password,
        }

        return docs
