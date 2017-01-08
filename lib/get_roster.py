
import requests
from bs4 import BeautifulSoup as bs4
from funcs import *


URL_PATTERN = "http://www.sports-reference.com/cbb/schools/{school_abbrev}/2017.html"

def get_player_info(row):
  player = {td.attrs.get('data-stat') : td.text.strip() for td in row.findAll('td')}
  return player

def height_to_inches(height):
  ft, inches = height.split('-')
  height_inches = int(ft)*12 + int(inches)
  return height_inches

def convert_players_heights_to_inches(players):
  for player in players:
    player['height'] = height_to_inches(player.get('height'))
  return players

def list_of_dicts_to_header_and_lists(list_of_dicts):
  headers = list_of_dicts[0].keys()
  lists = []
  for record in list_of_dicts:
    lists.append([record.get(column) for column in headers])
  return headers, lists

def get_team_roster(school_abbrev):
  url = URL_PATTERN.format(school_abbrev = school_abbrev)
  html = get_html(url)
  soup = soupify_html(html)
  tbl = get_table_by_id(soup, 'roster')
  rows = get_table_body_rows(tbl)

  players = convert_players_heights_to_inches([get_player_info(row) for row in rows])
  headers, players = list_of_dicts_to_header_and_lists(players)

  write_to_file(players, '../data/players-{school_abbrev}.csv'.format(school_abbrev = school_abbrev), headers = headers, sep = '\t') 


  def get_all_rosters():
    teams = load_teams()

if __name__ == '__main__':

  get_all_rosters()
