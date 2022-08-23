# This file contains code that creates a database called workout_app.db upon running main.py if none exists.
# Defines functions that access the database to store profiles, sets, and exercise types.

import sqlite3
import os.path

# the base execution function.  if argument is provided, will treat command as a formatted string.  Returns None if
# fetchall and fetchone are both false

global database_name
database_filename = 'workout_app.db'

def executeSQL(command, *args, fetchall=False, fetchone=False):
    output = None
    conn = sqlite3.connect(f'{database_filename}')
    c = conn.cursor()

    c.execute(command.format(args))

    if fetchall:
        output = c.fetchall()
    if fetchone:
        output = c.fetchone()

    conn.commit()
    conn.close()
    return output


def create_profiles_table():
    executeSQL("""CREATE TABLE profiles (
        profile_name text
        )""")


def create_sets_table():
    executeSQL("""CREATE TABLE sets (
        profile_id integer,
        reps integer,
        exercise_id integer,
        weight integer,
        timestamp text
        )""")


def create_exercises_table():
    executeSQL("""CREATE TABLE exercises (
        exercise text
        )""")

# Creates a database in the current directory if none exists
def create_database():
    if not os.path.exists(f'{database_filename}'):
        create_profiles_table()
        create_sets_table()
        create_exercises_table()



#SQL commands that deal with profile data

def add_profile(profile_name):
    executeSQL("INSERT INTO profiles VALUES ('{}')".format(profile_name))


def del_profile(profile_name):
    executeSQL("DELETE FROM profiles WHERE profile_name='{}'".format(profile_name))


def get_profile_name(profile_id):
    profile_name = executeSQL("SELECT profile_name FROM profiles WHERE rowid = {}".format(profile_id), fetchone=True)[0]
    return profile_name


def list_all_profiles():
    profiles = executeSQL("SELECT rowid, * FROM profiles", fetchall=True)
    return profiles


#SQL commands that deal with set data

def add_set(profile_id, reps, exercise_id, weight, timestamp):
    executeSQL("INSERT INTO sets VALUES ({}, {}, {}, {}, '{}')".format(profile_id, reps, exercise_id, weight, timestamp))


def list_sets(profile_id, exercise_id=None):
    if exercise_id != None:
        sets = executeSQL("SELECT * FROM sets WHERE profile_id = {} AND exercise_id = {}".format(profile_id, exercise_id), fetchall=True)
    else:
        sets = executeSQL("SELECT * FROM sets WHERE profile_id = {}".format(profile_id), fetchall=True)
    return sets


#SQL commands that deal with exercise type data

def add_exercise_type(exercise_type):
    executeSQL("INSERT INTO exercises VALUES ('{}')".format(exercise_type))


def list_exercise_types():
    exercises = executeSQL("SELECT rowid, * FROM exercises", fetchall=True)
    return exercises

def get_exercise_type(id):
    exercise = executeSQL("SELECT * FROM exercises WHERE rowid = {}".format(id), fetchone=True)
    return exercise