from bs4 import BeautifulSoup
import requests
import json

url = 'https://betzona.ru/bestbets'
res = 'https://betzona.ru'

def grab(save=False):
	site = requests.get(url)
	soup = BeautifulSoup(site.text, features='html.parser')
	bestlist = soup.find('ul', 'list_best').find_all('div', {'class':'best'})
	bets = []

	for best in bestlist:
		bet = {}
		bet['first_command'] = best.find_all('span', {'class': 'name'})[0].text
		bet['second_command'] = best.find_all('span', {'class': 'name'})[1].text
		bet['tags'] = best.find('span', {'class': 'tags'}).text.replace('\n','')
		bet['date'] = best.find('span', {'class': 'date'}).text
		bet['prediction'] = best.find('span', {'class':'info'}).text
		bet['pfc'] = res + best.find_all('img')[0].get('src')
		bet['psc'] = res + best.find_all('img')[1].get('src')
		bets.append(bet)

	if save:
		with open('predictions.json', 'w', encoding='utf-8-sig') as f:
			f.write(json.dumps(bets, sort_keys=True, indent=4, ensure_ascii=False))
	return bets