import pandas as pd
import re
import time

class dataProcessing:

    def __init__(self, file_name_to_save, job_role, stats_filename, job_site, jd_count, experience_level, job_place, search_format):
        '''
        This is a special Python method that is automatically called when memory is allocated for a new object.

        file_name_to_save : name of file to save the scraped data
        jobrole_description_dict : dictionary containing scraped unprocessed data
        jd_scraped_count : No. of job descriptions scraped
        job_role : Job Role for which data is being scraped
        total_runtime : total time in seconds took by script to scrap data and process it
        time_per_jd : average time taken to scrape one Job Description
        duplicate_count : The number of duplicate Job Descriptions found
        stats_filename : name of the file which stores statistics of script
        job_site : name of the site from which scraping is done
        jd_count : Job Descriptions required
        '''

        self.file_name_to_save = file_name_to_save
        self.jd_count = jd_count
        self.job_role = job_role
        self.stats_filename = stats_filename
        self.job_site = job_site
        self.experience_level = experience_level
        self.job_place = job_place
        self.search_format = search_format
        self.time_stamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.time_stamp_filename = time.strftime("%Y%m%d_%H%M%S")



    def data_processing(self, jobrole_description_dict, jd_scraped_count):
        '''
        This function creates a csv file of scraped data after doing data processing.

        jobrole_description_dict : contains dictionary temp_jobrole_description_dict passed as argument in select_site() function
        jdd_key : contains key from dictionary jobrole_description_dict
        '''
        
        if len(jobrole_description_dict)>0:
            # #### Data processing
            print("Doing Data Processing.....")   
            for jdd_key in jobrole_description_dict.keys():
                #### converts job description from type - bs4.element.ResultSet to string
                str_content = str(jobrole_description_dict[jdd_key])
                #### to place full stop at end of JD
                if str_content[-1]=="]":  # for simplyhired
                    temp_str_content = str_content[:-1]
                    temp_str_content+=".]"
                    str_content=temp_str_content
                else:
                    str_content+="."    # for Indeed

                # to replace all closing p, div,li, ul, br with '. ''
                str_content = re.sub('<br/>', '. ', re.sub('<br />', '. ', re.sub('<br>', '. ', re.sub('</ul>', '. ', re.sub('</li>', '. ', re.sub('</div>', '. ', re.sub('</p>', '. ', str_content)))))))
                
                #### regex to convert any closing and opening tag to '', new line 
                # character to '. ', id="" to space
                str_content = re.sub(r'[i][d][=]["][^"]*["]',' ', re.sub(r'[\n]','. ', re.sub(r'[<][^>]*[>]','', str_content)))
                # replaces ascii codes &lt;, &gt;, &apos;, &quot;, &amp; with character
                str_content = re.sub('&lt;', '<', re.sub('&gt;', '>', re.sub('&apos;', "'", re.sub('&quot;', '"', re.sub('&amp;', '&', str_content)))))
                # regex to convert remaining ascii codes to blank
                if re.findall('[&][^;| ]*[;]', str_content):
                    str_content = re.sub('[&][^;| ]*[;]', '', str_content)
                    print("could not replace few ascii codes and are deleted")
                #### regex to convert two full stops with any number of spaces b/w them to single full stop
                while re.findall(r'[.][\ ]*[.]', str_content):
                    str_content = re.sub(r'[.][\ ]*[.]','.', str_content) 
                #### regex to convert '!.' with any number of spaces b/w them to '!'
                while re.findall(r'[!][\ ]*[\.]', str_content):
                    str_content = re.sub(r'[!][\ ]*[\.]','!', str_content)
                #### regex to convert ':.' with any number of spaces b/w them to ':'
                while re.findall(r'[:][\ ]*[\.]', str_content):
                    str_content = re.sub(r'[:][\ ]*[\.]',':', str_content)
                #### regex to convert '?.' with any number of spaces b/w them to '?'
                while re.findall(r'[\?][\ ]*[\.]', str_content):
                    str_content = re.sub(r'[\?][\ ]*[\.]','?', str_content)
                #### regex to convert '-.' with any number of spaces b/w them to '-'
                while re.findall(r'[-][\ ]*[\.]', str_content):
                    str_content = re.sub(r'[-][\ ]*[\.]','-', str_content)
                # to convert '.).' to ').' and '·' to blank
                str_content = re.sub('·','', re.sub(".\).",").", str_content))
                #### regex to convert any number of spaces to single space
                while re.findall(r'[\ ][\ ]*[\ ]', str_content):
                    str_content = re.sub(r'[\ ][\ ]*[\ ]',' ', str_content)
                #save processed data to dictionary
                jobrole_description_dict[jdd_key]=str_content
            # #### Save processed data into csv
            jd_file_name = "data/%s_%s.csv" %(self.file_name_to_save, self.time_stamp_filename)
            try:
                pd.DataFrame.from_dict(data=jobrole_description_dict, orient='index').to_csv(jd_file_name, header=False, mode='a')
                print("Saved Job Descriptions to: %s_%s.csv" %(self.file_name_to_save, self.time_stamp_filename))
                print("Number of Job Description's scraped: %i" %(jd_scraped_count))
            except Exception as e:
                print(e)
                print("Error writing file for Job Description")
            


    def log_stats(self, jd_scraped_count, total_runtime, time_per_jd, duplicate_count, script_status):
        '''
        This function creates a file stats.csv and appends statistics of script in it.
        stats_file : Object of the stats file
        total_runtime : Total time for which script runs
        time_per_jd : Average Time taken to download single JD
        '''

        try:
            stats_file_name = "%s_%s.csv" %(self.stats_filename, self.time_stamp_filename)
            stats_file_location = "data/%s" %(stats_file_name)
            stats_file = open(stats_file_location,'w+')
            stats_file.write("Start Time, Job site, Job Role, Job Place, Experience Level, Search Format, JD Requested, JD Scraped, Total Runtime(in seconds), Time per Job Description(in seconds), Duplicate Count, Stats File, Status\n")
            #jsc = '%.3f'%jd_scraped_count
            total_runtime = '%.3f'%total_runtime
            time_per_jd = '%.3f'%time_per_jd
            stats_file.write(self.time_stamp+","+self.job_site+","+self.job_role+","+self.job_place+","+self.experience_level+","+self.search_format+","+str(self.jd_count)+","+str(jd_scraped_count)+","+total_runtime+","+time_per_jd+","+str(duplicate_count)+","+stats_file_name+","+script_status+"\n")
            stats_file.close()
            if script_status == "Not Finished":
                print("Total Runtime(in seconds): %s\nTime per JD(in seconds): %s\nNumber of Duplicates: %d" %(total_runtime, time_per_jd, duplicate_count))
                print("Saved Scraping Stats to: %s_%s.csv" %(self.stats_filename, self.time_stamp_filename))
        except Exception as e:
            print(e)
            print("Unable to update %s_%s.csv file" %(self.stats_filename, self.time_stamp_filename))


class functionsCommonToAllSites():
    def __init__(self):
        pass


    # wait for page to load or 60 seconds max
    def wait_until_page_load(self, browser, elem_key, key_type, wait_time):
        '''
        This function waits until a specific element from page loads or at the max waits for the wait time passed in argument

        sleep_count : controls the number of time sleep function is to be called
        browser : contains the instance of webdriver.Chrome to select an element
        elem_key : contains the selector element
        key_type : contains the selector element type like xpath, css-selector, etc
        wait_time: contains the time for which program searches for a particular element on page
        '''
        sleep_count=0
        while True:
            try:
                if key_type=="id":
                    browser.find_element_by_id(elem_key)
                elif key_type == "class":
                    browser.find_element_by_class(elem_key)
                elif key_type == "xpath":
                    browser.find_element_by_xpath(elem_key)
                elif key_type == "css_selector":
                    browser.find_element_by_css_selector(elem_key)
                elif key_type=="link_text":
                    browser.find_element_by_link_text(elem_key)
                break
            except:
                time.sleep(1)
                sleep_count+=1
                if(sleep_count==wait_time):
                    print("could not load page with %s %s" %(key_type, elem_key))
                    break
                print("Waiting for page with %s %s to load" %(key_type, elem_key))