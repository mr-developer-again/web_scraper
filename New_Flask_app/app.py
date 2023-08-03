# this app run a web_interface application for getting the title
import os 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from flask import Flask , render_template , request , url_for , redirect

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html')
    
@app.route('/title')
def get_title():
    title = request.args.get("send_title")
####################################################
                    ## get titles ## EveryThing is ok
    # given_title = os.getenv("TITLE")
    years = ['2018' , '2019' , '2020' , '2021' , '2022' , '2023']
    driver = webdriver.Chrome()
    for index in years:
        driver.get(f"https://medium.com/tag/{title}/archive/{index}")
        main = driver.find_element(By.TAG_NAME, "body")

        articles = main.find_elements(By.CLASS_NAME, "streamItem--postPreview")

        for article in articles:
            titles = article.find_element(By.TAG_NAME, "h3")
            print(titles.text)
            link = article.find_elements(By.TAG_NAME, 'a')[3]
            link_url = link.get_attribute("href")  
            with open("../New_links.text" , 'a') as file :
                file.write(f"{titles.text}==={link_url}\n")
            
    return redirect(url_for('ok'))
            

@app.route('/waitngpage')
def wait():
    return render_template("wating.html")

@app.route('/ok')
def ok():
    return render_template("ok.html")

@app.route('/crateing_articles')
def creaing_files():
    driver = webdriver.Chrome()
    input()
    with open('../New_links.text' , 'r') as file:
        all_text = file.readlines()
        for text in all_text:
            val = text.split("===")    
                
            url = val[1]
            file_name = val[0]
            driver.get(url)

            # Find the element and get its text content
            element = driver.find_element(By.TAG_NAME , "article")
            text = element.text
            with open(f'../articles/{file_name}.txt' , 'a') as f :
                f.write(text)
    return render_template("tick.html")




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)