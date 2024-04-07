# 说明
此处用于存放上次实验中使用过的代码。





# gender-discrimination-hiring

This repo contains codes for obtaining the necessary data for the following paper:

#### *Li K.*, *L. Li*, *W. Si* and *Z. Xu* (2022) "**Childbearing Age and Gender Discrimination in Hiring Decisions: A Large-scale Field Experiment**" 

Please find the paper [here](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4199754).

To make sense of the explanations below, you may want to check the experimental design part of the paper first.


## `gender51job`

The `gender51job` folder contains a Scrapy web-crawling framework.

- It is used to obtain all the relevant positions (and position info such as company size, company type etc.) from [51job.com](https://www.51job.com/)
- Change the `url` variable in `gender-discrimination-hiring/gender51job/spiders/job.py` for different occupations (IT, Accounting or HR)
- The output would be a `json` file like `result_sample.json`. 

## `randomization_1to1.py`

`randomization_1to1.py` takes the `result.json` file obtained using `gender51job` and does the following:

- Data cleaning includes but not restricts to:
  - Exclude positions not in our research scope, such as positions requiring a doctor's degree or paying over a certain amount, etc.
  - Convert different salary measures to monthly salaries
  - Give company size levels, salary levels and other levels different labels
- Randomly divide the positions into blocks for each fictitious applicant
- The output would be a `xlsx` file like `output_sample.xlsx` 

## `autoapply.py`

After getting the list of positions (for instance, `output_sample.xlsx`) that a fictitious applicant needs to apply, one can of course do it manually. However, as we send out applications for more than 30,000 positions, we use `ChromeDriver` to automate the process. 

`ChromeDriver` is an open-source tool for automated testing of webapps. Information on installation and usage of the `ChromeDriver` can be found [here](https://chromedriver.chromium.org/).

`autoapply.py` loops through every item in `output_sample.xlsx` and automatically sends out the applications one by one, and it outputs a `csv` file with all the positions that have been successfully applied. Therefore, we can check if all submissions are successful, and if the program fails to submit for some positions, we can do it manually.

## `51job.py`

A paid 51job account provides more detailed information on a certain position. For instance, the "competition level" measured by how many people had applied for this position in the past month only shows in a paid mode.

To use `51job.py`, firstly login into the paid account, then get the "cookies" from the "dev tools" of your browser and set the `cookies` variable in the program. 
