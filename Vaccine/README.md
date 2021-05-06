# team-u03
M E 369P project team U03 (Spring 2021)

Our program examines a set of COVID vaccination data in US states and federal entities. The dataset can be found here: https://github.com/owid/covid-19-data/tree/master/public/data/vaccinations. Important columns to mention are date, location, share_doses_used, and people_vaccinated_per_hundred. share_doses_used defines the share of vaccination doses administered among those recorded as shipped and people_vaccinated_per_hundred_ represents the total number of people (out of 100) who received at least one vaccine dose.

Packages need to run our code include:

* Numpy
* Pandas
* Plotly
* Sklearn

The main objective of our program is to observe trends of COVID vaccine efficiency in the US, where efficiency is the percentage of shipped vaccines that have been administered. We will then use these trends to predict the efficiency of future months.

To use our program:

1. Run 'https://github.com/asniv/team-u03.git' in a windows terminal.
2. Open /Vaccine/vaccine_projector.py to start our program.
3. Enter desired state into program, followed by remaining states or 'done'.
4. An interactive plot will show trends in vaccine efficiency and herd immunity for those states over the past four months.
5. Next, we will train our data to predict future vaccine trajectory using a Linear Regression.
6. Input the range of dates you would like to use to train our data, starting with the end date.
7. Enter a date that you would like to predict vaccine efficiency until.
8. The plots will now include our predicted vaccine efficency values.
