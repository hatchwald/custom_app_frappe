# Copyright (c) 2023, jake and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import string
import random

class BlogPost(Document):
	pass
	titles = " ".join(random.choice(string.ascii_letters) for i in range(20))
	body = "lorem ipsum sit dolor amet "
	# frappe.enqueue("my_apps.api.create_blogpost",queue="short",job_name="created_blog_post",timeout=30000,title=titles,body=body)
