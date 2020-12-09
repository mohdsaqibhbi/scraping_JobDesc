import pandas as pd
import re
import argparse
import os


class scraper:
    
    def __init__(self, jd_count, job_role, file_name_to_save, site_name, job_place="United States", experience_level="", search_format="", stats_filename = "stats"):
        '''
        This is a special Python method that is automatically called when memory is allocated for a new object.

        jd_count : number of job descriptions to scrape
        experience_level : job experience level 
            indeed --> (Entry Level, Mid Level, Senior Level)
            glassdoor --> (Entry Level, Mid Level, Senior Level)
            simplyhired --> none
        job_role : job role to scrape like Machine Learning Engineer, Data Scientist, DevOps Engineer, etc
        job_place : Country/City where Job is located
        file_name_to_save : name of file to save the scraped data
        site_name : name of the website to scrape
        search_format : search format like : title:(), title:"",""
        '''
        self.jd_count = jd_count
        self.experience_level = experience_level
        self.job_role = job_role
        self.job_place = job_place
        self.file_name_to_save = file_name_to_save
        self.site_name = site_name
        self.search_format = search_format
        self.stats_filename = stats_filename

        self.select_site()

    def select_site(self):
        '''
        Function to select the site for scraping.

        indeed_obj : Object of indeedScraper class
        simplyhired_obj : Object of simplyhiredScraper class
        glassdoor_obj : Object of glassdoorScraper class
        temp_jobrole_description_dict : contains a dictionary of scraped data with job role as key and job description as value
        '''

        #create a folder 'data' if it does not exist
        if not os.path.exists('data'):
            os.makedirs('data')
        
        if self.site_name == 'indeed':
            from indeed import indeedScraper
            indeed_obj = indeedScraper(jd_count=self.jd_count, experience_level=self.experience_level, job_role=self.job_role, job_place=self.job_place, search_format = self.search_format, file_name_to_save = self.file_name_to_save, stats_filename = self.stats_filename)
            indeed_obj.indeed_scrape()
        elif self.site_name == 'simplyhired':
            if self.experience_level=="":
                from simplyhired import simplyhiredScraper
                simplyhired_obj = simplyhiredScraper(jd_count=self.jd_count, experience_level=self.experience_level, job_role=self.job_role, job_place=self.job_place, search_format = self.search_format, file_name_to_save = self.file_name_to_save, stats_filename = self.stats_filename)
                simplyhired_obj.simplyhired_scrape()
            else:
                print("Error: Simplyhired has no experience level filter. Please remove experience level filter argument and try to run script again")
        elif self.site_name == "glassdoor":
            from glassdoor import glassdoorScraper
            glassdoor_obj = glassdoorScraper(jd_count=self.jd_count, experience_level=self.experience_level, job_role=self.job_role, job_place=self.job_place, search_format = self.search_format, file_name_to_save = self.file_name_to_save, stats_filename = self.stats_filename)
            glassdoor_obj.glassdoor_scrape()
        else:
            print("Incorrect site name")


# The below code runs only when script is run from auto_scraper.py(as main program file) file.
if __name__=='__main__':
    # Define the parser
    parser = argparse.ArgumentParser(description='Contains Arguments for data scraping which can be passed from Command Line')
    parser.add_argument('-sn', action="store", dest='site_name', choices=['indeed','glassdoor','simplyhired'], required=True)
    parser.add_argument('-jc', action="store", dest='jd_count', type=int, required=True)
    parser.add_argument('-el', action="store", dest='experience_level', choices=['Entry Level', 'Mid Level', 'Senior Level', ''], default="")
    parser.add_argument('-jr', action="store", dest='job_role', required=True)
    parser.add_argument('-jp', action="store", dest='job_place', default="United States")
    parser.add_argument('-fn', action="store", dest='file_name_to_save', required=True)
    parser.add_argument('-sf', action="store", dest='search_format', choices=['title:()', 'title:""', '""', ''], default="")
    parser.add_argument('-sfn', action="store", dest='stats_filename', default="stats")
    # Now, parse the command line arguments and store the 
    # values in the `args` variable
    args = parser.parse_args()

    #create object for class scraper
    scrape_obj = scraper(jd_count=args.jd_count, experience_level=args.experience_level, job_role=args.job_role, job_place=args.job_place, file_name_to_save=args.file_name_to_save, site_name=args.site_name, search_format = args.search_format, stats_filename=args.stats_filename)