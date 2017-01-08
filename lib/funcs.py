
import argparse
import requests
from bs4 import BeautifulSoup as bsoup

TEAMS_PATH = '../data/teams2017.csv'

def load_teams():
  f = open(TEAMS_PATH, 'r')
  headers = f.readline().strip().split(',')
  teams = [ln.strip().split(',') for ln in f.readlines()]
  f.close()
  return teams

def get_html(url):
  resp = requests.get(url)
  if not resp.ok:
    raise
  html = resp.text
  return html
  
def soupify_html(html):
  soup = bsoup(html, 'html.parser') 
  return soup

def get_table_by_id(soup, tag_id):
  tbl = soup.find('table', {'id' : tag_id})
  return tbl
  
def get_table_body_rows(tbl):
  rows = tbl.find('tbody').findAll('tr')
  return rows

def write_to_file(rows, filename, headers = False, sep = ','):
  f = open(filename, 'w')
  if headers:
    f.write(sep.join(['%s'] * len(headers)) % tuple(headers) + '\n')
  write_format = sep.join(['%s'] * len(rows[0])) + '\n'
  for row in rows:
    f.write(write_format % tuple(row))
  f.close()
  print '%s rows written to %s.' % (len(rows), filename)



