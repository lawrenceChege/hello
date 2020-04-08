"""
    This module holds the database schema used in migrations
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import current_app

class DbModel():
    """
        Conncets methods to connect and perfom instructions to the database
    """

    def __init__(self):
        self.db_url = 'postgres://ggxwssliwpgezi:8980f616c4c97f77cd050bef11868bb9781354dcef3bb7fd391dfcb40a6662b8@ec2-184-72-236-57.compute-1.amazonaws.com:5432/d6guqhcrbardo1'

        try:
            self.conn = psycopg2.connect(self.db_url)
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
        except (Exception, psycopg2.OperationalError) as err:
            print (err)
            print('oops! Could not connect using Url\n')
            

    def init_db(self, app):
        try:
            url ='postgres://ggxwssliwpgezi:8980f616c4c97f77cd050bef11868bb9781354dcef3bb7fd391dfcb40a6662b8@ec2-184-72-236-57.compute-1.amazonaws.com:5432/d6guqhcrbardo1'
            self.conn = psycopg2.connect(url)
            print('connected to db using url...\n')
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
        except (Exception, psycopg2.OperationalError) as err:
            print (err)
            print('oops! Could not connect using Url\n')

    def drop_tables(self, table):
        """ drop existing tables """
        try:
            self.cur.execute("DROP TABLE IF EXISTS" + ' '+ table)
            self.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print (error)
            print('could not drop tables\n')

    def commit(self):
        """
        commit changes to the db
        """
        self.conn.commit()

    def close(self):
        """
            close the cursor and the connection
        """
        self.cur.close()
        self.conn.close()

    def findOne(self):
        """ return one item from query"""
        return self.cur.fetchone()

    def findAll(self):
        """ return all items from query"""
        return self.cur.fetchall()