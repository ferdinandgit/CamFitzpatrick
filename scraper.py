
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import csv


#Color code possibilities 
baseColor=["Y","R"]
fristNumber=[ str(k) for k in range(1,6)]
secondNumber=["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15"]
colorCode=[]

#Color code generation
for i in fristNumber:
    for j in baseColor:
        for k in secondNumber:
            colorCode.append(i+j+k)

#Csv generation parameters 
fields=["Pantone Code","hexacode","red","green","bleu"]
row=[]

for k in colorCode:
    try:
        #Search Resquest on Encycolorpedia for PantoneSkinTone Color guide 
        req = Request(
            url="https://encycolorpedia.fr/search?q="+k, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        
        #Find all url in the website 
        source = urlopen(req).read()
        soup = BeautifulSoup(source,'lxml')
        urllist=soup.find_all('a') 
        string=urllist[len(urllist)-1]
        
        #Exatact and convert HexaColorCode and convert to RGB 
        if k in str(string):
            hexacode=str(string)[10:16]
            red=int(hexacode[0:2],16)
            green=int(hexacode[2:4],16)
            bleu=int(hexacode[4:6],16)
            row.append([k,hexacode,red,green,bleu])
            print(k+" succed")
        else:
            print(k+" no exist")
    except:
        print("Fail"+" "+k)

#Write result in a csv File 

with open('PantoneSkinTone.csv', 'w') as f:
     
    write = csv.writer(f)
     
    write.writerow(fields)
    write.writerows(row)
