# build-dictionary-of-given-word-list

This program makes a dictionary in a printable format (not python dictionary) of given words using [(unofficial) Google Dictionary API](https://googledictionaryapi.eu-gb.mybluemix.net/) and a local .csv file which provide word meanings and example sentences.

`words.csv` is the input file which is a comma-separated value file containing four columns named: `english, bengali, prep, and example`. Output dictionary will be made up using the `english` column and other columns will be used also for meaning and example sentence.

The program first makes a `dic.json` file containing details of given words fetched from [(unofficial) Google Dictionary API](https://googledictionaryapi.eu-gb.mybluemix.net/) along with Bengali meaning, preposition and example that are given in `words.csv` file. That's mean data fetched from [Google Dictionary API](https://googledictionaryapi.eu-gb.mybluemix.net/) and the `words.csv`  are merged in `dic.json` file.


Then it makes a printable pdf file as the dictionary using LaTex.


