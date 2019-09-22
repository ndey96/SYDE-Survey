import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

df = pd.read_excel('part_1.xlsx')
terms = [
    '1a',
    '1ac',
    '1b',
    '1bc',
    '2a',
    '2ac',
    '2b',
    '2bc',
    '3a',
    '3ac',
    '3b',
    '3bc',
    '4a',
    '4b',
]
school_terms = []
work_terms = []
uppercase_terms = []
uppercase_school_terms = []
for term in terms:
    if 'c' in term:
        work_terms.append(term)
    else:
        school_terms.append(term)
        uppercase_school_terms.append(term.upper())
    uppercase_terms.append(term.upper())

# def barh(col, fname, data=None):
#     if data is None:
#         data = df[col]

#     total_count = len(data)
#     plt.figure(figsize=(10, 8))
#     sns.countplot(y=df[col])
#     plt.gca().set_xticklabels([
#         '{:.0f}%'.format(x * 100 / total_count) for x in plt.gca().get_xticks()
#     ])
#     plt.title(col)
#     plt.xlabel('Percentage')
#     # plt.figure().subplots_adjust(left=2)
#     # plt.tight_layout()
#     plt.savefig('graphs/' + fname + '_bar')
#     plt.close()


def barh(col, fname, data=None, bar_order=None):
    if data is None:
        data = df[col]
    c = Counter(data)
    bar_df = pd.DataFrame({'keys': list(c.keys()), 'vals': list(c.values())})
    if bar_order:
        bar_df['ii'] = [bar_order.index(x) for x in bar_df['keys']]
        bar_df = bar_df.sort_values(by='ii', ascending=True)
    else:
        bar_df = bar_df.sort_values(by='vals', ascending=True)

    labels = bar_df['keys']
    y_pos = np.arange(len(bar_df))
    plt.figure(figsize=(10, 8))
    plt.barh(y_pos, bar_df['vals'], align='center', color=sns.color_palette())
    plt.yticks(y_pos, labels)
    plt.gca().set_xticklabels(
        ['{:.0f}%'.format(x * 100 / len(df)) for x in plt.gca().get_xticks()])
    plt.xlabel('Percentage of Class')
    plt.title(col)
    plt.tight_layout()
    plt.savefig('graphs/' + fname + '_bar')
    plt.close()


def boxplot(cols, fname, title, xlabels, ylabel):
    boxplot_data = [df[col].dropna() for col in cols]
    plt.figure(figsize=(10, 8))
    sns.boxplot(data=boxplot_data)
    plt.ylabel(ylabel)
    plt.gca().set_xticklabels(xlabels)
    plt.title(title)
    plt.tight_layout()
    plt.savefig('graphs/' + fname + '_boxplot')
    plt.close()


def density(cols,
            fname,
            title,
            labels=None,
            xlims=None,
            ylims=None,
            rug=False,
            line_labels=None):
    plt.figure(figsize=(10, 8))
    if type(cols) is not list:
        cols = [cols]
    for idx, col in enumerate(cols):
        line_label = None
        if line_labels:
            line_label = line_labels[idx]
        sns.distplot(
            df[col].fillna(0),
            hist=False,
            kde=True,
            kde_kws={
                'shade': True,
                'linewidth': 3
            },
            label=line_label,
            rug=rug)
    if xlims:
        plt.xlim(xlims)
    if ylims:
        plt.ylim(ylims)
    if labels:
        plt.gca().set_xticklabels(labels)
    plt.ylabel('Proportion of Class')
    plt.xlabel(title)
    plt.tight_layout()
    plt.savefig('graphs/' + fname + '_density')
    plt.close()


def line(y_col, fname, title, data):
    plt.figure(figsize=(10, 8))
    sns.lineplot(x='Term', y=y_col, data=data)
    # plt.ylabel(ylabel)
    # plt.gca().set_xticklabels(xlabels)
    plt.title(title)
    plt.tight_layout()
    plt.savefig('graphs/' + fname + '_lineplot')
    plt.close()


# for col in df.columns:
#     print(col)

barh('What gender do you identify with?', 'gender')
birth_years = [1991, 1992, 1994, 1995, 1996, 1997]
barh('What year were you born in?', 'birth_year', bar_order=birth_years)
barh('Which ethnic background(s) do you identify with?', 'ethnicity')
barh('What most closely describes your religious school of thought?',
     'religion')
barh('What city did you grow up in?', 'home_town')
barh('How would you describe your political leanings?', 'political')
stress_qs = [term + 'How stressful was this term?' for term in terms]
boxplot(
    stress_qs,
    'stress',
    'Stress',
    xlabels=uppercase_terms,
    ylabel='Stress Level (1-10)')
political_labels = ['Left'] + [''] * 5 + ['Right']
density(
    cols='How would you describe your political leanings?',
    fname='political',
    title='Political Leaning',
    labels=political_labels,
    xlims=(1, 7))
density(
    'What was your entrance average from high-school (top 6 grades only)?',
    'hs_avg',
    'High School Entrance Average',
    xlims=(80, 100))
accelerated_programs = []
for el in df[
        'Which of the following accelerated programs, if any, did you graduate from?']:
    accelerated_programs += el.split(', ')
barh(
    'Which of the following accelerated programs, if any, did you graduate from?',
    'accelerated_programs', accelerated_programs)
hs_extras = []
for el in df[
        'Which of the following extracurricular activities did you do in high school, if any?']:
    el = el.replace(
        'Participate in a leadership program (SHAD, build a school in Africa)',
        'Leadership Program')
    hs_extras += el.split(', ')
barh(
    'Which of the following extracurricular activities did you do in high school, if any?',
    'hs_extras', hs_extras)
barh(
    'Before starting university, what industry did you see yourself working in?',
    'hs_industry')
faculties_applied_to = []
for el in df['What university faculties did you apply to?']:
    faculties_applied_to += el.split(', ')
barh('What university faculties did you apply to?', 'faculties_applied_to',
     faculties_applied_to)
incomes = [
    '$0 - 50k', '$50 - 100k', '$100 - 150k', '$150 - 200k', '$200 - 250k',
    '$250 - 300k', '$300k+', "Don't Know"
]
incomes = [x for x in incomes]
barh(
    "What was your parents' combined income at the time you entered university?",
    'household_income',
    bar_order=incomes)

term_avg_qs = [
    'What was your term average in ' + term.upper() + '?'
    for term in school_terms
]
density(
    cols=term_avg_qs,
    fname='term_avg',
    title='Term Average',
    line_labels=[t.upper() for t in school_terms],
    labels=None,
    xlims=(40, 100),
    ylims=(0, 0.1))

barh(
    'What is the highest level of education achieved by either of your parents?',
    'parent_education')

barh('Have either of your parents studied/worked in a STEM-related field?',
     'parent_stem')
barh('Were either of your parents born in North America?',
     'parent_north_america')
barh(
    'Approximately how much of your total university expenses were funded by your family? ',
    'parent_tuition')
debt_savings_order = [
    'None', '0-5k', '5k-10k', '10-20k', '20-50k', '50k+', 'Prefer not to say'
]
debt_savings_order.reverse()
debt_savings_order = [x for x in debt_savings_order]
barh(
    'How much debt are you graduating with?',
    'debt',
    bar_order=debt_savings_order)
barh(
    'How much do you have in savings?', 'savings', bar_order=debt_savings_order)
barh(
    "Of your 5 closest friends you've made in university, how many are in SYDE?",
    'syde_friends')
lecture_attendance_df = pd.DataFrame({
    'Term': [],
    'Percentage of Lectures Attended': []
})
for term in school_terms:
    orig_vals = df[term + 'How often did you attend lectures this term?']
    new_vals = []
    for val in orig_vals:
        if val == 'Almost always':
            new_vals.append(100)
        elif val == 'Most of the time':
            new_vals.append(75)
        elif val == 'About half the time':
            new_vals.append(50)
        elif val == 'Occasionally':
            new_vals.append(25)
        elif val == 'Almost never':
            new_vals.append(0)
        else:
            print(val)
    df[term + 'lecture_attendance'] = new_vals
    lecture_attendance_df = lecture_attendance_df.append(
        pd.DataFrame({
            'Term': [term.upper()] * len(new_vals),
            'Percentage of Lectures Attended': new_vals
        }),
        ignore_index=True)

lecture_attendance_qs = [term + 'lecture_attendance' for term in school_terms]
boxplot(
    lecture_attendance_qs,
    'lecture_attendance',
    'Lecture Attendance',
    xlabels=uppercase_school_terms,
    ylabel='Percentage of Lectures Attended')

line(
    y_col='Percentage of Lectures Attended',
    fname='lecture_attendance',
    title='Lecture Attendance',
    data=lecture_attendance_df)

####################################################
# Part 2
####################################################
