# import webbrowser
import requests
import bs4
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from data_processing import dataProcessing, functionsCommonToAllSites


class indeedScraper:

    #dictionary to saves the job role and job description as key value pair respectively
    jobrole_description_dict={}
    # jd_scraped_count : counts the number of job descriptions scraped
    jd_scraped_count = 0
    # counts the number of duplicate JD's scraped
    duplicate_count = 0
    

    def __init__(self, jd_count, job_role, file_name_to_save, stats_filename,job_place="United States", experience_level="", search_format=""):
        '''
        This is a special Python method that is automatically called when memory is allocated for a new object.

        jd_count : number of job descriptions to scrape
        experience_level : job experience level (Entry Level, Mid Level, Senior Level)
        job_role : job role to scrape like Machine Learning Engineer, Data Scientist, DevOps Engineer, etc
        job_place : Country/City where Job is located
        search_format : search format like : title:(), title:"",""
        file_name_to_save : name of file to save the scraped data
        '''
        self.jd_count = jd_count
        self.experience_level = experience_level
        self.job_role = job_role
        self.job_place = job_place
        self.search_format = search_format
        self.file_name_to_save = file_name_to_save
        self.stats_filename = stats_filename

        #object for data processing class
        self.data_processing = dataProcessing(file_name_to_save = self.file_name_to_save, jd_count = self.jd_count, job_role = self.job_role, stats_filename = self.stats_filename, job_site = "Indeed", experience_level = self.experience_level, job_place = self.job_place, search_format = self.search_format)
        # object for functions common to all sites
        self.common_functions_obj = functionsCommonToAllSites()


    def indeed_get_content(self, url_content_list, indeed_url):
        '''
        This function scrapes job description of all urls received from indeed_scrape() function and save it to jobrole_description_dict

        url_content_list: contains the list of job urls (from indeed_scrape() function)
        job_title : contains the title of scraped job
        job_description : contains the job description
        company_name : contains the company name
        jd_key : contains the key for job description, to save job description in a dictionary
        '''
        for url_content in url_content_list:
            
            if indeedScraper.jd_scraped_count < self.jd_count:
                try:
                    # Title of Job Description
                    job_title = url_content.text.strip()
                    # Request the page
                    res = requests.get(indeed_url + url_content.get('href'))
                    # Check status
                    res.raise_for_status()
                    # Look for Job description text
                    soup = bs4.BeautifulSoup(res.text, features="html.parser")
                    job_description = soup.find('div', class_='jobsearch-jobDescriptionText')
                    if job_description =="":
                        print("job_description not found in url: %s" %(indeed_url + url_content.get('href')))
                        continue
                    # Find company name
                    try: 
                        company_url = soup.find('div', class_="icl-u-lg-mr--sm icl-u-xs-mr--xs")
                        jd_key = job_title+'@'+company_url.text
                        # If Job key is unique
                        # Store Job description into the dictionary
                        if jd_key not in indeedScraper.jobrole_description_dict.keys():
                            indeedScraper.jobrole_description_dict[jd_key] = job_description
                            indeedScraper.jd_scraped_count+=1
                            print(jd_key, indeedScraper.jd_scraped_count)
                        else:
                            print("Cannot save duplicate key:%s" %jd_key)
                            indeedScraper.duplicate_count += 1
                    except Exception as e:
                        print("Warning! Cound not find Company name")
                        print(e) 
                except Exception as e:
                        print('Error: Problem downloading url: %s' %(indeed_url+url_content.get('href')))
                        print(e)

                # Time between 2 requests
                time.sleep(1)
                
            else:
                break


    def indeed_scrape(self):
        '''
        This function scrapes urls of job posts from indeed.com and pass these urls to function indeed_get_content()

        indeed_url : contains url for website to scrape
        job_keyword : contains the job role along with search format
        search_job_elem : contains the reference to element job title for search
        search_place_elem : contains the reference to element job place for search
        url_content_list : contains the urls for all the jobs on a page
        next_element : element to move to next page.
        close_popup : element to close the pop-up appearing on website
        tic : time at which script starts
        download_start_time : It is the time elapsed from opening of selenium browser to starting download of JD's
        '''
        # Site URL
        indeed_url = "https://www.indeed.com"
        #Start timer
        tic = time.perf_counter()
        # Site URL with US Locality
        url = "https://www.indeed.com/stc?_ga=2.97591007.1313838538.1592977347-878814794.1592977347"
        
        # Job keyword according to the input search format
        job_keyword=""
        if self.search_format == 'title:()':
            job_keyword = 'title:('+self.job_role+')'
        elif self.search_format == 'title:""':
            job_keyword = 'title:"'+self.job_role+'"'
        elif self.search_format == '""':
            job_keyword = '"'+self.job_role+'"'
        else:
            job_keyword = self.job_role

        try:
            # Opening Chrome browser
            browser = webdriver.Chrome(ChromeDriverManager().install())
            browser.get(url)
            
            self.common_functions_obj.wait_until_page_load(browser = browser, elem_key='text-input-what', key_type="id", wait_time=60)
            #Enter Job keyword
            search_job_elem = browser.find_element_by_id('text-input-what')
            search_job_elem.send_keys(job_keyword)

            # Enter Place
            search_place_elem = browser.find_element_by_id('text-input-where')
            search_place_elem.send_keys(Keys.CONTROL+'a')
            search_place_elem.send_keys(Keys.DELETE)
            search_place_elem.send_keys(self.job_place)

            # Search
            search_place_elem.send_keys(Keys.ENTER)

            # experience level filter
            if self.experience_level != "":
                self.common_functions_obj.wait_until_page_load(browser = browser, elem_key='filter-experience-level', key_type="id", wait_time=60)
                dropdown = browser.find_element_by_id("filter-experience-level")
                dropdown.click()
                browser.find_element_by_partial_link_text(self.experience_level).click()

            download_start_time = time.perf_counter() - tic
            # to download job roles = jd_count provided
            while indeedScraper.jd_scraped_count < self.jd_count:
                # Wait until job cards are visible or maximum 100 seconds
                self.common_functions_obj.wait_until_page_load(browser = browser, elem_key="//div[@class='jobsearch-SerpJobCard unifiedRow row result clickcard']", key_type="xpath", wait_time=100)
                try:
                    #Finding all job description urls from a page
                    soup = bs4.BeautifulSoup(browser.page_source, features="html.parser")
                    url_content_list = soup.select('div.jobsearch-SerpJobCard.unifiedRow.row.result.clickcard > h2 > a')
                    # Get job description and store in a dictionary
                    self.indeed_get_content(url_content_list, indeed_url)                        
                except Exception as e:
                    print("Error! Couldn't extract URLs!")
                    print(e)
                # Next tab (pagination)
                try:
                    next_element = browser.find_element_by_css_selector("[aria-label=Next]")
                    browser.execute_script("arguments[0].click();", next_element)
                except Exception:
                    try:
                        # Close pop dialog
                        self.common_functions_obj.wait_until_page_load(browser = browser, elem_key="[aria-label=Close]", key_type="css_selector", wait_time=60)
                        close_popup = browser.find_element_by_css_selector("[aria-label=Close]")
                        close_popup.click()
                        self.common_functions_obj.wait_until_page_load(browser = browser, elem_key="[aria-label=Next]", key_type="css_selector", wait_time=100)
                        next_element = browser.find_element_by_css_selector("[aria-label=Next]")
                        browser.execute_script("arguments[0].click();", next_element)
                    except Exception as e:
                        print("Next Element not found")
                        break
                # # #### Save unprocessed data and stats into csv
                self.output_to_file(tic, download_start_time, script_status = "Not Finished")  
            # # #### Save unprocessed data and stats into csv
            self.output_to_file(tic, download_start_time, script_status = "Finished")  
        except Exception as e:
            print(e)
        browser.quit()



    def output_to_file(self, tic, download_start_time, script_status):
        '''
        toc : time at which script ends
        total_runtime : It is the total time for which script runs
        time_per_jd : It is the average time for one job description scraped
        '''
        # # #### Save unprocessed data into csv
        toc = time.perf_counter()
        total_runtime = toc - tic
        time_per_jd = (total_runtime-download_start_time)/float(indeedScraper.jd_scraped_count)
        # Downloaded JD's are passed to below function for processing and saving into csv
        self.data_processing.data_processing(jobrole_description_dict = indeedScraper.jobrole_description_dict, jd_scraped_count= indeedScraper.jd_scraped_count)
        # To save statistics to Stats file
        self.data_processing.log_stats(jd_scraped_count = indeedScraper.jd_scraped_count, total_runtime = total_runtime, time_per_jd = time_per_jd, duplicate_count = indeedScraper.duplicate_count, script_status= script_status)
        indeedScraper.jobrole_description_dict = {}