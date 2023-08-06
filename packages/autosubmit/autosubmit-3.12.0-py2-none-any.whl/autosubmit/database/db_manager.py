#!/usr/bin/env python

# Copyright 2015 Earth Sciences Department, BSC-CNS

# This file is part of Autosubmit.

# Autosubmit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Autosubmit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Autosubmit.  If not, see <http://www.gnu.org/licenses/>.

import sqlite3
import os


class DbManager(object):
    """
    Class to manage an SQLite database.
    """

    def __init__(self, root_path, db_name, db_version):
        self.root_path = root_path
        self.db_name = db_name
        self.db_version = db_version
        is_new = not os.path.exists(self._get_db_filepath())
        self.connection = sqlite3.connect(self._get_db_filepath())
        if is_new:
            self._initialize_database()

    def disconnect(self):
        """
        Closes the manager connection

        """
        self.connection.close()

    def create_table(self, table_name, fields):
        """
        Creates a new table with the given fields
        :param table_name: str
        :param fields: [str]

        """
        cursor = self.connection.cursor()
        create_command = self.generate_create_table_command(table_name, fields[:])
        cursor.execute(create_command)
        self.connection.commit()

    def drop_table(self, table_name):
        """
        Drops the given table
        :param table_name: str

        """
        cursor = self.connection.cursor()
        drop_command = self.generate_drop_table_command(table_name)
        cursor.execute(drop_command)
        self.connection.commit()

    def insert(self, table_name, columns, values):
        """
        Inserts a new row on the given table
        :param table_name: str
        :param columns: [str]
        :param values: [str]

        """
        cursor = self.connection.cursor()
        insert_command = self.generate_insert_command(table_name, columns[:], values[:])
        cursor.execute(insert_command)
        self.connection.commit()

    def insertMany(self, table_name, data):
        """
        Inserts multiple new rows on the given table
        :param table_name: str
        :param data: [()]

        """
        cursor = self.connection.cursor()
        insert_many_command = self.generate_insert_many_command(table_name, len(data[0]))
        cursor.executemany(insert_many_command, data)
        self.connection.commit()

    def select_first(self, table_name):
        """
        Returns the first row of the given table
        :param table_name: str
        :return row: []
        """
        cursor = self._select_with_all_fields(table_name)
        return cursor.fetchone()

    def select_first_where(self, table_name, where):
        """
        Returns the first row of the given table that matches the given where conditions
        :param table_name: str
        :param where: [str]
        :return row: []
        """
        cursor = self._select_with_all_fields(table_name, where)
        return cursor.fetchone()

    def select_all(self, table_name):
        """
        Returns all the rows of the given table
        :param table_name: str
        :return rows: [[]]
        """
        cursor = self._select_with_all_fields(table_name)
        return cursor.fetchall()

    def select_all_where(self, table_name, where):
        """
        Returns all the rows of the given table that matches the given where conditions
        :param table_name: str
        :param where: [str]
        :return rows: [[]]
        """
        cursor = self._select_with_all_fields(table_name, where)
        return cursor.fetchall()

    def count(self, table_name):
        """
        Returns the number of rows of the given table
        :param table_name: str
        :return int
        """
        cursor = self.connection.cursor()
        count_command = self.generate_count_command(table_name)
        cursor.execute(count_command)
        return cursor.fetchone()[0]

    def drop(self):
        """
        Drops the database (deletes the .db file)

        """
        self.connection.close()
        if os.path.exists(self._get_db_filepath()):
            os.remove(self._get_db_filepath())

    def _get_db_filepath(self):
        """
        Returns the path of the .db file
        :return path: int

        """
        return os.path.join(self.root_path, self.db_name) + '.db'

    def _initialize_database(self):
        """
        Initialize the database with an options table
        with the name and the version of the DB

        """
        options_table_name = 'db_options'
        columns = ['option_name', 'option_value']
        self.create_table(options_table_name, columns)
        self.insert(options_table_name, columns, ['name', self.db_name])
        self.insert(options_table_name, columns, ['version', self.db_version])

    def _select_with_all_fields(self, table_name, where=[]):
        """
        Returns the cursor of the select command with the given parameters
        :param table_name: str
        :param where: [str]
        :return cursor: Cursor
        """
        cursor = self.connection.cursor()
        count_command = self.generate_select_command(table_name, where[:])
        cursor.execute(count_command)
        return cursor

    """
    Static methods that generates the SQLite commands to make the queries
    """

    @staticmethod
    def generate_create_table_command(table_name, fields):
        create_command = 'CREATE TABLE IF NOT EXISTS ' + table_name + ' (' + fields.pop(0)
        for field in fields:
            create_command += (', ' + field)
        create_command += ')'
        return create_command

    @staticmethod
    def generate_drop_table_command(table_name):
        drop_command = 'DROP TABLE IF EXISTS ' + table_name
        return drop_command

    @staticmethod
    def generate_insert_command(table_name, columns, values):
        insert_command = 'INSERT INTO ' + table_name + '(' + columns.pop(0)
        for column in columns:
            insert_command += (', ' + column)
        insert_command += (') VALUES ("' + str(values.pop(0)) + '"')
        for value in values:
            insert_command += (', "' + str(value) + '"')
        insert_command += ')'
        return insert_command

    @staticmethod
    def generate_insert_many_command(table_name, num_of_values):
        insert_command = 'INSERT INTO ' + table_name + ' VALUES (?'
        num_of_values -= 1
        while num_of_values > 0:
            insert_command += ',?'
            num_of_values -= 1
        insert_command += ')'
        return insert_command

    @staticmethod
    def generate_count_command(table_name):
        count_command = 'SELECT count(*) FROM ' + table_name
        return count_command

    @staticmethod
    def generate_select_command(table_name, where=[]):
        basic_select = 'SELECT * FROM ' + table_name
        select_command = basic_select if len(where) == 0 else basic_select + ' WHERE ' + where.pop(0)
        for condition in where:
            select_command += ' AND ' + condition
        return select_command
