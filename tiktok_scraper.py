import streamlit as st
import pandas as pd
from apify_client import ApifyClient
import plotly.express as px

# Function to display the sidebar
def show_sidebar():
    st.sidebar.markdown(
        """
        <div style="display: flex; align-items: center;">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" width="40" height="40" style="margin-right: 10px;"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d="M448 209.9a210.1 210.1 0 0 1 -122.8-39.3V349.4A162.6 162.6 0 1 1 185 188.3V278.2a74.6 74.6 0 1 0 52.2 71.2V0l88 0a121.2 121.2 0 0 0 1.9 22.2h0A122.2 122.2 0 0 0 381 102.4a121.4 121.4 0 0 0 67 20.1z"/></svg>
            <h1 style="margin: 0;">TikTok Hashtag Scraper</h1>
        </div>
        <br>
        Welcome to the TikTok Hashtag Scraper app! Enter TikTok hashtags (comma-separated),
        specify the results per page, and choose the download options. Click the "Scrape" button
        to get started. You can download the scraped data in CSV and/or JSON format.
        """
        , unsafe_allow_html=True
    )
    st.sidebar.markdown("### How to use:")
    st.sidebar.markdown(
        """
        1. Enter TikTok hashtags in the input box.
        2. Adjust the "Results Per Page" slider.
        3. Check the options for CSV and/or JSON download.
        4. Click the "Scrape" button to retrieve and display the data.
        """
    )

# Function to create histogram for a given column
def create_histogram(df, column_name):
    fig = px.histogram(df, x=column_name, nbins=30, title=f'Distribution of {column_name}')
    st.plotly_chart(fig)

# Function to create scatter plot for 'shareCount' vs. 'commentCount'
def create_scatter_plot(df):
    fig = px.scatter(df, x='shareCount', y='commentCount', title='Scatter Plot of Share Count vs. Comment Count')
    st.plotly_chart(fig)

# Function to create bar chart for 'playCount'
def create_bar_chart(df):
    fig = px.bar(df, x=df.index, y='playCount', title='Bar Chart of Play Count')
    st.plotly_chart(fig)

# Function to create pie chart for 'collectCount'
def create_pie_chart(df):
    fig = px.pie(df, values='collectCount', names=df.index, title='Pie Chart of Collect Count')
    st.plotly_chart(fig)

# Function to create another histogram for 'commentCount'
def create_another_histogram(df):
    fig = px.histogram(df, x='commentCount', nbins=30, title='Distribution of Comment Count')
    st.plotly_chart(fig)

# Streamlit UI
def main():
    show_sidebar()

    # Input for hashtags and other parameters
    hashtags = st.text_input("Enter TikTok Hashtags (comma-separated):")
    results_per_page = st.number_input("Results Per Page", min_value=1, max_value=100, value=20)
    
    # Checkboxes for download options
    download_csv = st.checkbox("Download CSV")
    download_json = st.checkbox("Download JSON")

    if st.button("Scrape"):
        if hashtags:
            st.info("Scraping...")
            hashtag_list = [hashtag.strip() for hashtag in hashtags.split(",")]
            scraped_data = scrape_tiktok_hashtags(hashtag_list, results_per_page)
            st.success(f"Scraped data for {len(scraped_data)} posts")

            # Convert the scraped data to a Pandas DataFrame
            df = pd.DataFrame(scraped_data)

            # Display the DataFrame
            st.write("Scraped Data:")
            st.dataframe(df)

            # Save the DataFrame to a CSV file if selected
            if download_csv:
                df.to_csv("scraped_data.csv", index=False)
                st.success("Data saved to 'scraped_data.csv'")

            # Save the DataFrame to a JSON file if selected
            if download_json:
                json_data = df.to_json(orient="records")
                with open("scraped_data.json", "w") as json_file:
                    json_file.write(json_data)
                st.success("Data saved to 'scraped_data.json'")

            # Plotly Visualizations
            create_histogram(df, 'diggCount')
            create_scatter_plot(df)
            create_bar_chart(df)
            create_pie_chart(df)
            create_another_histogram(df)

        else:
            st.warning("Please enter TikTok hashtags.")

# Function to call Apify TikTok Scraper Actor
def scrape_tiktok_hashtags(hashtags, results_per_page):
    # Initialize the ApifyClient with your API token
    client = ApifyClient("apify_api_Sd42jiNxLabuE6fHCdQb1ki5OJfBxN3hRf56")

    # Prepare the Actor input
    run_input = {
        "hashtags": hashtags,
        "resultsPerPage": results_per_page,
        "shouldDownloadVideos": False,
        "shouldDownloadCovers": False,
        "shouldDownloadSlideshowImages": False,
    }

    # Run the Actor and wait for it to finish
    run = client.actor("OtzYfK1ndEGdwWFKQ").call(run_input=run_input)

    # Fetch and return Actor results from the run's dataset (if there are any)
    scraped_data = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        scraped_data.append(item)

    return scraped_data

if __name__ == "__main__":
    main()
