import json
from pprint import pprint
from time import time
import requests
import os

user_ids = [

	]

# Environment/Constant Variables #
SLACK_TOKEN 	= os.getenv('SLACK_TOKEN')
DRY_RUN		 	= (os.getenv('DRY_RUN','True') == 'True')

def get_channel_id(channel_name):
	payload = {'token' : SLACK_TOKEN}
	response = requests.get('https://slack.com/api/channels.list', params=payload)
	channels = response.json()['channels']
	for channel in channels:
		if channel['name'] == channel_name:
			channel_id = channel['id']
	
	return channel_id

def invite_members(channel_id,user_ids):
	for user_id in user_ids:
		payload =  {'token'   : SLACK_TOKEN,
					'channel' : channel_id,
					'user'    : user_id}
		response = requests.get('https://slack.com/api/channels.invite', params=payload)
		response.raise_for_status()

channel_id = get_channel_id('dataproductandboston')
invite_members(channel_id,user_ids)