from flask import Flask 
import redis 
from rq import Queue
from . import get_url
from flask import request

app = Flask(__name__)

r = redis.Redis(host="127.0.0.1",port=6379)

q = Queue(connection=r)

def report_sucess(job, connection, result):
    print(job)
    print(job.get_status())

def report_failure(job, connection, result):
    print(job)



@app.route('/')
def index():
    url = 'http://nvie.com'
    # if request.method == "POST":
    #     url = request.FORM("url")
    html = " "
    task = q.enqueue(get_url.count_words_at_url,url,on_success=report_sucess,on_failure=report_failure)
    
    for job in q.jobs:
        html = f"<a href= job/{job.id}>{job.id}</a>"

    html+= f"Total {len(q.jobs)} jobs in the queue"

    return f"{html}"

@app.route('/job/<job_id>')
def get_job(job_id):

    res = q.fetch_job(job_id)

    if not res.result:
        return f"<p>Job is {res.get_status()}</p><br /> Queued at:{res.enqueued_at}"
    else:
        return f"the result is: {res.result}"
