import requests
import re
from bs4 import BeautifulSoup
import json
import smtplib
import os

def send_email(jobs):
    sender = os.environ['EMAIL_ADDRESS']
    receivers = 'nicmatth@cisco.com'
    server = smtplib.SMTP(os.environ['EMAIL_SERVER']+":587")
    message = """From: nicmatth-test@cisco.com
To:nicmatth@cisco.com
Subject: New jobs found

This is a job alert from nicmatth-script-v0.1.0.
    """
    for job in jobs:
        message += '\n' + job['title'] + '\n' + job['link'] +'\n'
    server.starttls()
    server.login(os.environ['EMAIL_ADDRESS'],os.environ['EMAIL_PASSWORD'])
    try:
        server.sendmail(sender, receivers, message)  
    except:
        server.sendmail(sender, receivers, "\n\nData Failed")

longurl = "https://www2.apply2jobs.com/RSS/index.cfm?fuseaction=RSSSearch&UUID=AD5852FF-BDB9-44EE-78C577568756A0B6&Lang=en&Params=2$0a74ZWOTmJIelkcLP-FaFUotawlrdM0U58bCQgIkH9xVN7Y3jVBozRBp6i_cEyGF1V-oqb4uHDEMHLNAstgt4HNXLJrwlGY6jJP6RChM0YVwLn43lW0fUr7amlnL5d9cERL7NZDDMuGDE56yLwRsPKAA2Ppn6bWZFC_FTt6L1m3M65zOdjhfWNLHhIzr5Rmg$tHfWag6QXz2PA26CFmRcbEelDU8FRml21bDC8IsL4D0"


def getjobs(url):
    r = requests.get(url)

    soup = BeautifulSoup(r.text)
    items = soup.findAll('item')
    jobs = []

    for item in items:
        title = str(item.title.text)
        results = re.search('(https.*=)([0-9]+)',item.text)
        link = str(results.group(1)) + str(results.group(2))
        jid = str(results.group(2))
        jobs.append( { 'jid' : jid , 'title' : title, 'link' : link } )
    
    return jobs

def get_difference(old_jobs, jobs):
    new_jobs = []
    for job in jobs:
        found = False
        for ojob in old_jobs:
            if job['jid'] == ojob['jid']:
                print "%r  %r" % (job['jid'], ojob['jid'])
                found = True
        if found == False:
            new_jobs.append(job)
    return new_jobs


o = open('/home/ubuntu/jobsearch/sdn.db','w+')
try:
    old_jobs = json.load(o)
except:
    old_jobs = []
jobs = getjobs(longurl)

new_jobs = get_difference(old_jobs, jobs) # switch to old_jobs,jobs after test
send_email(new_jobs)
#send_email(jobs)
print new_jobs

json.dump(jobs,o)
o.close()




