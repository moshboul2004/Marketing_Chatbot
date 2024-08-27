import logging
import streamlit as st
import os
from serpapi import GoogleSearch
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()


def fetch_google_search(query):
    logging.info(f"Fetching Google Trends for query: {query}")

    params = {
        "engine": "google",
        "q": query,
        "api_key": os.getenv('SERPAPI_API_KEY')
    }

    try:
        logging.info("Sending request to SerpAPI with the following parameters:")
        logging.info(params)

        search = GoogleSearch(params)
        results = search.get_dict()

        logging.info("Received response from SerpAPI.")
        logging.debug(f"Full response: {results}")

        organic_results = results.get("organic_results", [])

        if not organic_results:
            logging.warning("No organic results found in the response.")
        
        trends = [result.get("title", "No title available") for result in organic_results]

        if trends:
            logging.info(f"Extracted trends: {trends}")
        else:
            logging.warning("No trends extracted; returning default message.")

        return trends if trends else ["No trends found for this query."]
    
    except Exception as e:
        logging.error(f"Failed to fetch Google Trends: {e}")
        return ["Failed to retrieve trends. Please try again later."]


def fetch_google_trends(query):
    logging.info(f"Fetching Google Trends for query: {query}")

    params = {
        "engine": "google_trends",
        "q": query,
        "data_type": "TIMESERIES",
        "api_key": os.getenv('SERPAPI_API_KEY'),
        "time": "today 12-m"
    }
    try:
        logging.info("Sending request to SerpAPI with the following parameters:")
        logging.info(params)

        search = GoogleSearch(params)
        results = search.get_dict()

        logging.info("Received response from SerpAPI.")
        logging.debug(f"Results: {results}")

        if 'error' in results:
            logging.error(f"Error from Google Trends: {results['error']}")
            return "No trends data available due to an error."

        interest_over_time = results.get("interest_over_time", {}).get("timeline_data", [])

        if not interest_over_time:
            logging.warning("No interest over time data found in the response.")
            return "No trends data available for this query."

        dates = [entry.get('date', 'Unknown date') for entry in interest_over_time]
        values = [entry.get('values', [{}])[0].get('value', 0) for entry in interest_over_time]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, values, marker='o')
        plt.xticks(rotation=45, ha='right')
        plt.title(f"Google Trends for '{query}'")
        plt.xlabel("Date")
        plt.ylabel("Interest over Time")
        plt.grid(True)
        plt.tight_layout()

        plot_file_path = f"./google_trends_{query.replace(' ', '_')}.png"
        plt.savefig(plot_file_path)
        logging.info(f"Plot saved to {plot_file_path}")

        st.pyplot(plt)

        return plot_file_path

    except Exception as e:
        logging.error(f"Failed to fetch Google Trends: {e}")
        return "Failed to retrieve trends. Please try again later."



def spell_check(query):
    logging.info(f"Checking spelling for query: {query}")
    
    params = {
        "q": query,
        "hl": "en",
        "gl": "us",
        "api_key": os.getenv('SERPAPI_API_KEY')
    }
    
    logging.info(f"Sending request to SerpAPI with parameters: {params}")

    search = GoogleSearch(params)
    results = search.get_dict()    
    corrected_query = results.get("search_information", {}).get("spelling_fix", query)
    
    logging.info(f"Corrected query: {corrected_query}")
    
    return corrected_query


def fetch_local_results(query):
    logging.info(f"Fetching local results for query: {query}")
    
    params = {
        "engine": "google_local",
        "q": query,
        "location": "Southampton, England, United Kingdom",
        "api_key": os.getenv('SERPAPI_API_KEY')
    }
    
    logging.info(f"Sending request to SerpAPI for local results with parameters: {params}")
    search = GoogleSearch(params)
    results = search.get_dict()
    
    local_results = [
        {
            "name": result.get("title"),
            "type": result.get("type"),
            "address": result.get("address"),
            "phone_number": result.get("phone"),
            "rating": result.get("rating"),
            "reviews": result.get("reviews"),
            "hours": result.get("hours"),
        }
        for result in results.get("local_results", [])
    ]
    
    logging.info(f"Filtered local search results: {local_results}")
    
    formatted_results = "\n\n".join([
        f"**{res['name']}**\n"
        f"Type: {res['type']}\n"
        f"Address: {res['address']}\n"
        f"Phone: {res['phone_number']}\n"
        f"Rating: {res['rating']} ({res['reviews']} reviews)\n"
        f"Hours: {res['hours']}\n"
        for res in local_results
    ])
    
    logging.info(f"Formatted local search results: {formatted_results}")
    
    return formatted_results