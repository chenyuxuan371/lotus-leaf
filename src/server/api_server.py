"""The UW Solar API server."""

import json
import dateutil.parser
import bottle
import codec
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
        server.Route('GET', '/data', self.get_data),
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
    return json.dumps(self._db.get_all_topics(), cls=codec.TopicEncoder)

  def get_data(self):
    """Returns time-series data for a set of topics.

    This method expects the query string to contain the following parameters:

      * topic_ids: A comma-separated list of topic IDs to query.
      * start_date_time: The start of the date range being queried.
      * end_date_time: The end of the date range being queried.
      * sample_rate: The sample rate, between 0 and 1 (inclusive).

    Returns:
      A JSON-encoded list of topic data.
    """
    params = bottle.request.params.decode()  # pylint: disable=no-member

    # Validate topic ID.
    try:
      topic_ids = [int(i) for i in params.get('topic_ids').split(',')]
    except (AttributeError, TypeError, ValueError):
      raise bottle.HTTPError(400, 'A valid topic ID is required.')

    # Validate start and end times.
    try:
      start_dt = dateutil.parser.parse(params.get('start_date_time'))
      end_dt = dateutil.parser.parse(params.get('end_date_time'))
    except (TypeError, ValueError):
      raise bottle.HTTPError(400, 'Valid start and end times are required.')

    # Validate sample rate.
    try:
      sample_rate = float(params.get('sample_rate'))
      if sample_rate < 0 or sample_rate > 1:
        raise bottle.HTTPError(400, 'A valid sample rate is required.')
    except (TypeError, ValueError):
      raise bottle.HTTPError(400, 'A valid sample rate is required.')

    # Query database.
    bottle.response.content_type = 'application/json'
    result = self._db.get_data(topic_ids, start_dt, end_dt, sample_rate)

    return json.dumps(result, cls=codec.DatumEncoder)

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
