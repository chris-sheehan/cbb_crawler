
import requests
from bs4 import BeautifulSoup as bs4
from funcs import *
import time

logger = init_logging('../logs/get_rosters.log')
URL_PATTERN = "http://www.sports-reference.com/cbb/schools/{school_abbrev}/2017.html"

def get_player_info(row):
  row_head = row.find('th', {'data-stat' : 'player'})
  playerName = row_head.text
  playerId = row_head.attrs.get('data-append-csv')
  player = {td.attrs.get('data-stat') : td.text.strip() for td in row.findAll('td')}
  player['playerName'] = playerName
  player['playerId'] = playerId
  return player

def height_to_inches(height):
  ft, inches = height.split('-')
  height_inches = int(ft)*12 + int(inches)
  return height_inches

def convert_players_heights_to_inches(players):
  for player in players:
    try:
      player['height'] = height_to_inches(player.get('height'))
    except:
      continue
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

  filename = '../data/teams/players-{school_abbrev}.csv'.format(school_abbrev = school_abbrev)
  write_to_file(players, filename, headers = headers, sep = '\t') 
  logger.info('%s rows written to %s.' % (len(players), filename))

def get_all_rosters():
  teams = load_teams()
  for team, school_abbrev in teams[232:]:
    logger.info(team)
    get_team_roster(school_abbrev)
    time.sleep(1)

if __name__ == '__main__':

  get_all_rosters()
