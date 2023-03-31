import frappe 
import os
import json
import io
from datetime import datetime
import time
import string
import random
import http.client
from frappe.utils import now,get_timestamp
import time

import urllib3

@frappe.whitelist()

def execute_func(*args,**kwargs):
    DATA_FILE = "testing.json"
    if not os.path.exists(DATA_FILE):
        with io.open(os.path.join(DATA_FILE),'w') as data_files:
            datas = "sss"
            json.dump(datas,data_files)
    else:
        with open(DATA_FILE,"w+") as file_data:
            crnt = args
            json.dump(crnt,file_data)    


    #     return {}
    # print("something are here")
    # print(kwargs)

def create_blogpost(title,body):
    # title = string.ascii_letters
    # title = " ".join(random.choice(title) for i in range(20))

    # body = "lorem ipsum sit dolor amet empty"    

    post = frappe.get_doc({"doctype":"BlogPost",
                           "title":title,
                           "body": body
                           })
    post.insert()
    frappe.db.commit()    

def something():
    pass

def after_insert_partner(doc,method=None):
    frappe.utils.logger.set_log_level("DEBUG")
    logger = frappe.logger("api", allow_site=True, file_count=50)
    logger.info(doc)
    partner = frappe.get_doc('Partner',doc)
    some = frappe.as_json(doc)
    logger.info(some)
    conn = http.client.HTTPSConnection("discord.com")
    payload = json.dumps({
        "content":"partner was created",
        "tts":False,
        "embeds":[
            {
                "title":"partner data was posted",
                "description":some,
                "color":"178940",
                "timestamp":now()
            }
        ]
    })
    headers = {
        "Content-Type":"application/json"
    }

    conn.request("POST","/api/webhooks/1060092841046573076/KIrhiSKmeSvS0nBi0RGxzZ-gafWhVbDkx33ZBvEIjb42wxZMxAVlF4a5FbEwBbkCM4Jn",payload,headers)
    res = conn.getresponse()
    if res.status == 200 or res.status == 204:
        pass
    else:    
        title = "Error " + str(res.status)
        message = "Some error heppen ! check your log or your connection"
        return frappe.msgprint(msg=message,title=title)
          