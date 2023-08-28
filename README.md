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

- two functions--"predict_and_label()" and "auto_label()", both stored in the file [put name here]--are used to expedite labelling training data in the following ways:

  - predict_and_label: This function accelerates labelling train/test/validation data by using the fact that, as the sentence and token classification models are progressively fine tuned, most of their predictions will be correct. The function uses this by taking a job description, and first feeding the sentences in the description to the sentence classifier. The sentence classifier predicts the appropriate labels, and each sentence is then output, color coded according to the label it was assigned, and asks for a list of the sentences that were not labelled correctly. A human annotator indicates the sentences that are mislabeled. Now, all the sentences are labelled. Next, the same process is done to label the words in the sentence--the model makes predictions on the words, these predictions are indicated via color coding words according to label, and a human annotator indicates which tokens are mislabeled. After the sentences in some number of descriptions are labelled using this approach, both models are fine tuned with the newly labelled data. The process then repeats--the models are used to predict labels on new job descriptions, and a human annotator corrects the incorrect predictions--but   now, because the model is more refined, less feedback from the human annotator is required. *<-- would be nice to benchmark this, as do the process--how much less feedback is required after each round of fine tuning* * **make a 'see example notebook for how to use'**

  - auto_label: This function expedites labelling train/test/validation data for the sentence classification model by using the fact that sentences that contain certain words, or appear at a given place within a job description, are far more likely to be labelled a certain way. For example, nearly all sentences with the word "SQL" in it  should be labelled "this sentence contains words to extract from the job description". Similarly, the last few sentences of each job description typically should be labelled "does not contain words to extract from the job description", because often times they are legal statements. The "auto_label" function uses these facts to expedite labelling, by allowing the user to indicate that they want to use "keyword mode" or "first and last sentences mode".

    -  keyword mode: The user enters a word, as well as a default label, and all sentences in the dataset with that word are output to an html file. The user determines which of the sentences in the html file should be given the default label, indicates this to the program, and then those sentences are assigned that label. There is also an option to indicate only the sentences in the file that *should not* be assigned the default label, up to the number that the user looked through (if ten thousand sentences have "SQL" in them, the user might not want to look at every sentence in one sitting).
    - first and last sentences mode: This mode works like keyword mode, except that the user inputs a percentage and a default label. The program outputs the first N% and last N% of each job to to a html file, and then the user indicates which of the sentences should/should not be assigned the default label. 
    - Two things to note:
      - These were used to create a more balanced dataset--if you only use "predict_and_label", because most of the sentences in the description do not contain words to annotate, the data will be unbalanced.
      - The "keyword mode" of the "auto_label" function will likely lead to overfitting the keywords used, if you aren't careful. Future work involves using a part-of-speech tagger and data augmentation to mitigate this. For example, if more data was created from all of the sentences that were labelled "has word to extract" due to having "SQL" in them, by replacing all of the proper nouns with proper nouns from another field, this would force the model to associate the structure of the sentence, with the label, instead of the word "SQL". **<-- make a 'see example notebook for how to use'**


    








(for self/delete this later) guiding principles of the read me:

- how do you run it?
- how do you train it?
- folder with sample outputs
- a "how to create the missing pieces (the first two bullet points)" s.t. the stuff in the repo that relies on them, works with what you've made (nobody is actually going to use this, so does that actually make sense)