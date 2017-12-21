import json
from pprint import pprint
from time import time
import requests
import os

# Environment/Constant Variables #
SLACK_TOKEN 	= os.getenv('SLACK_TOKEN')
DRY_RUN		 	= (os.getenv('DRY_RUN','True') == 'True')

def main():
	sentry_messages = get_sentry_messages(get_channel_messages())
	delete_sentry_messages(sentry_messages)

def get_channel_id(channel_name):
	payload = {'token' : SLACK_TOKEN}
	response = requests.get('https://slack.com/api/channels.list', params=payload)
	channels = response.json()['channels']
	for channel in channels:
		if channel['name'] == channel_name:
			channel_id = channel['id']
	
	return channel_id

channel_id = get_channel_id('dev-assessment-learn')

def get_channel_messages():
	payload = {
		'token'		: SLACK_TOKEN,
		'channel' 	: channel_id,
		'count' 	: 1000
		}

	messages = []
	
	has_more = True
	while has_more:
		response = requests.get('https://slack.com/api/channels.history', params=payload)
		new_messages = response.json()['messages']
		has_more = response.json().get('has_more',False)
		message_count = len(new_messages)
		payload['latest'] = new_messages[message_count-1]['ts']
		messages += response.json()['messages']
	
	return messages

def get_sentry_messages(messages):
	sentry_messages = []
	for message in messages:
		if message.has_key('bot_id') and message['bot_id'] == 'B8EGG6PMM':
			sentry_messages.append(message)

	return sentry_messages

def delete_sentry_messages(sentry_messages):
	payload = {
	'token'		: SLACK_TOKEN,
	'channel' 	: channel_id,
	}
	print(DRY_RUN)
	if DRY_RUN:
		print('Would delete %d sentry messages' % len(sentry_messages))
	else:
		for message in sentry_messages:
			payload['ts'] = message['ts']
			response = requests.post('https://slack.com/api/chat.delete', params=payload)
			if response.status_code == 200:
				body = response.json()
				if body['ok']:
					log_message = 'Deleted Sentry message with timestamp %s' % body['ts']
				else:
					log_message = 'Failed to delete Sentry message with error: %s' % body['error']
			else:
				log_message = 'Rest communication failed with status code %d' % response.status_code

			with open('sentrylog.log', 'a') as f:
				f.write(log_message+'\n')