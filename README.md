# SYDE-Survey

This repository contains all of the materials that [Jason](https://github.com/iFallUpHill) and I used to create the [SYDE 2019 Class Profile](http://ndey96.github.io/syde_2019_class_profile.pdf).

First we asked our class to fill out a two-part survey powered by Google Forms. The first part of the survey contains most of the questions. The second part of the survey contains the most sensitive questions to better protect the privacy of the respondents. If you would like to have a copy of the Google forms we used, send me an email at nsdey@uwaterloo.ca.

Once your class fills out the forms, you can export the response data as a `.xlsx` file. The `graphs.py` file expects a files called `part_1.xlsx` and `part_2.xlsx`.

To generate all of the graphs in the `graphs/` directory, run `python graphs.py`. Note: Python 3 is required.

`clean.py` was used to perform some basic data cleaning.

I hope this repository is helpful!
