import requests
import bs4
from bs4 import BeautifulSoup

from pandas import Series, DataFrame
import pandas as pd
import time

URL = "https://www.indeed.com.sg/jobs?q=data+scientist&l=Singapore"
#conducting a request of the stated URL above:
page = requests.get(URL)
#specifying a desired format of “page” using the html parser - this allows python to read the various components of the page, rather than treating it as one long string.
soup = BeautifulSoup(page.text, "html.parser")
#printing soup in a more structured tree format that makes for easier reading
# print(soup.prettify())

def extract_job_title_from_result(soup): 
  jobs = []
  for div in soup.find_all(name="div", attrs={"class":"row"}):
  	for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
  		jobs.append(a["title"])
  return(jobs)

print(extract_job_title_from_result(soup))

def extract_company_from_result(soup): 
  companies = []
  for div in soup.find_all(name="div", attrs={"class":"row"}):
    company = div.find_all(name="span", attrs={"class":"company"})
    if len(company) > 0:
      for b in company:
        companies.append(b.text.strip())
    else:
      sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
      for span in sec_try:
      	companies.append(span.text.strip())
  return(companies)
 
print(extract_company_from_result(soup))

def extract_location_from_result(soup): 
  locations = []
  spans = soup.findAll("span", attrs={"class": "location"})
  for span in spans:
  	locations.append(span.text)
  return(locations)

print(extract_location_from_result(soup))

max_results_per_city = 100
city = "Singapore"
columns = ["city", "job_title", "company_name", "location", "summary", "salary"]
sample_df = pd.DataFrame(columns = columns)
job_posts = []
page_id = 0
for page_id in range(100):
  if page_id < 100:
  # get the url
    if page_id==0:
      page = requests.get('https://www.indeed.com.sg/jobs?q=data+scientist&l=' + str(city))
    else:
      page = requests.get('https://www.indeed.com.sg/jobs?q=data+scientist&l=' + str(city) + "&start=" + str(page_id))

    page_id = page_id + 10
    soup = BeautifulSoup(page.text, "lxml", from_encoding="utf-8")
    for div in soup.find_all(name="div", attrs={"class":"row"}): 
      #specifying row num for index of job posting in dataframe
      num = len(sample_df) + 1
      #creating an empty list to hold the data for each posting
      job_post = [] 
      #append city name
      job_post.append(city) 
      #grabbing job title
      for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
        job_post.append(a["title"]) 
      #grabbing company name
      company = div.find_all(name="span", attrs={"class":"company"}) 
      if len(company) > 0: 
        for b in company:
          job_post.append(b.text.strip()) 
      else: 
        sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
        for span in sec_try:
          job_post.append(span.text) 
      #grabbing location name
      c = div.findAll("span", attrs={"class": "location"}) 
      for span in c: 
        job_post.append(span.text) 
      #grabbing summary text
      d = div.findAll("span", attrs={"class": "summary"}) 
      for span in d:
        job_post.append(span.text.strip()) 
      #grabbing salary
      try:
        job_post.append(div.find("nobr").text) 
      except:
        try:
          div_two = div.find(name="div", attrs={"class":"sjcl"}) 
          div_three = div_two.find("div") 
          job_post.append(div_three.text.strip())
        except:
          job_post.append("Nothing_found") 
      # appending list of job post info to dataframe at index num
      # print (job_post)

      series_1=Series(job_post)
      job_posts.append(series_1)
      print(series_1)
      # sample_df.loc[num] = series_1

job_posts = pd.DataFrame(job_posts)
#saving sample_df as a local csv file — define your own local path to save contents 
job_posts.to_csv("/Users/shirley/Desktop/indeed_job.csv", encoding="utf-8")
