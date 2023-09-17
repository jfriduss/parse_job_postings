# Mining skills from job descriptions for a data driven learning path



## Motivation:

Many people study subjects, such as physics, that teach the foundational skills for many jobs, but whose training is less specific to a particular career, compared to majors like engineering or computer science. This project provides tools for people in this situation to understand how suited they are for different career paths, and determine the specific skills within their expertise that are most sought after.



## A solution:

### The job_analytics_tools module:

#### Overview: 

Using [data](documentation/data_format_README.ipynb) scraped from a major job search engine, [two transformer models](documentation/ML_models_README.ipynb) were fine tuned to create a pipeline that extracts entities in job descriptions that are useful for understanding whether an individual is a good fit for the job. The training data for the models was labelled according to these [annotation guidelines](documentation/annotation_guidelines.md), using [labeling tools](documentation/labeling_tools_README.md) that were created to expedite the labeling process. 



#### Functionality and sample outputs:

Within the [job analytics tools module](career_fit_tools/job_analytics_tools.py), the 

- a function, **get_if_qualified_indicators** that takes a job description, as a string, and outputs a list of entities that are useful for understanding whether an individual is a good fit for the job. Below is a portion of an image of a sample job description, with the entities that have been extracted, in color. Refer to this [notebook](career_fit_tools/job_analytics_tools_sample_outputs.ipynb) for more information.

  

  ![sample output](career_fit_tools\examples\pictures\sample_output_get_if_qualified_indicators.png)



- in progress: a tool that takes entities drawn from numerous job descriptions, and reduces the entity space in a systematic way, so that analytics can be done to draw meaningful conclusions.

  

#### Running the project: 

- create a .env file with [this](format_of_env_file.txt) format
- run "conda create --name *environment_name* --file packages.txt" to create an environment with the necessary packages 
- follow the instructions provided in this [notebook](career_fit_tools/job_analytics_tools_sample_outputs.ipynb) to initiate your exploration of the compatibility between your skillset and various career paths!

 









