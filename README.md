# Freebase-to-Wikipedia

This repository contains a Freebase dump parser that extracts Freebase IDs (MID), entity name and links to Wikipedia (entity page url and curid). 
It works for all languages of Wikipedia available in the Freebase triples dump (default is 'en'). 

## Usage


First, download the latest dump from [Freebase Data Dumps](https://developers.google.com/freebase/)

Then, use the following command to run the code:

```
python freebase2wikipedia.py <path to freebase-rdf-latest.gz>
```

Using this command, the script will create an auxiliary file <freebase_wikipedia_dump> and then a final tsv file <mid2wikipedia.tsv> containing Freebase links to Wikipedia:

```
mid	name	wikipedia_link	curid
/m/04lk0z9	1925 Open Championship	1925_Open_Championship	19247817
/m/04kls6	Ekati Diamond Mine	Ekati_Diamond_Mine	1232295
/m/03c0j04	Woodstock High School	Woodstock_High_School_(New_Brunswick)	13283256
/m/04grcjm	Sovla	Sovla	18867851
/m/0nhqw_l	Svein Christiansen	Svein_Christiansen	37512440
```


Using the latest Freebase dump, the script is able to extract 4,389,796 Freebase links to English Wikipedia.
Python v2.7 is required for running the code.
