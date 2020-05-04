import requests
from lxml import etree
import pandas as pd
import datetime
import requests
from lxml import etree
import pdfkit

href1_list =[]
Audilist = []
pricelist = []
Audipricelist = []

def appendlist( hrefx ): # 資料清洗，把型號跟價格分別裝成list
	if hrefx != []:	
			for i in range( len( hrefx ) ):
				if 'Audi' in hrefx[i] and hrefx[i][0] != 'A': # 有些車款資料，前面有多5個字元，有些前面多6個
					Audilist.append( hrefx[i][6:] )
				if 'Audi' in hrefx[i] and hrefx[i][0] == 'A': # 多5個字元
					Audilist.append( hrefx[i][5:] )
				if 'NT' in hrefx[i]: # 價格
					pricelist.append( hrefx[i][3:] )
	
headers = { "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15" } # 用自身瀏覽器的網頁代理，假裝不是爬蟲
response = requests.get( 'http://www.audi.com.tw/tw/web/zh.html?ds_rl=1256997&ds_rl=1257015&ds_rl=1253959&ds_rl=1253959&ds_rl=1257015', headers = headers ) # 取得網址，reponse為200代表取得成功
content = response.content.decode() # 單純印出content為unicode的形式，因此用decode解碼，()內沒輸入時預設為utf-8
html = etree.HTML( content ) # 使用 xpath 選擇器來擷取數據
for i in range(1,14,1): # 不同車款
	for j in range(1,6,1): # 不同型號
		href = html.xpath('/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/ul/li/a/@href') # 取得各類車型的網址
for i in range( len( href) - 1 ):
		response1 = requests.get( 'http://www.audi.com.tw' + href[i][0:-5] + '/price.html', headers = headers ) # 建議售價的網址
		content1 = response1.content.decode() # 解碼
		html1 = etree.HTML( content1 ) # 4種xpath的呈現方式
		href1 = html1.xpath( '/html/body/div[1]/div[2]/div/div[7]/div[2]/div/div[2]/table/tbody/tr//text()')
		href2 = html1.xpath( '/html/body/div[1]/div[2]/div/div[7]/div[2]/div[2]/table/tbody/tr//text()')
		href3 = html1.xpath( '/html/body/div[1]/div[2]/div/div[6]/div[2]/div[2]/table/tbody/tr//text()' )
		href4 = html1.xpath( '/html/body/div[1]/div[2]/div/div[7]/div[2]/div/div[3]/table/tbody/tr//text()')
		appendlist( href1 )
		appendlist( href2 )			
		appendlist( href3 )
		appendlist( href4 )
for i in range( len(Audilist) ):
	Audilist[i] = Audilist[i].replace(u'\xa0', u' ') # 清洗資料中無用的資訊
	Audipricelist.append( (Audilist[i].strip(), pricelist[i].strip()) ) # 新車網站所有車款的型號與原價

href_list =[]
information_list =[]
headers = { "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15" } # 用自身瀏覽器的網頁代理，假裝不是爬蟲
for i in range( 1, 12, 1 ): # 1到11頁
	response = requests.get( 'http://approvedplus.audi.com.tw/?lm=r&p='+str(i), headers = headers ) # 取得網址，reponse為200代表取得成功
	content = response.content.decode() # 單純印出content為unicode的形式，因此用decode解碼，()內沒輸入時預設為utf-8
	html = etree.HTML( content ) # 使用 xpath 選擇器來擷取數據
	href = html.xpath('//*[@id="srch-results"]/div/div[1]/div/div/div[2]/div/h3/a/@href') # 辦認每台車的網址
	for j in range(12): 
		try: # 每頁至多12筆資料，用try才不會 runtime error
			if href[j] not in href_list:
				href_list.append( href[j] )
		except:
			pass
# 目前已取得126台中古車的網址（此數字會不斷變動）

for i in href_list: # 透過中古車型號，配對車相同車款的原價
	response = requests.get( 'http://approvedplus.audi.com.tw'+str(i), headers = headers ) # 取得網址，reponse為200代表取得成功
	content = response.content.decode() # 單純印出content為unicode的形式，因此用decode解碼，()內沒輸入時預設為utf-8
	html = etree.HTML( content ) # 使用 xpath 選擇器來擷取數據
	model = html.xpath('/html/body/div[1]/div[2]/section[2]/div/h1/text()') # 型號
	original_price = 'None' # 初始設定
	for j in range( len(Audipricelist) ):
		if model[0] == Audipricelist[j][0]: # 若車款相同
			original_price = Audipricelist[j][1].strip() # 找到原價
	years = html.xpath('/html/body/div[1]/div[2]/section[2]/div/div[2]/div[1]/ul/li[1]/span[2]/text()') # 年份
	year = years[0][0:4] # 年份
	month = years[0][5:] # 月份
	date = datetime.datetime(int(year),int(month),1,0,0,0) # 日期
	today = datetime.datetime(2019,1,1,0,0,0) # 現在的年份與月份
	days = today - date # 已掛牌幾天
	days = days.days # 轉換格式
	secondhand_price = html.xpath('/html/body/div[1]/div[2]/section[2]/div/div[2]/div[1]/ul/li[2]/span[2]/text()') # 價格
	secondhand_price[0] = float( secondhand_price[0].strip()[0:-2] ) * 10000 # 網站以中文字萬元計價，在此將其轉換為數字
	mileage = html.xpath('/html/body/div[1]/div[2]/section[2]/div/div[2]/div[1]/ul/li[10]/span[2]/text()') # 里程
	if mileage[0].strip() == '<500': # 若里程數低於500，不會顯示實際里程數
		mileage[0] = '250' # 假設為250
	if original_price != "None": # 有配對到資料才能跑迴歸（新車與中古車網站上有部分車款資訊詳細程度不一，無法確認為相同車款，因此不予配對）
		information = [model[0],days, mileage[0].strip(), secondhand_price[0], original_price.strip()] # 標題依序為 車款、車齡、里程數、二手價、原價
		information_list.append(information) 

column_name = ['Model', 'Days', 'Mileage(km)', 'Secondhand Price(NT$)', 'Original Price(NT$)']
test = pd.DataFrame(columns = column_name, data = information_list) # 轉換為矩陣形式
test.to_csv('/Users/lijicheng/Downloads/履歷表/奧迪福斯資料分析/result.csv', encoding = 'utf_8_sig') # 存成csv檔，輸出結果會有千分位，要用excel解決


