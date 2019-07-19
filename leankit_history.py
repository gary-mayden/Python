import requests
import json
import csv

#CONSTANTS
url_pre = "https://pluralsight.leankit.com/kanban/api/board/"
url_post = "/AssignUserLite"
note = "Reassigning after provisioning issue on July 11"
headers = {
    'Content-Type': "application/json",
    'Authorization': "",
    'User-Agent': "PostmanRuntime/7.15.0",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "",
    'Host': "pluralsight.leankit.com",
    'accept-encoding': "gzip, deflate",
    'content-length': "116",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }


with open('leankit_assign.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    row_count = 0
    for row in reader:
        row_count += 1
        if row_count <= 5110:
            print("Skipping row")
            continue

        url = url_pre + str(row['board_id']) + url_post

        payload = {'CardId'             :   row['\ufeffcard_id'],
                   'UserId'             :   row['user_id'],
                   'OverrideComment'    :   note}

        formattedpayload = json.dumps(payload)

        try:
            response = requests.request("POST", url, data=formattedpayload, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            print ("Unknown: Something Else",err)

        body = response.json()
        print(str(body['ReplyText']) + " " + str(payload))