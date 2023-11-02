import json
import urllib.parse
import base64
import requests
import mysql.connector
import os
import time


def get_environment_variable(variable_name):
    return os.environ.get(variable_name, "")


def get_slack_token():
    return get_environment_variable('slack_bot_token')


def get_mysql_config():
    return {
        'user': get_environment_variable('mysql_user'),
        'password': get_environment_variable('mysql_pwd'),
        'host': get_environment_variable('mysql_host'),
        'database': get_environment_variable('mysql_db'),
    }


def insert_to_database(final_data, submitted_by):
    try:
        conn = mysql.connector.connect(**get_mysql_config())
        cursor = conn.cursor()
        insert_query = "INSERT INTO v_project_agile (project_channel, project_summary, submitted_by, submission_time) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (final_data['channel'], final_data['project_summary'], submitted_by, int(time.time()))
        cursor.execute(insert_query, values)
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def open_modal(trigger_id, modal_data):
    slack_api_url = "https://slack.com/api/views.open"
    headers = {
        "Authorization": f"Bearer {get_slack_token()}",
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "trigger_id": trigger_id,
        "view": modal_data
    }
    print("request paylad")
    print(payload)
    response = requests.post(slack_api_url, headers=headers, data=json.dumps(payload))
    print('request sent')
    print(response.json())
    return response.json()
    # return


def handle_model_submit(json_data_view):
    username = json_data_view.get('user', {}).get('username', "")
    state = json_data_view.get('view', {}).get('state', {})
    values = state.get('values', {})
    final_data = {}
    for key in values.keys():
        plain_text = values.get(key).get('plain_text_input-action')
        if key == 'project_channel':
            drop_down = values.get(key).get('actionId-0', {}).get('selected_conversation', "")
            final_data['channel'] = drop_down
        elif plain_text is not None:
            plain_text_value = values.get(key).get('plain_text_input-action', {}).get('value', "")
            final_data[key] = plain_text_value
    message_data = {
        'channel': final_data['channel'],
        'text': f"*Submitted By* <@{username}>\n"
                f">*Meeting Type * \n> {final_data['meeting_type']}\n\n"
                f">*Summary* \n> {final_data['summary']}"
    }
    headers = {
        "Authorization": f"Bearer {get_slack_token()}",
        "Content-Type": "application/json; charset=utf-8"
    }
    response = requests.post('https://slack.com/api/chat.postMessage', headers=headers, json=message_data)
    insert_to_database(final_data, username)
    rep = response.json()


def lambda_handler(event, context):
    print(event)
    body_base64 = event.get('body', "")
    body = base64.b64decode(body_base64).decode('utf-8')
    print(body)

    if 'payload' in body:
        query_parameters = urllib.parse.parse_qs(body)
        body_payload = query_parameters.get('payload', [''])[0]
        json_data_view = json.loads(body_payload)
        view_type = json_data_view.get('type', "")
        if view_type != 'view_submission':
            return
        handle_model_submit(json_data_view)
        final_resp = {
            "response_action": "clear"
        }
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(final_resp)
        }

    query_parameters = urllib.parse.parse_qs(body)
    token = query_parameters.get('token', [''])[0]
    team_id = query_parameters.get('team_id', [''])[0]
    team_domain = query_parameters.get('team_domain', [''])[0]
    channel_id = query_parameters.get('channel_id', [''])[0]
    channel_name = query_parameters.get('channel_name', [''])[0]
    user_id = query_parameters.get('user_id', [''])[0]
    user_name = query_parameters.get('user_name', [''])[0]
    command = query_parameters.get('command', [''])[0]
    text = query_parameters.get('text', [''])[0]
    trigger_id = query_parameters.get('trigger_id', [''])[0]

    print("TriggerId")
    print(trigger_id)
    
    print("Qery params")
    print(query_parameters)
    
    model_data = {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "Daily Reporting App",
            "emoji": True
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit",
            "emoji": True
        },
        "close": {
            "type": "plain_text",
            "text": "Cancel",
            "emoji": True
        },
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Submit your meeting summary!",
                    "emoji": True
                }
            },
            {
                "type": "actions",
                "block_id": "project_channel",
                "elements": [
                    {
                        "type": "conversations_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select project channel",
                            "emoji": True
                        },
                        "action_id": "actionId-0",
                        "response_url_enabled": True,
                        "default_to_current_conversation": True,
                        "initial_conversation": channel_id
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Meeting Type:"
                },
                "accessory": {
                    "type": "radio_buttons",
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Daily Sync Meeting",
                                "emoji": True
                            },
                            "value": "value-0"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Sprint Planning Meeting",
                                "emoji": True
                            },
                            "value": "value-1"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Project Demo Meeting",
                                "emoji": True
                            },
                            "value": "value-2"
                        }
                    ],
                    "action_id": "radio_buttons-action"
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "multiline": True,
                    "action_id": "plain_text_input-action"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Summary",
                    "emoji": True
                }
            }
        ]
    }
    open_modal(trigger_id, model_data)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        }
    }
