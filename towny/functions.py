import requests
from yaml import safe_load, load as yaml_load
from bs4 import BeautifulSoup 
import re
config = safe_load(open('./config.yaml','r'))
updates_url = config.get('url')
get_town_name = re.compile("(.*?)\s*\(")
get_nation_name =  re.compile(".*?\((.*?)\)")

if not updates_url:
	raise ValueError('You need to input \'url\' in config.yaml!')

def get_updates():
	return requests.get(updates_url).json()

def parse_desc(desc):
	'''minetown'''
	players = []
	town = ''
	mayor = ''
	nation = ''
	settings = ''
	parsed = BeautifulSoup(f'<html><body>{desc}</body></html>','html.parser')
	regioninfo = parsed.find('div','regioninfo')
	if not regioninfo:
		return
	# getting mayor
	mayor = regioninfo.findAll('span')[2].findAll('span')[1].text.replace(' ','')
	

	# getting town
	town = regioninfo.findAll('span')[0].text

	# getting nation
	nation =regioninfo.findAll('span')[7].text.replace('Нация: ','')

	players_raw = regioninfo.findAll('span')[27]
	players_raw = players_raw.text.split(':')[1:][0]
	for player in players_raw.split(','):
		players.append(player.replace(' ',''))
	print(players)
	return {
	'town': town,
	'mayor':mayor,
	'nation':nation,
	'players':players,
	'settings': settings
	}
	# getting players

   
	'''elitecrew'''

	# town = ''
	# mayor = ''
	# nation = ''
	# settings = ''
	# parsed = BeautifulSoup(f'<html><body>{desc}</body></html>','html.parser')
	# infowindow = parsed.find('div','infowindow')
	# if not infowindow:
	# 	return

	# # getting mayor
	# mayor = infowindow.findAll('span')[1].text

	# # getting town
	# town = get_town_name.match(infowindow.findAll('span')[0].text).group(1).replace(' ','')

	# # getting nation
	# nation = get_nation_name.match(infowindow.findAll('span')[0].text).group(1).replace(' ','')
	# # getting players

	# # getting settings
	# settings = infowindow.findAll('span')[3].text
	
	# for player in infowindow.findAll('span')[2].text.split(','):
	# 	players.append(player.replace(' ',''))
	
	# return {
	# 'town': town,
	# 'mayor':mayor,
	# 'nation':nation,
	# 'players':players,
	# 'settings': settings
	# }

def get_towns_info():
	updates = get_updates()['updates']
	towns = {}
	for update in updates:
		label = update.get('label')
		if towns.get(label) is None:
			data = {}
			data = parse_desc(update.get('desc'))
			towns.update({label:data})
	return towns
			

def player_by_info():
	players = {}
	towns = get_towns_info()

	for town in towns:
		town = towns[town]
		if not town:
			continue
		for player in town.get('players',[]):
			players.update(
				{player:{
					'nick':player,
					'town':town.get('town'),
					'nation':town.get('nation'),
					'is_mayor':bool(town.get('mayor') == player)
					}

				}
			)
	return players

