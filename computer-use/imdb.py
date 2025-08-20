from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import pandas as pd

def openChrome():
    chromedriver_path = ChromeDriverManager().install()
    print(f"Using ChromeDriver at: {chromedriver_path}")
    try:
        driver = webdriver.Chrome(service=Service(chromedriver_path))
        driver.maximize_window()
        return driver
    except Exception as e:
        print(f"Error starting ChromeDriver: {e}")
        raise

def IMDBfindelement(movie_name):
    url = "https://www.imdb.com/"
    driver.get(url)
    elem = driver.find_element(By.ID, "suggestion-search")# find the search bar
    elem.send_keys(movie_name) # input movie name
    driver.find_element(By.ID, "suggestion-search-button").click()# submit the search query

if __name__ == '__main__':
    
    driver = openChrome()
    df = {'vidlink': [], 'title': [], 'imdb_id': []}
    data = pd.read_csv('video_list.csv')  # Read from csv input file
    # data=pd.read_excel('video_list.xlsx')# Read from Excel input file
    for index, row in data.iterrows():
        vidlink = row['vidlink']
        title = row['title']
        imdb_id = row['imdb_id']
        # print(row) # print input data
        
        if imdb_id!=imdb_id: # check if imdb_id is NaN (null)

            IMDBfindelement(title) # Run the search on the movie title
            print(index+1,'. Movie ',title, ' search results shown in the browser; please select one option to continue:')

            judgement=input("""- Click the correct result and then Press Enter to the next record...
- Type in 'n' (no quote) and Press Enter to the next record if there is no correct result...
- Type in 'exit' and Enter to finish...""")

            if judgement=='exit': # user input is exit, then end the loop and move on to save the collected data
                break
            
            elif judgement=='n': # user input is n, i.e., no matched result
                df['vidlink'].append(vidlink) 
                df['title'].append(title)
                df['imdb_id'].append('no_result')
                print('No correct result:',str(index+1),title)
                
            else: # any other user input, e.g., Enter, extract imdb_id from the current browser URL
                website_url=driver.current_url
                print ('website_url:',website_url)  
                try:
                    imdb_id=(re.findall(r"/(.+?)/",website_url))[1]
                except:
                    imdb_id='error'
                    
                print('imdb_id:',imdb_id)
                df['vidlink'].append(vidlink) 
                df['title'].append(title)
                df['imdb_id'].append(imdb_id)                
                print('Collected:',str(index+1),title,imdb_id)
                
        else: # if the imdb_id already exists in the input file
                df['vidlink'].append(vidlink) 
                df['title'].append(title)
                df['imdb_id'].append(imdb_id)
                print('Already collected:',str(index+1),title,imdb_id)

    print('Saving the file...')

    destinationFileName='video_list_imdb.csv'
    pd.DataFrame(df).to_csv(destinationFileName, index=False)

    print('Successfully Saved')