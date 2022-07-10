from flask import Flask 
import redis 
from rq import Queue
from get_url import count_words_at_url
from flask import request

app = Flask(__name__)

r = redis.Redis(host="redis",port=6379)

q = Queue(connection=r)



@app.route('/')
def index():
    url = 'http://nvie.com'
    # if request.method == "POST":
    #     url = request.FORM("url")
    html = " "
    task = q.enqueue(count_words_at_url,url)
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
