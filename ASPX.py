import requests
from bs4 import BeautifulSoup
import json

class ASPX__doPostBack:
	def __init__(self,base_url,cp_no):
		self.base_url = base_url
		self.cp_no = cp_no
		self.url = None	
		self.param = None
		self.head_list = []
		self.data_list = []

	def get_base_url(self):
		self.url = requests.get(self.base_url)	
		soup=BeautifulSoup(self.url.content, "html.parser")
		VIEWSTATE=soup.find(id="__VIEWSTATE")['value']
		VIEWSTATEGENERATOR=soup.find(id="__VIEWSTATEGENERATOR")['value']
		EVENTVALIDATION=soup.find(id="__EVENTVALIDATION")['value']
		VIEWSTATEENCRYPTED = soup.find(id="__VIEWSTATEENCRYPTED")['value']
		self.param ={'dnn$ctr410$MemberSearch$txtCpNumber':str(self.cp_no),'__EVENTTARGET':'dnn$ctr410$MemberSearch$btnSearch', '__EVENTARGUMENT':'','__VIEWSTATEENCRYPTED':VIEWSTATEENCRYPTED,'__LASTFOCUS':'', '__VIEWSTATE':VIEWSTATE, '__VIEWSTATEGENERATOR':VIEWSTATEGENERATOR, '__EVENTVALIDATION':EVENTVALIDATION} 
		return self.param
	
	def post_data_to_base_url(self):
		post_request = requests.post(self.base_url,data=self.param)
		soup = BeautifulSoup(post_request.content,'lxml')
		# iter = soup.find_all("td",{"class":"chart_detail"})
		iter3 = soup.find_all("div",{"class":"chart_att"})

		for each in iter3:
			heads = each.find_all("td",{"class":"chart_head"})
			data = each.find_all("td",{"class":"chart_detail"})
			for each in heads:
				self.head_list.append(each.get_text().strip('\r\n\t'))
			for each in data:
				self.data_list.append(each.get_text().strip('(*)\n'))
		json_data = json.dumps(dict(zip(self.head_list,self.data_list)))
		print json_data

if __name__ == "__main__":
	x = ASPX__doPostBack('https://www.icsi.in/student/Members/MemberSearch.aspx',16803)
	x.get_base_url()
	x.post_data_to_base_url()