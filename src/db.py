"""A module containing a SQL database connection handler."""

import collections
import os.path
import sqlalchemy
import sqlalchemy.orm
import sqlparse
import model

_SQLITE_SQL_PATH = os.path.dirname(__file__) + '/../test/db/'
_SQLITE_SQL = [
    'meta.sql', 'topics.sql', 'data.sql', 'volttron_table_definitions.sql'
]

# An object containing database options.
DatabaseOptions = collections.namedtuple(
    'DatabaseOptions',
    ['db_type', 'user', 'password', 'host', 'database', 'pool_size'])


class Database(object):
  """A class for all SQL-based database connection handlers."""

  def __init__(self, opts):
    """Initializes the database handler."""
    if opts.db_type == 'sqlite':
      self.engine = sqlalchemy.create_engine('sqlite:///:memory:')
      self._initialize_sqlite()
    elif opts.db_type == 'mysql':
      self.engine = sqlalchemy.create_engine(
          'mysql+mysqlconnector://%s:%s@%s/%s' % (opts.user, opts.password,
                                                  opts.host, opts.database),
          pool_size=opts.pool_size)

  def _initialize_sqlite(self):
    """Creates tables and loads sample data."""
    # Create tables.
    model.BASE.metadata.create_all(self.engine)

    # Load test DB files and execute them.
    c = self.engine.connect()
    for sql in _SQLITE_SQL:
      f = open(_SQLITE_SQL_PATH + sql, 'r')
      statements = sqlparse.split(f.read())
      for statement in statements:
        c.execute(statement)
      f.close()
    c.close()

  def get_earliest_data_timestamp(self):
    """Gets the earliest timestamp from the data table.

    Returns:
      A datetime object for the earliest data entry.
    """
    s = sqlalchemy.orm.Session(self.engine)
    result = s.query(model.Datum).order_by(model.Datum.ts.asc())
    datum = result.first()
    s.close()
    return datum.ts

  def get_latest_data_timestamp(self):
    """Gets the latest timestamp from the data table.

    Returns:
      A datetime object for the earliest data entry.
    """
    s = sqlalchemy.orm.Session(self.engine)
    result = s.query(model.Datum).order_by(model.Datum.ts.desc())
    datum = result.first()
    s.close()
    return datum.ts

  def get_all_topics(self):
    """Gets a list of topic values.

    Returns:
      A list of Topic objects.
    """
    s = sqlalchemy.orm.Session(self.engine)
    result = s.query(model.Topic).all()
    s.close()
    return result
