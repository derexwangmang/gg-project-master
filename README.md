**Golden Globe Project**
COMP_SCI 337: Natural Language Processing, Spring 2022

## CONTRIBUTORS

- Andrew Hong
- Allison Rhee
- Derex Wangmang
- Matthew Wuyan

## OBJECTIVE

This is an NLP project on identifying hosts, awards, presenters, nominees, and winners for each award, based on Twitter tweets during the 2013 and 2015 Golden Globes Awards Ceremony. In addition to completing the basic requirements for this project, we have also implemented extra features, including sentiment analysis and the "Red Carpet" (determining who Twitter thought was the best and worst dressed).

## HOW TO RUN

First clone this repository. We recommend creating a virtual enviornment for the packages required in the project. To install the necessary packages, run `pip install -r requirements.txt`. Next, include `gg2013.json` and `gg2015.json`, the datasets of Twitter tweets, within the main directory.

By running `python3 gg_api.py`, you will be able to run `pre_ceremony()`, which processes the raw tweet data into more machine readable text data and `main()`, which will run the main identification tasks of this project and output them to `STDOUT` and `results{YEAR}.txt`, based on user input for the `YEAR` of the Golden Globes they want information from.

If you would like to test the performance of `pre_ceremony()`, we recommend that you first delete `processedtweets2013.txt` and `processedtweets2015.txt` in the main directory, and all files **except** for `awardsandfilters.txt` in the subdirectory `awardsandfilters/`. `pre_ceremony()` will generate fresh copies of those files.

To see autograder results, run `python3 autograder.py`. Expected results are within `autograder_results.txt`.

## GITHUB Repository

The Github repository can be located [here](https://github.com/derexwangmang/gg-project-master).
