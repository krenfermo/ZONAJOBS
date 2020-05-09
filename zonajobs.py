
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import sys
import math
import time
from datetime import datetime
import cloudscraper
import codecs




   


def my_round(i):
    f = math.floor(i)
    return f if i - f < 0.5 else f+1



def quitar_signos(s):
    replacements = (
        (",", ""),
        ("\"", ""),
         
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

  
def paginas2(soup):
     
    try:
        
        Total_pages = soup.find('div', class_='listado-empleos col-sm-9 col-md-9')
         
        
        Total_pages = Total_pages.find('h1').find('strong').text 
         
        
        
    #Total_pages =driver.find_element_by_xpath("display-flex t-12 t-black--light t-normal").text.split(" ")[0] 
    except:
        #Total_pages =driver.find_element_by_xpath("/html/body/div[7]/div[3]/section[1]/div[2]/div/div/div[1]/div[1]/div[1]/small").text.split(" ")[0]
          
        print('error pagina')
        formato1 = "%Y-%m-%d %H"
        hoy = datetime.today()  

        hoy = hoy.strftime(formato1)  

        path=str(Path().absolute())
        f= codecs.open(path+"\\SCRAPS\\"+str(trabajo)+"_"+hoy+".csv","w+")


        f.write("\"URL\","+"\"NOMBRE\","+"\"DESCRIPCION\","+"\"REQUERIMIENTOS\","+"\"EMPRESA\","+"\"PUBLICADO\","+"\"TIPO CONTRATO\","+"\"JORNADA\"\n")

        f.close()
        exit()
                     
        
        
        
    print(str(Total_pages)+ " resultados")
    Total_pages=int(Total_pages)/25
    #print(Total_pages)
    Total_pages=my_round(Total_pages+0.5)


    return(Total_pages) 





def cuerpo(Total_paginas):
    for pages in range(1,Total_paginas+1) :
             
            print("pagina: "+str(pages))
            URL="https://www.zonajobs.com.ar/buenos-aires/ofertas-de-trabajo-"+str(trabajo)+"-publicacion-menor-a-7-dias-pagina-"+str(pages)+".html"
            print(URL)
            # Get login csrf token
            result = scraper.get(URL, allow_redirects=True)

            #guardo en soup todo el codigo fuente para extraer los valores de la sesion
            soup = BeautifulSoup(result.content, 'html.parser')
            
            
            trabajos=soup.find('div',class_='aviso-no-sponsor')
            
            try:
                homes=trabajos.find_all('div',class_='aviso aviso-home clearfix')
                
            except:
                print("error home")
            try:
                destacados=trabajos.find_all('div',class_='aviso aviso-destacado clearfix')
            except:
                print("error destacados")
            try:
                simples=trabajos.find_all('div',class_='aviso aviso-simple clearfix')
            except:
                print("error simples")
            lista_trabajos=[]
            #print("HOMES:")
            for item in homes:                
                #print(item.find('a')["href"])
                lista_trabajos.append(item.find('a')["href"])
            #print("DESTACATDOS:")    
            for item in destacados:
                #print(item["id"])
                lista_trabajos.append(item["id"])
            
            
            #print("SIMPLES:")    
            for item in simples:
                #print(item["id"])
                lista_trabajos.append(item["id"])
            time.sleep(1)
                
                
               
            
            for item in lista_trabajos:
                time.sleep(1)    
                #print(item)            
                
                navega_cada_pagina_2("https://www.zonajobs.com.ar"+str(item))
                
                
                
                 


def navega_cada_pagina_2(pagina):    
    
    print(pagina)  
    headers = {
"Upgrade-Insecure-Requests":"1",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",


"Sec-Fetch-Dest":"document",
 
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
}


    scraper = cloudscraper.create_scraper()   
    
    result =  scraper.get(pagina, headers=headers)    
    
     
    soup = BeautifulSoup(result.content, 'html.parser')

    
    try:
        nombre = soup.find('h1', class_='aviso_title')
        nombre=nombre.text.lstrip().rstrip()
    except:
        nombre="S/D"
    #print(nombre)
    
    
    
    
    try:
        empresa = soup.find('span', class_='aviso_company')
        empresa=empresa.text.lstrip().rstrip()
    except:
        empresa="S/D"
        
    #print(empresa)
    
    try:    
        descripcion = soup.find('div', class_='aviso_description')
        descripcion=descripcion.text.lstrip().rstrip()
    except:
        descripcion="S/D"
    
    #print(descripcion)
 
    
    
    
    try:       
        datos = soup.find_all('div', class_='col-sm-12 col-md-6 col-lg-10 spec_def')
        #area=area.text
    except:
        
        datos="S/D"
    

    try:    
        lugar_trabajo=datos[0].text.lstrip().rstrip()
        
    except:
        lugar_trabajo="S/D"
    
    
    try: 
        publicado = datos[1].text.lstrip().rstrip()
        
    except:
        publicado="S/D"
        
    try:
        Tipodecontrato=datos[3].text.lstrip().rstrip()
        
    except:
        Tipodecontrato="S/D"
    
    try:
        area=datos[4].text.lstrip().rstrip()
         
    except:
        area="S/D"
    
    
    
     
        
     
    time.sleep(1)
     
    
    
 
    
    
    #print(nombre)
    #print(empresa)
    #print(descripcion) 
    #print(experiencia) 
    #print(jornada)
    #print(publicado) 
    
    f.write("\""+pagina.lstrip().rstrip()+"\",")
    f.write("\""+quitar_signos(nombre)+"\",")
    f.write("\""+quitar_signos(descripcion)+"\",") 
    f.write("\""+quitar_signos(empresa)+"\",")
        
    f.write("\""+quitar_signos(lugar_trabajo)+"\",")
    
    
    f.write("\""+quitar_signos(publicado)+"\",")
    f.write("\""+quitar_signos(Tipodecontrato)+"\",")
    f.write("\""+quitar_signos(area)+"\"\n")
    



trabajo=sys.argv[1].replace(" ","-")


LOGIN_URL="https://www.zonajobs.com.ar/buenos-aires/ofertas-de-trabajo-"+str(trabajo)+"-publicacion-menor-a-7-dias-pagina-1.html"

print(LOGIN_URL)

scraper = cloudscraper.create_scraper() 
# Get login csrf token
result = scraper.get(LOGIN_URL, allow_redirects=True)


#guardo en soup todo el codigo fuente para extraer los valores de la sesion
soup = BeautifulSoup(result.content, 'html.parser')


Total_paginas=paginas2(soup)
print(str(Total_paginas)+" paginas")
    

formato1 = "%Y-%m-%d %H"
hoy = datetime.today()  

hoy = hoy.strftime(formato1)  

path=str(Path().absolute())
f= codecs.open(path+"\\SCRAPS\\"+str(trabajo)+"_"+hoy+".csv","w+")



f.write("\"URL\","+"\"NOMBRE\","+"\"DESCRIPCION\","+"\"EMPRESA\","+"\"LUGAR DE TRABAJO\","+"\"PUBLICADO\","+"\"TIPO CONTRATO\","+"\"AREA\"\n")


cuerpo(Total_paginas)
f.close()