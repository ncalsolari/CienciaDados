import json
import re
import time
import requests
from bs4 import BeautifulSoup as BSoup


def find_value(val):
	match = re.search('\d+', val)
	if match is not None:
		return match.group(0)
	return match

def get_apt_info(htmlpage):

	apt = {}
	soup = BSoup(htmlpage.text, 'html.parser')
	res = soup.find('div', {'class': 'col-md-4 detalhes-imovel'})
	infos = res.find_all('p')

	apt_code = None
	for i in infos:
		text = i.text.strip()
		stext = text.split()
		first_part = stext[0]
		sec_part = ' '.join(stext[1:])

		if 'Código' in text:
			apt_code = sec_part
		elif 'R$' in text:
			apt['preco'] = float(sec_part.replace(',','.'))
			#teste = 1
		elif 'Finalidade' in text:
			apt['finalidade'] = sec_part
		elif 'Tipo' in text:
			apt['tipo'] = sec_part
		elif 'Bairro' in text:
			apt['bairro'] = sec_part
		elif 'Dorm' in text:
			apt['Dormitorios'] = find_value(first_part)
		elif 'Cozinha' in text:
			apt['Cozinha'] = find_value(first_part)
		elif 'Lavanderia' in text:
			apt['Lavanderia'] = find_value(first_part)
	return apt_code, apt

def extract_apts(htmlpage):

	apts_dict = {}
	soup = BSoup(htmlpage.text,'html.parser')
	links = [l['href'] for l in soup.find_all('a',{'class':'ver-mais'})]
	tempo = 0
	for apt_url in links:
		print(tempo)
		tempo += 1
		time.sleep(1)
		apt_page = requests.get(apt_url)
		apt_code, apt_data = get_apt_info(apt_page)
		apts_dict[apt_code] = apt_data
	return apts_dict


PAGE_ID = 2
page = requests.get(
	'https://predialsaocarlos.com/busca/?finalidade=2&tipo=A&dormitorios=1&valor-maximo=900%2C00'.format(PAGE_ID))

apts = extract_apts(page)
print(apts)

with open('apts.json','w') as f:
	json.dump(apts,f)

