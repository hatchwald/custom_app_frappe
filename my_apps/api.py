import frappe 
import os
import json
import io
# from datetime import time
import time
@frappe.whitelist()

def execute_func(*args,**kwargs):
    DATA_FILE = "testing.json"
    if not os.path.exists(DATA_FILE):
        with io.open(os.path.join(DATA_FILE),'w') as data_files:
            datas = json.loads(time.time)
            json.dump(datas,data_files)
    else:
        with open(DATA_FILE,"w+") as file_data:
            crnt = json.loads(time.time)
            json.dump(crnt,file_data)    


    #     return {}
    # print("something are here")
    # print(kwargs)
