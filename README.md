# Scraping Automation

Scrape job descriptions from the site Indeed.com (more can be added later).

## Description

The auto_scraper.py script scrapes job posts from the website using a search query and various filters. You can execute the program by running it in the command line with the appropriate flags or by passing arguments to the object of scraper class.

### Important Files

* auto_scraper.py : It is main script file which imports indeed script as required, scraps job descriptions.
* indeed.py : This file contain functions to scrap indeed.com.
* data_processing.py : This file contains functions for data processing and saving file.

### Cloning the project:
```
git clone https://gitlab.com/careermap/scraping/scraping_automation.git
```

### Setting up the Virtual Environment
* For Windows:
   * Install
   ```
   pip install virtualenv
   python -m venv auto-scraping-env
   ```
   * Activate
   ```
   auto-scraping-env\Scripts\activate
   ```
* For Unix or MacOS:
   * Install
   ```
   pip install virtualenv
   python -m venv auto-scraping-env
   ```
   * Activate
   ```
   source auto-scraping-env/bin/activate
   ```

### Dependencies

After setting up your virtual environment, download the dependencies with `pip install -r requirements.txt`

### Executing program

To run the program type 'python auto_scraper.py' followed by the tag value pair for each parameter you want to set.

| tag (* = required)| variable          | options                                        | default value   |
|:-----------------:|:------------------|:-----------------------------------------------|:----------------|
| -sn *             | site_name         | choices=[indeed]                               | REQUIRED        |
| -jc *             | jd_count          | No. of JD's requried (type=int)                | REQUIRED        |
| -el               | experience_level  | choices=["Entry Level", "Mid Level", "Senior Level", ""] | ""              |
| -jr *             | job_role          | name of job role you'd like to scrape          | REQUIRED        |
| -jp               | job_place         | any goegraphic location                        | "United States" |
| -fn *             | file_name_to_save | name of file to save                           | REQUIRED        |
| -sf               | search_format     | choices=["title:()", "title:\\""\\""", "\\""\\""", ""]                | ""              |
| -sfn               | stats_filename   | name of file to save scraping stats             | "stats"         |

* Command Line exmaple:
   * Type command:
   ```
   python auto_scraper.py -sn "indeed" -jc 10 -el "Entry Level" -jr "Machine Learning Engineer" -jp "United States" -fn "machine_learning_engineer_indeed" -sf "title:()"
   ```
* Function call example:
   * Type the command:
   ```
   from auto_scraper import scraper
   ```
   ```
   scrape_object = scraper(site_name = "indeed", jd_count = 10, experience_level= "Entry Level", job_role = "Machine Learning Engineer", job_place = "United States", file_name_to_save = "machine_learning_engineer_indeed", search_format = "title:()")
   ```

### Data Processing

* The data processing of the downloaded JD's include the below points:
	* place full stop at end of JD(last line of JD)
	* replace all closing p, div,li, ul, br with '. ''
	* convert any closing and opening tag to blank(), new line character to '. ', id="" to space(found in text of glassdoor)
	* replaces ascii codes &lt;, &gt;, &apos;, &quot;, &amp; with their respective character
	* convert remaining ascii codes to blank()
	* convert two or more full stops with any number of spaces b/w them to single full stop
	* convert '!.' with any number of spaces b/w them to '!'
	* convert ':.' with any number of spaces b/w them to ':'
	* convert any number of spaces to single space
	* convert '?.' with any number of spaces b/w them to '?'
	* convert '-.' with any number of spaces b/w them to '-'
	* convert '.).' to ').' and '·' (bullet point) to blank

### Note

* In file name argument -fn file name should contain only name of file excluding extension. Extension of the file will always be .csv.
* The output data will be saved in a file with name provided in file name argument. The file will be saved inside folder 'data'.
* The experience level filter argument must not be used for Simplyhired as it will result in error message, as simplyhired does not contain experience filters.
* Stats file is a csv file that stores jd count, total runtime, time per job, and number of duplicate posts found with the time and date alongside the job title
