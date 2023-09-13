## Annotation Guidelines:

*Need a sentence introduction and explanation of the 'B', 'I', 'O' stuff, up top here!*



- **(1) Annotated:** nouns that describe the desired education level, qualifications and degrees of study that the person in the position has 

  

- **(2) Annotated:** nouns that describe experience or skills that the company wants applicants to have; technologies that it wants applicants to have used; journals that the it wants the applicant to have published in; and concrete qualities related to the position it would appreciate the applicant having 

  

- **(3) Annotated:** nouns that are things that the person in the position, or the company as a whole uses, modifies/improves, works on, maintains, creates, or is involved in doing, barring the exceptions below. 

  - **(3a) exception:** proper nouns (but not common nouns) that the company as a whole works on	

  

- **(4) Handling unclear situations in (1-3):** The below guidelines add more detail on how to apply the guidelines stated in (1-3):

  - *(4d-i) Modifying nouns:* is more detail required than the below? 
  - *(4d-ii)* Nouns that would not otherwise be annotated, but appear immediately next to nouns that themselves are annotated, and contribute to the description of the concept, are themselves annotated. But if the nouns in question are separated by punctuation (besides hyphens), they are not annotated
    - example: "machine learning research" is annotated "machine (B) learning (I) research (I)", even though "research", appearing isolated from "machine learning" would not be annotated
    - example: "model development, validation, and implementation" is annotated "model (B) development (I)", because , out of context, "validation" and "implementation" are abstract concepts. *See "(6) Future Improvements" for ...*
    - example: "monitoring model input and output data distributions" is annotated "output (B) data (I) distributions (I)", because out of context, "model input" is a vague concept, and "output" in "output data distributions" does contribute to the meaning of the concept. *See "(6) Future Improvements" for ...*
  - *(4d-iii)* In situations in which the thing people in the position will be working on is described, but the act of the person working on it is not described, for example sentences with the form "*object_made_by_person_in_job* may involve X, Y, and Z", if the thing fits the above guidelines, it is annotated
  - *(4d-iv)* When the qualifications/qualities/skills that the company wants the applicant to have is framed as a question, annotate these as would be annotated if they were listed in a more conventional way.
    - example: "machine learning" and "NLP" are annotated in the sentence "Do you love machine learning and NLP?"
  - **(4d-v) For nouns that the above guidelines do not clearly indicate whether or not to annotate it, use a search engine to search "what is *specific_noun* , in the context of jobs"; if it returns a concrete thing related to the job, that can be learned about to become more qualified for the position, then annotate. If not, do not annotate it.**
    - example: "reusable platform component",  "business process", "strategic organizational decisions" are all annotated, because when they are searched, they bring up a concrete idea that can be researched, and that an applicant can improve their facility with the concept. But "autonomous development" is not annotated, because when it is searched, it brings up resources about child rearing, which is unrelated to the position of the job description that it appeared in.

  

- **(5) Annotated:** Adjectives that come immediately before nouns, that describe inherent qualities or features of the subject; or that are necessary for the subject to be useful in the context that it is being referred to in. In these cases, the adjective-noun combination is considered a single entity and annotated like "adjective (B) noun (I)", e.g. "autonomous (B) vehicle (I)"

  - **(5a) Handling unclear situations:**

    - *(5a-i)* in the case of compound adjectives, if there is only a hyphen, or no punctuation between the adjectives, both adjectives are included in the annotation

    - *(5a-ii)* adjectives separated from the noun by something other than a punctuation (e.g. a comma), are *not* annotated

    - *(5a-iii)* adjectives that add contextual/attributive information to the subject, or are subjective, are *not* annotated

      - example: "high-quality" in "high-quality publications" is **not** annotated
      - example: "proprietary" in "proprietary docking library" is **not** annotated
      - example: "cutting-edge" in "cutting-edge machine learning model" is **not** annotated

    - *(5a-iv)* if it is still unclear whether or not to annotate the adjective, ask yourself "could this guide the study of 'learning more about the subject', or not". If yes, annotate the adjective; else, do not annotate it. (?) Or google "particular_adjective particular_noun" and "particular_noun", and see whether the adjective makes a difference in the of how useful the concept is. 

      

- **(6) Handling abbreviations:** Abbreviations of things that should be annotated, should themselves be annotated if either (i) the word that they are an abbreviation for is returned when searching "what is *specific_abbreviation* an abbreviation for, in the context of jobs" into a search engine, or (ii) the word that the abbreviation is for is returned when searching "what might *specific_abbreviation* be an abbreviation for, in the context of *specific_industry/field_of_work*" into a search engine, where "specific industry" is the industry that the position is in.

  - example: in the phrase "Experience working with native machine learning orchestration systems like MLflow, Airflow, or TFX", the abbreviation "TFX" is annotated because an explanation for what it is is returned when searching "what might TFX be an abbreviation for, in the context of machine learning?"
  - example: "...DNA - encoded library ( DEL ) platform" is annotated DNA (B) - (B) encoded (B) library (I) ( DEL (B) ) platform (O). But note that if the abbreviation were not there, "platform would be annotated"; the phrase "...DNA - encoded library platform" is labelled DNA (B) - (B) encoded (B) library (I) platform (I).



- **(7) Determining unit boundaries:**  Words separated by hyphens, as well as the hyphen itself, are all assigned the same label ('B', 'I', or 'O'). 
  - example: "full-stack development" is annotated full(B) - (B) stack (B) development(I)
  - example: "end - to - end solutions" is annotated end(B) -(B) to(B) -(B) end(B) solutions(I)



- **(8) Global exceptions:** The below are *not* annotated, even if the above guidelines would otherwise dictate that they be

  - (8a) job titles

  - (8b) abstract, general qualities that are difficult to assess, that the company wants the applicant to have (e.g. self-starter, team-player, storyteller, data-wrangler etc.) 

  - (8c) abstract concepts that can be done across many domains/industries, that are useless without more context. Note: concrete technologies that are ubiquitous (e.g. Microsoft Office) **are** annotated

    - example: "research" in the phrase "you will conduct research" is **not** annotated

    - example: "breakthrough" in the phrase "you will create breakthroughs" is **not** annotated

    - example: "data" in the phrase "the position involves storage and delivery of data" is **not** annotated
    - example: "mentoring" in the phrase "foster a culture of mentoring across teams by..."

  - (8d) entities that the person/team is doing the task for (e.g. "customers", "end users"), unless the word is a part of a concept that can be learned about to improve at the position (e.g. "customer satisfaction" **is** annotated)

  - (8e) Gerunds--words derived from a verb, but that function as a noun--are annotated only if their presence next to a noun makes the "noun-gerund" or "gerund-noun" sequence into a bona fide noun

    - example: "learning" in "machine learning" is annotated

    - example: "building" in "you will work on building houses" is *not* annotated

      

- **(9) More examples:**

  - phrase: "Identify and eliminate bottlenecks in the **ML stack**, from **data-loading** up to the **GPU**"
    - note: determining not to label "bottlenecks" required using rule 8c; determining to label "data-loading" required applying rule 4d-v
  - sentence: "Your team creates and leverages cutting-edge **ML models**, especially **Large Language Models** (**LLMs**) to extract new signals from **unstructured data** and make insightful, **actionable predictions** for customers."
    - note: determining to label "unstructured data" required using rule 4d-v
  - phrase: "We have been building a cutting-edge, machine-learning-enabled capability to design..."
    - note: nothing in this phrase is labelled, because a "machine-learning enabled capability" is too abstract (8c)
  - sentence: "Our client’s machine learning products are their core value proposition for their customers, so ML efficiency has a direct connection to their value to customers and as a company."
    - note: this phrase comes from a job posting from a recruiter, so the language is atypical--their "client" is the company that the applicant would be working for. For this reason, "machine learning products" and "ML efficiency" are both annotated, because, were the applicant to get the position, those are things that the company broadly works on as a whole, and by rule 3, should be annotated.



- **(10) Future improvements to the guidelines:**
  - Dictate methods of connecting "amount of experience" to "skill that the hiring entity wants the applicant to know"
    - example: from the phrase, "5+ years of experience building machine learning products", a tuple (5, machine learning products), would be extracted, instead of just "machine learning products"
  - Be able to handle modifying nouns that aren't adjacent to the noun of interest
    - example (from 4): three sets of entities would be extracted from the phrase "model development, validation, and implementation": "model (B) development (I)", "model (B) validation (I)", and "model (B) implementation (I)"
    - example (from 4): two sets of entities would be extracted from the phrase "monitoring model input and output data distributions": "model input data distributions" and model output data distributions
  - Develop guidelines to handle verbs and adverbs 
  - Label words according to the section that they appear. For example, have "B-skills" and "I-skills" to label words that describe skills that the company desires the applicant to have, versus "B-responsibilities" and "I-responsibilities" to label words that describe the responsibilities that a worker in the position has
  - use a well-defined process to determine when the guidelines are sufficiently stable -- e.g. "N postings have been annotated by M people, with less than K% disagreement between the annotations"





