## Mining skills from job descriptions for a data driven learning path



This project is an attempt to:

	- create a tool that can be used to extract skills/qualifications required for career paths
	- gain familiarity with packages/techniques useful in machine learning/data analytics 



The project as a whole consists of three parts:

- a program that gets information from job postings on the internet, built on top of Selenium
- a table on a MySQL Community Server that holds information on each job
- a pipeline of HuggingFace Transformer NLP models that are used to extract words and phrases indicating useful skills, from the ads.
  - in order to quantitatively evaluate the pipeline, annotation guidelines were created that remove ambiguity as to what the pipeline should/should not extract

*Only the item in the third bullet point, the files involved in extracting skills from the already-scraped job postings, are included in this repo.* The other two components are not included because the "scrape information from job postings" bot  could be used towards illegal ends, and the information from the database that is used in the project is also stored in the json file, [put name here], that is in the repo.



About the skill extracting pipeline:

The skills extracting pipeline takes a string containing a job posting, and outputs the posting with the skills highlighted. The constituents of the pipeline are:

- a function that partitions the string into sentences
  - the function relies on that the job posting uses common syntactical conventions, and detects when the posting does not. If the posting does not use the common syntactical conventions, the pipeline asks the user to manually partition the string. See [put notebook name here] for a discussion of the choices made at this step.
- a transformer model that [info about the sentence classification model]
- a transformer model that [info about the token classification model]



About training the models used in the skill extracting pipeline:

- the json file [put name of file here] contains a list, with each element of the list being a dictionary with the information about a given ad required to train the models. The dictionary has the following keys:
  - job_id: the value of this key is an integer that corresponds to the primary key of the job posting in the table that the job postings are stored, in the database on the MySQL Community Server
  - sentences: the value of this key is a list of strings, each corresponding to a sentence in the job posting
  - helpers:  the value of this key is a string, that provides a way to reconstruct the ad from the list of sentences. It has information about on what characters (e.g. newlines, periods, etc.) the "partition string function" used to break the paragraph into sentences. Using the function [put function name here], that takes the list of sentences and the 'helpers' string, the ad can be reconstructed.
  - labels: the value of this key is a list that is the same length as the list that the "sentences" key references. It contains labels both to classify each sentence as a whole according to whether or not it contains tokens to be annotated, as well as labels for token classification of the individual tokens (words) in each sentence. To contain both labels, each element in the list, is itself a list, with two elements. The first element is an integer (0/1) that classifies the sentence based on whether or not it contains tokens to be annotated. The second element is of length BERT_tokenizer(*sentence_i*).tokens, that contains a label for each token in the sentence.
  
- the function "add_job_ads_to_json_file()" in the file [put name here] queries the table in the database that contains the job postings, and, for each posting in the database that is not in  [insert name of json file], it adds a dictionary to the list in the json file with the information described in the previous bullet point.

- two functions--"predict_and_label()" and "auto_labeler", both stored in the file [put name here]--are used to expedite labelling training data in the following ways:

  - predict_and_label: this function accelerates labelling train/test/validation data by using the fact that, as the sentence and token classification models are progressively fine tuned, most of their predictions will be correct. The function uses this by taking a job description, and first feeding the sentences in the description to the sentence classifier. The sentence classifier predicts the appropriate labels, and each sentence is then output, color coded according to the label it was assigned, and asks for a list of the sentences that were not labelled correctly. A human annotator indicates the sentences that are mislabeled. Now, all the sentences are labelled. Next, the same process is done to label the words in the sentence--the model makes predictions on the words, these predictions are indicated via color coding words according to label, and a human annotator indicates which tokens are mislabeled. After the sentences in some number of descriptions are labelled using this approach, both models are fine tuned with the newly labelled data. The process then repeats--the models are used to predict labels on new job descriptions, and a human annotator corrects the incorrect predictions--but   now, because the model is more refined, less feedback from the human annotator is required. *<-- would be nice to benchmark this, as do the process--how much less feedback is required after each round of fine tuning*

  - *discuss auto_labeler here*

    








(for self/delete this later) guiding principles of the read me:

- how do you run it?
- how do you train it?
- folder with sample outputs
- a "how to create the missing pieces (the first two bullet points)" s.t. the stuff in the repo that relies on them, works with what you've made (nobody is actually going to use this, so does that actually make sense)