import requests
import pandas as pd
import openpyxl
from  bs4 import BeautifulSoup

URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="ResultsContainer")

job_elements = soup.findAll("div", class_="card-content")

jobs = {
    "title": [],
    "company": [],
    "content": [],
    "location": [],
    "date": []
}

for job_element in job_elements:
    
    url_jobs = job_element.findAll("a")[1]["href"]
    job_page = requests.get(url_jobs)
    soup_job = BeautifulSoup(job_page.content, "html.parser")
    content_soup_job = soup_job.find(id="ResultsContainer")

    title = content_soup_job.find("h1", class_="title")
    company = content_soup_job.find("h2", class_="company")
    content = content_soup_job.find("div", class_="content").find("p")
    location = content_soup_job.find("p", id="location")
    date = content_soup_job.find("p", id="date")

    jobs["title"].append(title.text.strip())
    jobs["company"].append(company.text.strip())
    jobs["content"].append(content.text.strip())
    jobs["location"].append(location.text.strip()[10:])
    jobs["date"].append(date.text.strip()[-8:])

df = pd.DataFrame()

df["title"] = jobs["title"]
df["company"] = jobs["company"]
df["content"] = jobs["content"]
df["location"] = jobs["location"]
df["date"] = jobs["date"]

df.to_csv("./test.csv")