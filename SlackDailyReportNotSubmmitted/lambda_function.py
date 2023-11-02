import os
import requests
import mysql.connector
from datetime import datetime, timedelta

# Set your Slack API token

slack_token = os.environ.get("slack_bot_token")
mysql_db = os.environ['mysql_db']
mysql_host = os.environ['mysql_host']
mysql_pwd = os.environ['mysql_pwd']
mysql_user = os.environ['mysql_user']
exclude_user = ['wf_bot_a061hjvb6q25', 'vikas', 'hitesh.u','slack_bot_test','dhaval.m','colin.s']

mysql_config = {
    'user': mysql_user,
    'password': mysql_pwd,
    'host': mysql_host,
    'database': mysql_db,
}

def get_channels_with_int_suffix():
    headers = {
        "Authorization": f"Bearer {slack_token}"
    }

    params = {
        "limit": 200,
        "exclude_archived": "true",
        "types": "public_channel,private_channel"
    }

    all_channels = []

    while True:
        response = requests.get("https://slack.com/api/conversations.list", headers=headers, params=params)
        data = response.json()

        if not data["ok"]:
            print(f"Error: {data['error']}")
            return []

        channels = data["channels"]
        int_channels = [channel for channel in channels if channel["name"].endswith("-int")]
        #print(int_channels)
        all_channels.extend(int_channels)

        next_cursor = data.get("response_metadata", {}).get("next_cursor")
        if not next_cursor:
            break  # Break the loop if there's no more data

        params["cursor"] = next_cursor  # Use the cursor for the next request
    #print(all_channels)

    return all_channels

def get_usernames_in_channel(channel_id):
    headers = {
        "Authorization": f"Bearer {slack_token}"
    }

    params = {
        "channel": channel_id
    }

    response = requests.get("https://slack.com/api/conversations.members", headers=headers, params=params)
    #print(response)
    data = response.json()
    #print(data)

    if not data["ok"]:
        print(f"Error2: {data['error']}")
        return []

    user_ids = data["members"]
    #print("user_ids")
    #print(user_ids)
    usernames = []

    for user_id in user_ids:
        user_info = get_user_info(user_id)
        if user_info and not user_info.get("is_bot", True) and not user_info.get("is_restricted",True):
            usernames.append(user_info["name"])
    return usernames

def get_user_info(user_id):
    headers = {
        "Authorization": f"Bearer {slack_token}"
    }

    params = {
        "user": user_id
    }

    response = requests.get("https://slack.com/api/users.info", headers=headers, params=params)
    data = response.json()

    if not data["ok"]:
        print(f"Error4: {data['error']}")
        return None

    return data["user"]

def get_users_responded(channel_id, yesterday_epoch_time, users_in_channel):
    conn = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_pwd,
        database=mysql_db
    )
    
    cursor = conn.cursor(dictionary=True)
    
    users_in_channel = ', '.join([f'"{user_id}"' for user_id in users_in_channel])
    users_not_responded = []
    if users_in_channel:
	    query = f"""
	    SELECT distinct submitted_by FROM task.v_daily_reporting
	    WHERE submitted_by IN ({users_in_channel})
	    AND submission_time > {yesterday_epoch_time}
	    AND project_channel = '{channel_id}'
	    """
	    cursor.execute(query)
	    users_not_responded = cursor.fetchall()
	    #print(users_not_responded)    
    
    cursor.close()
    conn.close()
    
    return users_not_responded

def send_message_to_channel(channel_id, message, user_ids_to_mention=None):
    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json"
    }

    data = {
        "channel": channel_id,
        "text": message
    }
    
    if user_ids_to_mention:
        data["text"] += " " + " ".join([f"<@{user_id}>" for user_id in user_ids_to_mention])

    response = requests.post("https://slack.com/api/chat.postMessage", headers=headers, json=data)
    data = response.json()
    #print(data)

    if not data["ok"]:
        print(f"Error3: {data['error']}")
        
def get_users_not_responded(channel_id, yesterday_epoch_time, users_in_channel):
    users_responded = get_users_responded(channel_id, yesterday_epoch_time, users_in_channel)
    #print("users_responded")
    #print(users_responded)
    
    users_not_responded = [username for username in users_in_channel if username not in [user['submitted_by'] for user in users_responded]]
    users_not_responded = [user for user in users_not_responded if user not in exclude_user]
    
    return users_not_responded        

def lambda_handler(event, context):
    int_channels = get_channels_with_int_suffix()
    additional_channel = {"id": "C02BERLMVPA", "name": "trackimo"}
    int_channels.append(additional_channel)

    for channel in int_channels:
        channel_id = channel["id"]
        channel_name = channel["name"]
        users_in_channel = get_usernames_in_channel(channel_id)
        #print("users_in_channel")
        #print(users_in_channel)

        # Calculate yesterday's epoch time for 11:59 PM
        yesterday = datetime.now() - timedelta(days=1)
        yesterday = yesterday.replace(hour=23, minute=59, second=0, microsecond=0)
        yesterday_epoch_time = int(yesterday.timestamp())

        users_not_responded = get_users_not_responded(channel_id, yesterday_epoch_time, users_in_channel)
        print("users_not_responded")
        print(users_not_responded)

        if users_not_responded:
            message = channel_name + ": Participants who did not respond yet:\n"
            #send_message_to_channel('C03QYSV6R3R', message, users_not_responded)
            send_message_to_channel(channel_id, message, users_not_responded)
            
