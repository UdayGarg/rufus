# demo.py
from rufus import RufusClient
import os

if "__main__" == __name__:
    client = RufusClient()

    # Define your scraping instructions
    instructions = "Find information about different programs and admission FAQs."
    output_filename = "test2.json"

    # Start scraping
    documents = client.scrape("https://www.bu.edu/cs/masters/program/", instructions=instructions, output_filename=output_filename)


    print(f"Scraping completed. Documents saved to '{output_filename}'.")