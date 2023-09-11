import json
from datetime import datetime
from log import Log

db_log = Log('database', ['tipo', 'status'])


class MicroDB:
  _db_dir = './'
  _db_name = ''
  _data = {}

  def __init__(self, db_name: str, db_dir='./') -> None:
    """
        Initializes a MicroDB instance.
        :param db_name: the name of the database.
        :param db_dir: the directory where the database file will be stored. Default is './databases/'.
        """
    self._db_name = db_name
    self._db_dir = db_dir
    try:
      self.load()
    except:
      self.save()

    db_log.logger(['startup', 'passed'])

  def save(self):
    """
        Saves the database to a JSON file.
        """
    try:
      with open(self._db_dir + self._db_name + '.json', "w") as f:
        f.write(json.dumps(dict(self._data)))
        db_log.logger(['save', 'sucess'])
      self.load()
    except Exception as e:
      db_log.logger(['save', 'failed'])
      raise Exception('write', e)

  def load(self):
    """
        Loads the database from a JSON file.
        """
    try:
      with open(self._db_dir + self._db_name + '.json', "r") as f:
        self._data = json.loads(f.read())
        db_log.logger(['load', 'sucess'])

    except Exception as e:
      db_log.logger(['load', 'failed'])
      raise Exception('read', e)

  def get(self, key: str):
    """
        Retrieves a value from the database.
        :param key: the key of the value to retrieve.
        :return: the value associated with the given key.
        """
    self.load()
    db_log.logger(['get', 'passed'])
    return self._data.get(key)

  def set(self, key: str, value):
    """
        Sets a value in the database.
        :param key: the key of the value to set.
        :param value: the value to set.
        """
    self._data[key] = value
    self.save()
    db_log.logger(['set', 'passed'])

  def rem(self, key: str):
    """
        Removes a value from the database.
        :param key: the key of the value to remove.
        """
    self._data.pop(key)
    self.save()
    db_log.logger(['remove', 'passed'])

  def get_all(self):
    self.load()
    db_log.logger(['get_all', 'passed'])
    return self._data
