import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_website(url, feature):
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    feature_elements = soup.find_all(feature)

    feature_data = [element.get_text() for element in feature_elements]

    return feature_data

def save_to_excel(data, file_name):
    df = pd.DataFrame({"Scraped Data": data})
    df = df["Scraped Data"].str.split('\n', expand=True).fillna('').stack().reset_index(drop=True)
    df = pd.DataFrame(df, columns=["Scraped Data"])
    df.to_excel(file_name, index=False)
    return file_name

def main():
    st.title("Web Scraping with Streamlit")

    url = st.text_input("Enter the URL of the website to scrape:")

    scrape_option = st.radio("Select scraping option:", ("All data", "Specific content"), index=0)

    if scrape_option == "Specific content":
        # Feature input
        feature = st.text_input("Enter the HTML tag for the specific content you want to scrape (e.g., 'h1', 'p', 'a'):")

    if st.button("Scrape"):
        if url == "":
            st.error("Please enter a URL.")
        elif scrape_option == "Specific content" and feature == "":
            st.error("Please enter a feature HTML tag.")
        else:
            try:
                if scrape_option == "All data":
                    scraped_data = scrape_website(url, "body")  # scraping all data from the entire body
                else:
                    scraped_data = scrape_website(url, feature)

                file_name = "scraped_data.xlsx"
                save_to_excel(scraped_data, file_name)
                st.success(f"Scraped data saved to {file_name}")

                df = pd.read_excel(file_name)
                st.write("Excel Data:")
                st.dataframe(df, width=len(df) * 20)  # Adjust the height as needed
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
