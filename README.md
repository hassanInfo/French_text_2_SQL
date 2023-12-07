<div align="center">

# Text to SQL: Query writen in French to SQL 

</div>

This NLP project focuses on advancing the translation of French text to SQL, specifically targeting key SQL commands such as SELECT, FROM, WHERE, and GROUP BY. Four distinct approaches have been rigorously tested to enhance the accuracy and efficiency of the translation process.

Each aproache has its one ipynb file:
* t5_base_finetuned_wikiSQL_FR2SQL.ipynb
* NER_FR2SQL_LSTM.ipynb
* NER_FR2SQL_BERT.ipynb
* FR2SQL_seq2seq.ipynb
Data preparation ipynb file:
* Spider_FR2SQL_processing.ipynb
Apps:
* App_Streamlit_Docker_BERT/
* App_Streamlit_Ngrok_FR2SQL_BERT/


## Aproches

The first method we have used is called **ln2sql**, which is located in the repository [[1]](#recourses). It is a rule-based method.

![Copy of Add a heading-04](https://github.com/hassanInfo/NLP_FR2SQL_project/assets/85229840/555e344c-e492-4f74-beb4-a265c9c1fc7b)

![Copy of Add a heading-05](https://github.com/hassanInfo/NLP_FR2SQL_project/assets/85229840/2a7d7151-80e1-4c62-be9f-0a10ecccb4c8)

The concept behind the following approach involves fine-tuning on the wikiSQL dataset. One drawback of this method is that, by default, the dataset lacks a defined table name in each record (replaced with mytable). Post-processing is required to translate English SQL values into French (like "SELECT name ..." to "SELECT nom ...").

![Copy of Add a heading-06](https://github.com/hassanInfo/NLP_FR2SQL_project/assets/85229840/0e16d2ef-ca29-4cd1-87c7-67b7f4385801)

In this section, we employed Named Entity Recognition (NER) by treating each token in a French query as an entity. The primary challenge we faced was the absence of a dataset containing both French queries and their corresponding SQL. While English datasets were available, we addressed this gap by constructing a French dataset. We accomplished this by translating English queries from the Spider Dataset to French. Subsequently, through the use of the Doccan software for data annotation, we prepared and trained several machine learning models.
* We trained an LSTM, which achieved significant results for short sentences. To address this challenge, we proposed utilizing BERT.
* We conducted finetuning on BERT.

![Copy of Add a heading-07](https://github.com/hassanInfo/NLP_FR2SQL_project/assets/85229840/9a69f53e-c394-49fd-8f03-2c6bfbe17408)

![Copy of Add a heading-09](https://github.com/hassanInfo/NLP_FR2SQL_project/assets/85229840/a8bb588e-77bb-4c8b-a85e-ed02dd4d35e3)

![Copy of Add a heading-10](https://github.com/hassanInfo/NLP_FR2SQL_project/assets/85229840/3736af69-9d39-4ebd-be23-d1853a15718e)

![Copy of Add a heading-11](https://github.com/hassanInfo/NLP_FR2SQL_project/assets/85229840/dc04648d-044b-42a1-a35c-c14c28fb2a20)

![Copy of Add a heading-12](https://github.com/hassanInfo/NLP_FR2SQL_project/assets/85229840/56ae8644-6193-48af-be68-f967e43fdb64)

![Copy of Add a heading-13](https://github.com/hassanInfo/NLP_FR2SQL_project/assets/85229840/2804f480-5ffc-475a-9248-79ac657e67fc)

![Copy of Add a heading-14](https://github.com/hassanInfo/NLP_FR2SQL_project/assets/85229840/f945e697-4ec3-42ce-8fcc-1b0e4d8522ed)

![Copy of Add a heading-15](https://github.com/hassanInfo/NLP_FR2SQL_project/assets/85229840/e6c50b49-b1c1-4131-8dc3-eaf493a4d79b)

![Copy of Add a heading-16](https://github.com/hassanInfo/NLP_FR2SQL_project/assets/85229840/4066998c-e11e-49c2-8860-0df81d6fdeac)

![Copy of Add a heading-17](https://github.com/hassanInfo/NLP_FR2SQL_project/assets/85229840/75495251-0f29-4fe8-aa71-e77daf78987e)

![Copy of Add a heading-18](https://github.com/hassanInfo/NLP_FR2SQL_project/assets/85229840/50f2dc4c-f4cf-4fc7-9b57-3511061fb8db)

The fift aproch consists of considering the problem as pure translation from one language to another, keep in mind that to train from scratch the transformer seq2seq model need a huge data.  

![Copy of Add a heading-19](https://github.com/hassanInfo/NLP_FR2SQL_project/assets/85229840/2d31f8be-9645-4ec4-84b1-1969760688ac)

![Copy of Add a heading-20](https://github.com/hassanInfo/NLP_FR2SQL_project/assets/85229840/ca65452a-1299-4220-b845-a45151f0eebb)

![Copy of Add a heading-21](https://github.com/hassanInfo/NLP_FR2SQL_project/assets/85229840/920e27d0-9c14-44fd-b47b-01dbfcd94a9a)

![Copy of Add a heading-22](https://github.com/hassanInfo/NLP_FR2SQL_project/assets/85229840/650d48a3-87ea-49f5-9be7-b3ec10233d31)

# Deployment

![Copy of Add a heading (4)](https://github.com/hassanInfo/French_text_2_SQL/assets/85229840/66143dc4-11e7-42e0-9b18-664a347aa162)

![Copy of Add a heading-24](https://github.com/hassanInfo/NLP_FR2SQL_project/assets/85229840/ffe7063c-fd4a-4e31-b30b-15b8144f1396)

![Copy of Add a heading-25](https://github.com/hassanInfo/NLP_FR2SQL_project/assets/85229840/b3dc705c-8b3d-4982-b2aa-c8dcae94171f)

![Copy of Add a heading-26](https://github.com/hassanInfo/NLP_FR2SQL_project/assets/85229840/3eb06231-8606-46e0-ac8b-627852d44fa5)

![Copy of Add a heading-27](https://github.com/hassanInfo/NLP_FR2SQL_project/assets/85229840/7461c16b-70d2-4992-b7b3-eb2cb2bec5d9)


## Resources

[1] [https://github.com/FerreroJeremy/ln2sql](https://github.com/FerreroJeremy/ln2sql)

[2] [https://www.researchgate.net/publication/280700277_fr2sql_Interrogation_de_bases_de_donnees_en_francais](https://www.researchgate.net/publication/280700277_fr2sql_Interrogation_de_bases_de_donnees_en_francais)

[3] [https://github.com/DukeNLIDB/NLIDB](https://github.com/DukeNLIDB/NLIDB)

[4] [https://towardsdatascience.com/natural-language-to-sql-from-scratch-with-tensorflow-adf0d41df0ca](https://towardsdatascience.com/natural-language-to-sql-from-scratch-with-tensorflow-adf0d41df0ca)

[5] [https://towardsdatascience.com/text-to-sql-learning-to-query-tables-with-natural-language-7d714e60a70d](https://towardsdatascience.com/text-to-sql-learning-to-query-tables-with-natural-language-7d714e60a70d)

[6] [https://arxiv.org/pdf/2205.06983.pdf](https://arxiv.org/pdf/2205.06983.pdf)

[7] [https://www.cse.scu.edu/~m1wang/projects/NLP_naturalLanguage2SqlQuery_18w.pdf](https://www.cse.scu.edu/~m1wang/projects/NLP_naturalLanguage2SqlQuery_18w.pdf)

[8] [https://arxiv.org/pdf/1709.00103.pdf](https://arxiv.org/pdf/1709.00103.pdf)
