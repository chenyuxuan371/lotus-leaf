"""The UW Solar API server."""

import json
import bottle
import model
import server

class ApiServer(server.BaseServer):
  """The UW Solar API server."""

  def __init__(self, db):
    """Initializes routes and WSGI application.

    Args:
      db: A database accessor.
    """
    super().__init__([
        server.Route('GET', '/ping', ApiServer.ping),
        server.Route('GET', '/data/timestamp/earliest',
                     self.get_earliest_data_timestamp),
        server.Route('GET', '/data/timestamp/latest',
                     self.get_latest_data_timestamp),
        server.Route('GET', '/topics', self.get_all_topics)
    ])

    self._db = db

  @staticmethod
  def ping():
    """Returns a ping response.

    For now, this method always returns success as long as the web server was
    successfully initialized. In the future, this may be extended to perform
    more extensive health checks, such as to ensure that dependent services are
    available (e.g. the database).
    """
    pass

  def get_all_topics(self):
    """Returns a list of topic values.

    Returns:
      A JSON-encoded list of topic values.
    """
    bottle.response.content_type = 'application/json'
    return json.dumps(self._db.get_all_topics(), cls=model.TopicEncoder)

  def get_earliest_data_timestamp(self):
    """Returns the earliest timestamp for which there is solar panel activity.

    Returns:
      A JSON-encoded ISO8601 timestamp.
    """
    bottle.response.content_type = 'application/json'
    result = self._db.get_earliest_data_timestamp()
    if not result:
      return ''

    return json.dumps(result.isoformat())

  def get_latest_data_timestamp(self):
    """Returns the latest timestamp for which there is solar panel activity.

    Returns:
      A JSON-encoded ISO8601 timestamp.
    """
    bottle.response.content_type = 'application/json'
    result = self._db.get_latest_data_timestamp()
    if not result:
      return ''

    return json.dumps(result.isoformat())
