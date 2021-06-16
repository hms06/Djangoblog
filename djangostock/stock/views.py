from django.shortcuts import render
import requests
import json
import xmltodict


def stock(request):
	api_requests = requests.get('https://cloud.iexapis.com/stable/stock/aapl/book?token=pk_a31babcc00cc4f05a6f8bd3258d7180c')
	krx_api_requests = requests.get('http://asp1.krx.co.kr/servlet/krx.asp.XMLSise?code=035420').content.strip()
	try :
		api = json.loads(api_requests.content)
		krx_api_to_str =  json.dumps(xmltodict.parse(krx_api_requests))
		krx_api_to_str = krx_api_to_str.replace('@','')
		krx_api = json.loads(krx_api_to_str)
	except Exception as e:
		api = "error"

	return render(request, 'stock.html', {'stock_info' : api['quote'], 'krx_info' : krx_api['stockprice']['TBL_StockInfo'] })

def home(request):
	return render(request, 'home.html', {})