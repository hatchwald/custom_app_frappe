import frappe
import re
from frappe.core.doctype.rq_job.rq_job import RQJob
from rq.job import Job
from frappe.utils import (
	cint,
	compare,
	convert_utc_to_user_timezone,
	create_batch,
	make_filter_dict,
)
from frappe.utils.background_jobs import get_queues, get_redis_conn

class RQjobs(RQJob):
    def get_list(args):
        start = cint(args.get("start")) or 0
        page_length = cint(args.get("page_length")) or 20

        order_desc = "desc" in args.get("order_by", "")

        matched_job_ids = RQJob.get_matching_job_ids(args)

        jobs = []
        for job_ids in create_batch(matched_job_ids, 100):
            jobs.extend(
                serialize_job(job)
                for job in Job.fetch_many(job_ids=job_ids, connection=get_redis_conn())
                if job and for_current_site(job)
            )
            if len(jobs) > start + page_length:
                # we have fetched enough. This is inefficient but because of site filtering TINA
                break

        return sorted(jobs, key=lambda j: j.modified, reverse=order_desc)[start : start + page_length]

def for_current_site(job: Job) -> bool:
	return job.kwargs.get("site") == frappe.local.site

def serialize_job(job: Job) -> frappe._dict:
	modified = job.last_heartbeat or job.ended_at or job.started_at or job.created_at
	job_name = job.kwargs.get("kwargs", {}).get("job_type") or str(job.kwargs.get("job_name"))
    
    
	# function objects have this repr: '<function functionname at 0xmemory_address >'
	# This regex just removes unnecessary things around it.
	if matches := re.match(r"<function (?P<func_name>.*) at 0x.*>", job_name):
		job_name = matches.group("func_name")
    
	return frappe._dict(
		name=job.id,
		job_id=job.id,
		queue=job.origin.rsplit(":", 1)[1],
		job_name=job_name,
		status=job.get_status(),
		started_at=convert_utc_to_user_timezone(job.started_at) if job.started_at else "",
		ended_at=convert_utc_to_user_timezone(job.ended_at) if job.ended_at else "",
		time_taken=(job.ended_at - job.started_at).total_seconds() if job.ended_at else "",
		exc_info=job.exc_info,
		arguments=frappe.as_json(job.kwargs),
		timeout=job.timeout,
		creation=convert_utc_to_user_timezone(job.created_at),
		modified=convert_utc_to_user_timezone(modified),
		_comment_count=0,
        socket_rq=(frappe.get_conf().redis_queue).rsplit(":")[2]
	)