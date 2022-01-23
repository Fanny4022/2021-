import pandas as pd
import requests
from bs4 import BeautifulSoup

#"縣市"流水號
city = ['63000000000000000', '65000000000000000', '68000000000000000', '66000000000000000', '67000000000000000', '64000000000000000', '10004000000000000', '10005000000000000', '10007000000000000', '10008000000000000', '10009000000000000', '10010000000000000', '10013000000000000', '10002000000000000', '10015000000000000', '10014000000000000', '10016000000000000', '09020000000000000', '09007000000000000', '10017000000000000', '10018000000000000', '10020000000000000']

for i in range(0, len(city)):
    add = 0
    while True: #判斷"區"流水號
        currentPage = int(city[i]) + add
        add += 100000000
        url = 'https://referendum.2021.nat.gov.tw/pc/zh_TW/01/' + str(currentPage) + '.html'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if soup.title.string == '404 Not Found':
            break
        
        else:
            vote_table = pd.read_html(url)

            #上半部的表格
            vote_df = vote_table[2]     #讀取第三個表格
            vote_df.drop(columns = [4, 5, 6], inplace = True)   #刪除欄
            vote_df.columns = vote_df.loc[1]    #把第一列放置到column的位置
            vote_df = vote_df.drop([0, 1, 3, 4, 5, 6])   #刪除列
            vote_df.reset_index(drop = True, inplace = True)    #重新設置選舉表格
            vote_df

            #下半部的表格
            totalvote_df = vote_table[2]
            totalvote_df.columns = totalvote_df.loc[3]
            totalvote_df = totalvote_df.drop([0, 1, 2, 3, 5, 6])
            totalvote_df.reset_index(drop = True, inplace = True)
            totalvote_df

            #所有表格
            allvotes_df=pd.concat([vote_df, totalvote_df], axis = 1)    #合併列
            allvotes_df
            
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'lxml')
            area = soup.select_one('b').text
            area2 = area.split('-', 1)
            allvotes_df['投票地區'] = area2[1]
            
            pd.set_option('display.unicode.ambiguous_as_wide', True)
            pd.set_option('display.unicode.east_asian_width', True) # 設置列名與數據對齊
            pd.set_option('display.width', 100) #設置顯示寬度為100
            print(allvotes_df)
