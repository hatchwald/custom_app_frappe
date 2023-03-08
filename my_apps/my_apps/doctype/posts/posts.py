# Copyright (c) 2023, jake and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import json
import http.client
import frappe
from frappe.model.naming import getseries
import time
from frappe.utils import (getdate,nowdate)
import re

class posts(Document):
	TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImZpbm4iLCJpYXQiOjE2NzgyNDY5OTUsImV4cCI6MTY3ODMzMzM5NX0.rfpCkfJgHBab9sJU0aCRSrbozTTj8B_Sm7A1AeaWQmo"
	
	def http_data(method,target,payload):
		conn = http.client.HTTPConnection("localhost:2828")
		headersList = {
		"Accept": "*/*",
		"Authorization": "Bearer "+posts.TOKEN,
		"Content-Type": "application/json"
		}
		conn.request(method,target,payload,headersList)
		response = conn.getresponse()
		return response

	def sorted_data(self) -> list:
		return self.get('title')			
	@staticmethod
	def whitelist(fn):
		frappe.whitelist()(fn)
		return fn
	
	@frappe.whitelist()
	def get_current_data(sort_key=None,reverse=True) -> dict[str,dict]:
		result = posts.http_data("GET","/api/blog","")
		if result.status != 200 :
			title = "Error " + str(result.status)
			message = "Some error heppen ! check your log or your connection"
			return frappe.msgprint(msg=message,title=title,raise_exception=FileNotFoundError)
		print("get current data")
		result = result.read()
		f_data = json.loads(result)
		data_msg = f_data['message']
		key_sort = 'date' if sort_key == None else sort_key
		print(data_msg)
		if any(key_sort in keys for keys in data_msg):
			key_sort = key_sort
		else:
			key_sort = 'date'
		print(key_sort)		 
		# datas = data_msg.sort(key=lambda k: k[key_sort],reverse=reverse)
		print(data_msg)
		datas_arr = {}
		for x in f_data['message']:
			x['name'] = x['id']
			x['owner'] = x['author']
			x['creation'] = x['date']
			datas_arr[x['id']] = x
		data_final = json.dumps(datas_arr)	
		return json.loads(data_final)
		print(result.decode("utf-8"))
		
		with open (article.DATA_FILE) as f:
			return json.load(f)

	@staticmethod
	def update_data(self,*args,**kwargs) -> None:
		payload = json.dumps(self)
		result = posts.http_data("PUT",'/api/blog/1'+self['name'],payload)
		if result.status != 200 :
			title = "Error " + str(result.status)
			result_final = result.read()
			result_finals = json.loads(result_final)
			if result_finals['message'] is None:
				message = "Some error heppen ! check your log or your connection"
			else:	
				message = result_finals['message']
			return frappe.msgprint(msg=message,title=title,raise_exception=FileNotFoundError)
		print(result)

	def db_insert(self, *args, **kwargs) -> None:
		d = self.get_valid_dict(convert_dates_to_str=True)
		
		payload = json.dumps(d)

		result = posts.http_data("POST","/api/blog",payload)
		result = result.read()
		f_data = json.loads(result)
		self.name = f_data['data']['id_blog']
		
		
	@frappe.whitelist()
	def load_from_db(self):
		data = self.get_current_data()
		d = data.get(self.name)
		
		super(Document,self).__init__(d)

	def db_update(self,*args,**kwargs):
		d = self.get_valid_dict(convert_dates_to_str=True)
		self.update_data(d)

	def delete(self):
		result = posts.http_data("DELETE","/api/blog/"+self.name,"")
		print(result)
		
	@frappe.whitelist()
	# @staticmethod
	def get_list(args):
		print("get list")
		order_key = args['order_by']
		order_key = order_key.replace("`tabposts`.","")
		order_key = order_key.replace("`","")
		order_key = re.split("\s",order_key)
		reverse_order = True
		if order_key[1] == "asc":
			reverse_order = False

		print(order_key)
		data = posts.get_current_data(order_key[0],reverse_order)
	

		return [frappe._dict(doc) for name, doc in data.items()]

	@staticmethod
	def get_count(args):
		data = posts.get_current_data()
		return len(data)

	@staticmethod
	def get_stats(args):
		return {}

