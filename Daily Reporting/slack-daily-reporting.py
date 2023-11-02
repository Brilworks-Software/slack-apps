import json
import urllib.parse
import base64
import requests
import mysql.connector
import os
import time
import model_json as model
import log_database as logdb
import message_formatter as msgformat

def get_environment_variable(variable_name):
    return os.environ.get(variable_name, "")

def get_slack_token():
    return get_environment_variable('slack_bot_token')


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
    response = requests.post(slack_api_url, headers=headers, data=json.dumps(payload))
    return response.json()
    

def handle_model_submit(json_data_view):
    #print(json_data_view)
    username = json_data_view.get('user', {}).get('username', "")
    callback_id = json_data_view.get('view', {}).get('callback_id', {})
    state = json_data_view.get('view', {}).get('state', {})
    
    if callback_id == 'log_scrum_info':
        msgformat.handleScrumReport(state,username)
    elif callback_id == 'log_daily_report':
        msgformat.handleDailyReport(state,username)
    elif callback_id == 'log_lead':
        msgformat.handleNewLead(state,username)
    else:
        msgformat.handleDailyReport(state,username)


def lambda_handler(event, context):
    body_base64 = event.get('body', "")
    body = base64.b64decode(body_base64).decode('utf-8')
    
    if 'payload' in body:
        query_parameters = urllib.parse.parse_qs(body)
        body_payload = query_parameters.get('payload', [''])[0]
        json_data_view = json.loads(body_payload)
        view_type = json_data_view.get('type', "")
        
        #print("json_data_view")
        #print(json_data_view)
        if view_type == 'shortcut':
            callback_id = json_data_view.get('callback_id', {})
            trigger_id = json_data_view.get('trigger_id', {})
            
            if callback_id == 'log_daily_report':
                model_data = model.getLogDailyReportModalJson(callback_id)
            elif callback_id == 'log_scrum_info':
                model_data = model.getLogScrumInfoModalJson(callback_id)
            elif callback_id == 'log_lead':
                model_data = model.getNewLeadModalJson(callback_id)
            
            open_modal(trigger_id, model_data)
            resp = {
                "text": "Kindly fill Report!"
            }
            
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps(resp)
            }    
        elif view_type != 'view_submission':
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
                        "text": "Submit your reporting for the day!",
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
                    "type": "input",
                    "block_id": "what_have_you_done_today",
                    "element": {
                        "type": "plain_text_input",
                        "multiline": True,
                        "action_id": "plain_text_input-action"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "What you have done today?",
                        "emoji": True
                    }
                },
                {
                    "type": "input",
                    "block_id": "what_is_your_plan_for_tomorrow",
                    "element": {
                        "type": "plain_text_input",
                        "multiline": True,
                        "action_id": "plain_text_input-action"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "What your plan for tomorrow?",
                        "emoji": True
                    }
                },
                {
                    "type": "input",
                    "block_id": "any_blocker",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "plain_text_input-action",
                        "initial_value": "No"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Any blocker?",
                        "emoji": True
                    }
                }
            ]
        }
        
    open_modal(trigger_id, model_data)
    resp = {
        "text": "Kindly fill the Daily Report!"
    }
    

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(resp)
    }

