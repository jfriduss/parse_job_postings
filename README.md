# Mining skills from job descriptions for a data driven learning path



## The question:

​	Many people study subjects, such as physics, that teach the foundational skills for many jobs, but whose training is less specific to a particular career, compared to majors like engineering or computer science. This project provides tools for people in this situation to understand how suited they are for different career paths, and determine the specific skills within their expertise that are most sought after.



*possibly put a figure here that demonstrates the need for this type of thing*



## The solution:

### The job_analytics_tools module:

#### Overview: 

​	Using [data](documentation/data_format_README.ipynb) scraped from a major job search engine, [two transformer models](documentation/ML_models_README.ipynb) were fine tuned to create a pipeline that extracts entities in job descriptions that are useful for understanding whether an individual is a good fit for the job. The training data for the models was labelled according to these [annotation guidelines](documentation/annotation_guidelines.md), using the following [labeling tools](documentation/labeling_tools_README.ipynb) that were created to expedite the labeling process. 

#### Functionality and sample outputs:

Within the [job analytics tools module](career_fit_tools/job_analytics_tools.py), the 

- a function, **get_if_qualified_indicators** that takes a job description, as a string, and outputs a list of entities that are useful for understanding whether an individual is a good fit for the job. Below is an image of the job description, with the entities that have been extracted, in color.
  - *insert image here*



#### Benchmarking the models: 

*describe the different ways that benchmarking it, both against itself (e.g. when using the sentence classifier ahead of the token classifier, versus not doing this), and also against things that other people have made (e.g. the solution that working from. Also, maybe benchmark against BERT fine tuned straight from my data, without starting from jobBERT)*



#### Running the project: 

*create instructions to set up and run the project here*, *include link to the general documentation markdown file here, if not more natural to place it elsewhere*

 



*where/how to integrate discussion of how might improve what has currently been made, in the future, as well as making additional features.* *Also, maybe have a section with visualization that take advantage of the tools* 









