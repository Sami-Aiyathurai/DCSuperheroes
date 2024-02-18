import requests
import lxml
from bs4 import BeautifulSoup
import re
from queue import Queue
import csv

# might make a function to check if is a superhero
def getLinks(href):
    return href and re.compile("wiki/").search(href) and not re.compile("Category").search(href) and not re.compile("wikipedia", re.IGNORECASE).search(href) and not re.compile("http").search(href) and not re.compile("Help").search(href) and not re.compile("Special").search(href) and not re.compile("disambiguation").search(href)

def main():
  # read in list of heroes to limit scope
  file = open("list2.txt", "r") 
  data = file.read() 
  heroes = data.split("\n")
  queue = Queue() 
  marked = []
  extras = []

  root_url = "https://en.wikipedia.org"
  superman = "/wiki/Superman"
  queue.put(superman)
  marked.append("Superman")
  
  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
  }
  while not queue.empty():
    hero_url = queue.get()
    full_url = root_url + hero_url
    f = requests.get((full_url), headers = headers)
    soup = BeautifulSoup(f.content, 'lxml')
    links = soup.find_all(href=getLinks, limit= 50)
    for link in links:
        text = link.string
        if text in heroes:
          if text not in marked:
            queue.put(link.get("href"))
            marked.append(text)
            print("Hero Found: ", text)
        else:
          if text not in extras:
            extras.append(text)
  print("made it!")
  print()
  print("Heroes")
  for hero in marked:
     print(hero)
  print()
  print("Extras")
  for link in extras:
     print(link)

if __name__ == "__main__":
    main()