import json
import os
import time

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from sqlalchemy import desc
import utils.config
from model import *

__author__ = 'guoguangchuan'

db_host = utils.config.get("preseller_db", "host")
db_port = utils.config.get("preseller_db", "port")
db_user = utils.config.get("preseller_db", "user")
db_pssswd = utils.config.get("preseller_db", "passwd")
db_database = utils.config.get("preseller_db", "database")

engine = create_engine(
    'mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8' % (db_user, db_pssswd, db_host, db_port, db_database))
db_session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))

Base.query = db_session.query_property()
Base.metadata.create_all(engine, checkfirst=True)

BUSY_TIME_OUT = 60 * 1000


@event.listens_for(engine, 'connect')
def set_busy_timeout(dbapi_connection, connection_record):
    """
        Set sqlite busy timeout for lock problem.
        See Also: http://jira.haizhi.com/browse/BDP-11760
    Args:
        dbapi_connection(Connection):
        connection_record:
    """
    cursor = dbapi_connection.cursor()  # type: Cursor
    try:
        cursor.execute('PRAGMA busy_timeout={timeout}'.format(timeout=BUSY_TIME_OUT))
    finally:
        cursor.close()


class Configure(object):
    DEBUG = False

    def __init__(self):
        self.session = db_session()  # type: Session

    def add(self, instance):
        try:
            self.session.add(instance)
            self.session.flush()
            self.session.commit()
        except Exception, e:
            self.session.rollback()
            raise e

    def delete(self, instance):
        try:
            self.session.delete(instance)
            self.session.flush()
            self.session.commit()
        except Exception, e:
            self.session.rollback()
            raise e

    def first(self, model, is_del=0, **kwargs):
        """

        Args:
            model:
            **kwargs:

        Returns:
        """
        kwargs['is_del'] = is_del
        result = self.session.query(model).filter_by(**kwargs).first()
        return result

    def filter_all(self, model, filters, is_del=0, **kwargs):
        """

        Args:
            model:
            **kwargs:

        Returns:
        """
        kwargs['is_del'] = is_del
        result = self.session.query(model).filter(filters).filter_by(**kwargs).all()
        return result

    def all(self, model, filters=None, page=None, order_by=None, filter_by=None, is_del=0, **kwargs):
        query = self.session.query(model)

        if order_by:
            query = query.order_by(desc(order_by))

        if filter_by:
            kwargs.update(filter_by)
        if filters:
            query = query.filter(filters)
        kwargs['is_del'] = is_del
        query = query.filter_by(**kwargs)

        if page:
            query = query.limit(10).offset(10 * int(page) - 10)

        result = query.all()
        return result

    def count(self, model, is_del=0, **kwargs):
        kwargs['is_del'] = is_del
        return self.session.query(model).filter_by(**kwargs).count()

    def tick(self, instance):
        self.reload(instance)
        instance.tick()

    def commit(self):
        self.session.flush()
        self.session.commit()

    def expire(self, instance):
        self.session.expire(instance)

    def refresh(self, instance):
        self.session.refresh(instance)

    def reload(self, instance):
        self.expire(instance)
        self.refresh(instance)

    def flush(self):
        self.session.flush()

    def close(self):
        self.session.close()
        self.session.remove()
