import requests
import smtplib
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from datetime import datetime
from json import *

load_dotenv()

class Sites:
    def __init__(self, name, url, target_job_title):
        self.name = name
        self.url = url
        self.target_job_title = target_job_title

SITES = [
    Sites("redgate", "https://www.red-gate.com/our-company/careers/current-opportunities/", "software engineer")
]
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,de;q=0.8,fr;q=0.6,en;q=0.4,ja;q=0.2",
    "Dnt": "1",
    "Priority": "u=1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Sec-Gpc": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
}

email_body = ""

def append_email_body(body, company, jobs):
    if jobs:
        body += f"{company.title()}: \n"
        for j in jobs:
            body += f"{j} \n"
    return body

def process_jobs(body, target_job_title, company, applied_jobs, jobs):
    output_jobs = []

    for job in jobs:
        if target_job_title in job.getText().lower() and job.getText().lower() not in applied_jobs:
            output_jobs.append(f"{job.getText()} {s.url + job["href"]}")
    return append_email_body(body, company, output_jobs)

for s in SITES:
    site = requests.get(s.url, headers=HEADERS).text
    soup = BeautifulSoup(site, "html.parser")
    try:
        with open("applied_jobs.json") as file:
            applied_jobs = load(file)[s.name]
    except FileNotFoundError:
        new_dict = {s.name:[] for s in SITES}
        dump(new_dict, open("applied_jobs.json", "w"), indent=4)
        applied_jobs = []
    except KeyError:
        with open("applied_jobs.json") as file:
            current_dict = load(file)
            current_dict.update({s.name: []})
            dump(current_dict, open("applied_jobs.json", "w"), indent=4)
    except JSONDecodeError:
        dump({}, open("applied_jobs.json", "w"), indent=4)

    if s.name == "redgate":     
        jobs_section = soup.find(class_="tabbed__content")
        if "cambridge" in jobs_section.getText().lower() and s.target_job_title in jobs_section.getText().lower():
            for location_section in jobs_section.children:
                if "cambridge" in location_section.getText().lower() and s.target_job_title in location_section.getText().lower():
                    email_body = process_jobs(email_body, s.target_job_title, s.name, applied_jobs, location_section.select(".list--bare li a"))

try:
    open("log.txt", "a").write(f"Run: {str(datetime.now())[:19]} \n")
except FileNotFoundError:
    open("log.txt", "w").write(f"Run: {str(datetime.now())[:19]} \n")
            
if email_body:
    with smtplib.SMTP(os.environ["SMTP_ADDRESS"], port=587) as connection:
        connection.starttls()
        result = connection.login(os.environ["EMAIL_ADDRESS_FROM"], os.environ["EMAIL_PASSWORD"])
        connection.sendmail(
            from_addr=os.environ["EMAIL_ADDRESS_FROM"],
            to_addrs=os.environ["EMAIL_ADDRESS_TO"],
            msg=f"Subject:Weekly job alert!\n\n{email_body}".encode("utf-8")
        )