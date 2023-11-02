import json
import urllib.parse
import base64
import requests
import mysql.connector
import os
import time

import log_database as logdb

def get_environment_variable(variable_name):
    return os.environ.get(variable_name, "")

def get_slack_token():
    return get_environment_variable('slack_bot_token')


def handleNewLead(state,username):
    values = state.get('values', {})
    # print(values)
    final_data = {}
    for key in values.keys():
        plain_text = values.get(key).get('plain_text_input-action')
        static_select = values.get(key).get('static_select-action')
        rich_text = values.get(key).get('rich_text_input-action')
        if plain_text is not None:
            plain_text_value = values.get(key).get('plain_text_input-action', {}).get('value', "")
            final_data[key] = plain_text_value
        elif static_select is not None:
            static_select_value = values.get(key).get('static_select-action', {}).get('selected_option', "").get("text",{}).get("text",{})
            final_data[key] = static_select_value
        elif rich_text is not None:
            
            print(values.get(key).get('rich_text_input-action', {}))
            print(values.get(key).get('rich_text_input-action', {}).get('rich_text_value', ""))
            print(values.get(key).get('rich_text_input-action', {}).get('rich_text_value', "").get("elements",[]))
            rich_textElements = values.get(key).get('rich_text_input-action', {}).get('rich_text_value', {}).get("elements",[]);
            
            for item in rich_textElements:
                item_type = item['type']
                
                if item_type == 'rich_text_section':
                    elements = item['elements']
                    
                    output_string=""        
                    
                    for item in elements:
                        if item['type'] == 'user':
                            userId = item['user_id']
                            output_string += f"<@{userId}>"
                        elif item['type'] == 'text':
                            output_string += item['text']

            
            
            final_data[key] = output_string
            
    #print(final_data)
    final_data['client_email'] = final_data['client_email']
    final_data['next_step'] = final_data['next_step']
    final_data['lead_source'] = final_data['lead_source']
    
    message_data = {
        'channel': "C042ACQNR1C",
        'text': f"*Submitted By* <@{username}>\n"
                f">*Client Name*: {final_data['client_name']}\n"
                f">*Client Email*: {final_data['client_email']}\n"
                f">*Country*: {final_data['country']}\n"
                f">*Project Type*: {final_data['project_type']}\n"
                f">*Lead Source*: {final_data['lead_source']}\n"
                f">*Company *: {final_data['company']}\n"
                f">*LinkedIn *: {final_data['linkedin']}\n"
                f">*Description *: {final_data['description']}\n"
                f">*Next Step* : {final_data['next_step']}"
    }
    headers = {
        "Authorization": f"Bearer {get_slack_token()}",
        "Content-Type": "application/json; charset=utf-8"
    }
    response = requests.post('https://slack.com/api/chat.postMessage', headers=headers, json=message_data)
    
    logdb.insert_to_leads(final_data, username)
    rep = response.json()
    
def handleScrumReport(state,username):
    values = state.get('values', {})
    #print(values)
    final_data = {}
    for key in values.keys():
        plain_text = values.get(key).get('plain_text_input-action')
        static_select = values.get(key).get('static_select-action')
        if key == 'project_channel':
            drop_down = values.get(key).get('actionId-0', {}).get('selected_conversation', "")
            final_data['channel'] = drop_down
        elif plain_text is not None:
            plain_text_value = values.get(key).get('plain_text_input-action', {}).get('value', "")
            final_data[key] = plain_text_value
        elif static_select is not None:
            static_select_value = values.get(key).get('static_select-action', {}).get('selected_option', "").get("text",{}).get("text",{})
            final_data[key] = static_select_value    
        #print(final_data)   
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
    logdb.insert_to_project_agile(final_data, username)
    rep = response.json()
    
def handleDailyReport(state,username):
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
                f">*What I've done today* \n> {final_data['what_have_you_done_today']}\n\n"
                f">*My plan for tomorrow* \n> {final_data['what_is_your_plan_for_tomorrow']}\n\n"
                f">*Any blockers* \n> {final_data['any_blocker']}"
    }
    headers = {
        "Authorization": f"Bearer {get_slack_token()}",
        "Content-Type": "application/json; charset=utf-8"
    }
    response = requests.post('https://slack.com/api/chat.postMessage', headers=headers, json=message_data)
    logdb.insert_to_reporting(final_data, username)
    rep = response.json()
