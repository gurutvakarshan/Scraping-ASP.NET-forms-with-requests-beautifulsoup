from bs4 import BeautifulSoup
import requests
import json
def aspx_scrape():

	head_list = []
	data_list = []
	page = requests.get('https://www.icsi.in/student/Members/MemberSearch.aspx')

	soup=BeautifulSoup(page.content, "html.parser")
	VIEWSTATE=soup.find(id="__VIEWSTATE")['value']
	VIEWSTATEGENERATOR=soup.find(id="__VIEWSTATEGENERATOR")['value']
	EVENTVALIDATION=soup.find(id="__EVENTVALIDATION")['value']
	VIEWSTATEENCRYPTED = soup.find(id="__VIEWSTATEENCRYPTED")['value']

	Join_Group ={'dnn$ctr410$MemberSearch$txtCpNumber':'16803','__EVENTTARGET':'dnn$ctr410$MemberSearch$btnSearch', '__EVENTARGUMENT':'','__VIEWSTATEENCRYPTED':VIEWSTATEENCRYPTED,'__LASTFOCUS':'', '__VIEWSTATE':VIEWSTATE, '__VIEWSTATEGENERATOR':VIEWSTATEGENERATOR, '__EVENTVALIDATION':EVENTVALIDATION} 
	join = requests.post('https://www.icsi.in/student/Members/MemberSearch.aspx', data=Join_Group)
	soup = BeautifulSoup(join.content,'lxml')
	# iter = soup.find_all("td",{"class":"chart_detail"})
	iteration = soup.find_all("div",{"class":"chart_att"})

	for each in iteration:
		heads = each.find_all("td",{"class":"chart_head"})
		data = each.find_all("td",{"class":"chart_detail"})
		for each in heads:
			head_list.append(each.get_text().strip('\r\n\t'))
		for each in data:
			data_list.append(each.get_text().strip('(*)\n'))
	json_data = json.dumps(dict(zip(head_list,data_list)))
	print json_data