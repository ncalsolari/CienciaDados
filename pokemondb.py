import json
import re
import time
import requests
import os
from bs4 import BeautifulSoup as BSoup


def extract_attributes(colunapok, dadosdescartaveis, evolucao):
	dados = {}

	if dadosdescartaveis>0:
		

		aux = colunapok.find('td', {'class': 'name'})
		nome = aux.find('a')
		pattern = re.compile(r'>.+<')
		res = pattern.search(str(nome))
		x=res.group()
		x = x.split(">")
		x = x[1].split("<")
		x= x[0]
		dados['Nome'] = x
		

		
		aux = colunapok.find('td', {'class': 'type2'})
		tipo = aux.find_all('img')
		for t in range(len(tipo)):
			dados['Tipo' + str(t+1)] = tipo[t].get("alt")
		if len(tipo) < 2:
			dados['Tipo2'] = None



		aux = colunapok.find('td', {'class': 'ability'})
		habilidade = aux.find('a')
		res = pattern.search(str(habilidade))
		x=res.group()
		x = x.split(">")
		x = x[1].split("<")
		x= x[0]
		dados['Habilidade'] = x

		ovo = colunapok.find('td', {'class': 'egg-group'})
		results = re.split(r"\n+", str(ovo))
		
		if len(results) > 3:
			ovo = results[1].split("<br>")
			ovo2 = results[2].split("<br>")
			
			dados['Ovo'] = str(ovo[0] + ' ' + ovo2[0])
		else:
			ovo = results[1].split("<br>")

			dados['Ovo'] = str(ovo[0])
			

		
		indice = 0
		pattern = re.compile(r'>.+<')
		aux = colunapok.find_all('td', {'class': 'stat'})
		for a in aux:
			res = pattern.search(str(a))
			x=res.group()
			x = x.split(">")
			x = x[1].split("<")
			x= x[0]
			dados['Status' + str(indice)]=x
			indice += 1


		
		if evolucao == ['evolution-depth-2'] or evolucao == ['evolution-depth-3']:
			dados['Evolucao'] = 1
		else:
			dados['Evolucao'] = 0





	return dados
		


def extract_pokemons(htmlpage):

	bd_final = {}
	soup = BSoup(htmlpage.text,'html.parser')
	links = soup.find_all('tr')
	# evol = soup.tr['class']
	tempo = 0
	for l in links:
		
		# time.sleep(1)
		evol=l['class']
		

		data = extract_attributes(l, tempo, evol)
		bd_final[tempo] = data

		os.system('clear') or None
		print('Pokemons analisados:' , tempo)
		tempo += 1
		if tempo==965: #965
			break
			

	return bd_final



page = requests.get(
	'https://veekun.com/dex/pokemon/search?sort=evolution-chain&introduced_in=1&introduced_in=2&introduced_in=3&introduced_in=4&introduced_in=5&introduced_in=6&introduced_in=7')

pokebd = extract_pokemons(page)

print(pokebd)

with open('bdpokemon-evoluc.json','w') as f:
	json.dump(pokebd,f)

