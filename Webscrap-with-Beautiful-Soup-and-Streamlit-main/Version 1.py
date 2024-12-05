import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import requests
import base64

def scrape_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a')]
    paragraphs = [paragraph.text.strip() for paragraph in soup.find_all('p')]
    specific_class = [element.text.strip() for element in soup.find_all('div', class_='specific-class')]
    max_length = max(len(links), len(paragraphs), len(specific_class))
    scraped_data = []
    for i in range(max_length):
        data_entry = {
            'Links': links[i] if i < len(links) else None,
            'Paragraphs': paragraphs[i] if i < len(paragraphs) else None,
            'Specific Class': specific_class[i] if i < len(specific_class) else None
        }
        scraped_data.append(data_entry)
    
    return scraped_data
st.title('Web Scraping with Streamlit')
url = st.text_input('Enter the URL to scrape:')

if st.button('Scrape Data'):
    if url:
        try:
            scraped_data = scrape_data(url)
            if scraped_data:
                # Create a DataFrame from the list of dictionaries
                df = pd.DataFrame(scraped_data)
                st.write('Scraped Data:')
                st.write(df)
                
                # Download scraped data as Excel file
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="scraped_data.csv">Download scraped data as CSV file</a>'
                st.markdown(href, unsafe_allow_html=True)
            else:
                st.warning("No data scraped.")
        except Exception as e:
            st.error(f"An error occurred while scraping data: {e}")
    else:
        st.warning("Please enter a URL to scrape.")
