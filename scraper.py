from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

url = "https://catalog.fullerton.edu/preview_program.php?catoid=80&poid=38156&returnto=11049"

driver = webdriver.Chrome()
driver.get(url)
wait = WebDriverWait(driver, 100)

# fina all the course links
a_tags = driver.find_elements(By.CSS_SELECTOR, 'li.acalog-course a')

# click all course links to open the description
for tag in a_tags:
  driver.execute_script("arguments[0].scrollIntoView();", tag)
  tag.click()
  time.sleep(1)
  
# grab all the data from description
table = driver.find_elements(By.CSS_SELECTOR, 'li.acalog-course-open table')


# build a dataframe from the data with following columns
course_numbers = []
course_names = []
description = []
workload = []
prerequisits = []

for item in table:
  data = item.text
  data = data.split("]\n")[-1] # remove the extra item when it exists
  details = data.split('\n')
  course_number, course_name = details[0].split(' - ')
  course_numbers.append(course_number)
  course_names.append(course_name)

  description.append(details[1])

  wl = details[1].split("(")[-1].split(")")[0]
  workload.append(wl)

  prereq = None
  for part in details[2:]:
    print(part)
    if "Prerequisite" in part or "Corequisite" in part:
      prereq = part
      break
  if prereq and ":" in prereq:    
    prerequisits.append([p.strip() for p in prereq.split(":")[1].split(";")])
  else:
    prerequisits.append([])

data = {
    "course_number": course_numbers,
    "course_name": course_names,
    "description": description,
    "work_load": workload,
    "prerequisits": prerequisits
}

df = pd.DataFrame(data)
df.to_csv("course_data.csv")
