import json
import urllib.parse
import base64
import requests
import mysql.connector
import os
import time


def get_mysql_config():
    return {
        'user': get_environment_variable('mysql_user'),
        'password': get_environment_variable('mysql_pwd'),
        'host': get_environment_variable('mysql_host'),
        'database': get_environment_variable('mysql_db'),
    }

def get_environment_variable(variable_name):
    return os.environ.get(variable_name, "")


def insert_to_reporting(final_data, submitted_by):
    try:
        conn = mysql.connector.connect(**get_mysql_config())
        cursor = conn.cursor()
        insert_query = "INSERT INTO v_daily_reporting (project_channel, what_done_today, what_plan_tomorrow, blocker, submitted_by, submission_time) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (final_data['channel'], final_data['what_have_you_done_today'], final_data['what_is_your_plan_for_tomorrow'], final_data['any_blocker'], submitted_by, int(time.time()))
        cursor.execute(insert_query, values)
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def insert_to_project_agile(final_data, submitted_by):
    try:
        conn = mysql.connector.connect(**get_mysql_config())
        cursor = conn.cursor()
        insert_query = "INSERT INTO v_project_agile (project_channel, project_summary, submitted_by, submission_time) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (final_data['channel'], final_data['summary'], submitted_by, int(time.time()))
        cursor.execute(insert_query, values)
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def insert_to_leads(final_data, submitted_by):
    try:
        conn = mysql.connector.connect(**get_mysql_config())
        cursor = conn.cursor()
        insert_query = "INSERT INTO v_sales_leads (client_name,client_email,region,project_type,company,linkedin,project_description,next_step,submitted_by,submitted_on,lead_source) VALUES (%s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s)"
        values = (final_data['client_name'], final_data['client_email'], final_data['country'], final_data['project_type'],final_data['company'],final_data['linkedin'],final_data['description'],final_data['next_step'], submitted_by, int(time.time()),final_data['lead_source'])
        cursor.execute(insert_query, values)
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
