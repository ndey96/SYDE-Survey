import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re

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
uppercase_work_terms = []

for term in terms:
    if 'c' in term:
        work_terms.append(term)
        uppercase_work_terms.append(term.upper())
    else:
        school_terms.append(term)
        uppercase_school_terms.append(term.upper())
    uppercase_terms.append(term.upper())


def get_unique_vals(qs):
    unique_work_cities = []
    for q in qs:
        unique_work_cities += list(df[q])
    return np.unique(unique_work_cities)


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
        ['{:.0f}%'.format(x * 100 / len(data)) for x in plt.gca().get_xticks()])
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
    plt.xlabel('Term')
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


def line(y_col, fname, title, data, ylims=None):
    plt.figure(figsize=(10, 8))
    sns.lineplot(x='Term', y=y_col, data=data, ci='sd')
    # plt.ylabel(ylabel)
    # plt.gca().set_xticklabels(xlabels)
    if ylims:
        plt.ylim(ylims)
    plt.title(title)
    plt.tight_layout()
    plt.savefig('graphs/' + fname + '_lineplot')
    plt.close()


def stacked_line(data, fname, title):
    plt.figure(figsize=(10, 8))
    plt.stackplot(
        uppercase_work_terms, list(data.values()), labels=list(data.keys()))
    plt.legend(loc='lower right')
    # plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.savefig('graphs/' + fname + '_stacked_lineplot')
    plt.close()


fast = True

if fast == False:

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
    stress_qs = [term + 'How stressful was this term?' for term in school_terms]
    boxplot(
        stress_qs,
        'stress',
        'Stress',
        xlabels=uppercase_terms,
        ylabel='Stress Level (1-10)')
    stress_df = pd.DataFrame({'Term': [], 'Stress Level (1-10)': []})
    for term in school_terms:
        responses = df[term + 'How stressful was this term?']
        c = Counter(responses)
        stress_df = stress_df.append(
            pd.DataFrame({
                'Term': [term.upper()] * len(responses),
                'Stress Level (1-10)': responses
            }),
            ignore_index=True)
    line(
        y_col='Stress Level (1-10)',
        fname='stress',
        title='Stress',
        ylims=None,
        data=stress_df)

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
        'None', '0-5k', '5k-10k', '10-20k', '20-50k', '50k+',
        'Prefer not to say'
    ]
    debt_savings_order.reverse()
    debt_savings_order = [x for x in debt_savings_order]
    barh(
        'How much debt are you graduating with?',
        'debt',
        bar_order=debt_savings_order)
    barh(
        'How much do you have in savings?',
        'savings',
        bar_order=debt_savings_order)
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

    lecture_attendance_qs = [
        term + 'lecture_attendance' for term in school_terms
    ]
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
        ylims=(0, 100),
        data=lecture_attendance_df)

    employment_rate_df = pd.DataFrame({'Term': [], 'Employment Rate': []})
    for term in school_terms[:6]:
        responses = df[term + 'Did you find a co-op job this term?']
        c = Counter(responses)
        employment_rate_df = employment_rate_df.append(
            {
                'Term': term.upper(),
                'Employment Rate': c['Yes'] / len(responses)
            },
            ignore_index=True)
    line(
        y_col='Employment Rate',
        fname='employment_rate',
        title='Employment Rate',
        ylims=(0.95, 1.01),
        data=employment_rate_df)

    rent_qs = [
        term +
        'How much did you pay for rent? Format as amount, currency, rate. For example: 600, CAD, monthly'
        for term in terms
    ]
    boxplot(
        rent_qs,
        'rent',
        'Rent',
        xlabels=uppercase_terms,
        ylabel='Rent (CAD/month)')

    commute_qs = []
    for term in terms:
        location = 'school'
        if 'c' in term:
            location = 'work'
        commute_qs.append(
            term + 'How long was your commute to ' + location + ' in minutes?')
    boxplot(
        commute_qs,
        'commute',
        'Commute',
        xlabels=uppercase_terms,
        ylabel='Commute Time (Minutes)')

    original_job_search_methods = [
        'Jobmine / Waterloo Works', 'External Application / Cold Applying',
        'Networking', 'Referral', 'Returned to an old job', 'CECA',
        'Facebook page: HH Job Listings', 'Previous offer'
        'SYDE Department Reached out', 'Self-employed', 'nan',
        'returned to old company for a new position'
    ]
    job_search_methods = [
        'Waterloo Works', 'Cold Applying', 'Networking/Referral',
        'Previous Employer', 'Self-employed'
    ]

    job_search_method_counts = {m: [] for m in job_search_methods}
    for term in work_terms:
        c = Counter(df[term + 'How did you find this job?'])
        temp_dict = {m: 0 for m in job_search_methods}
        for key, val in c.items():
            if key in ('Jobmine / Waterloo Works', 'CECA',
                       'SYDE Department Reached out'):
                temp_dict['Waterloo Works'] += val
            elif key in ('Facebook page: HH Job Listings',
                         'External Application / Cold Applying'):
                temp_dict['Cold Applying'] += val
            elif key in ('Previous offer', 'Networking', 'Referral'):
                temp_dict['Networking/Referral'] += val
            elif key in (
                    'returned to old company for a new position',
                    'Returned to an old job',
            ):
                temp_dict['Previous Employer'] += val
            elif key == 'Self-employed':
                temp_dict['Self-employed'] += val
        for k, v in temp_dict.items():
            job_search_method_counts[k].append(v)

    stacked_line(
        data=job_search_method_counts,
        fname='job_search_methods',
        title='How did you find your job?')

    print(get_unique_vals(
        [term + 'What was your job title?' for term in work_terms]))

    print(get_unique_vals(
        [term + 'In which city did you work?' for term in work_terms]))

    print(get_unique_vals([
        term + 'Which industry best describes the company you worked for?'
        for term in work_terms
    ]))

    feel_integrated = []
    for x in df[
            'If you were not part of the original SYDE 2019 cohort, do you feel like the class has integrated you into the 2019 community?']:
        if x != 'I am a part of the original SYDE 2019 cohort':
            feel_integrated.append(x)

    barh(
        'Do you feel the class has integrated you into the 2019 community?',
        'feel_integrated',
        data=feel_integrated)

    syde_friends_variant_bar_order = ['0-5', '5-10', '10-20', '20-30', '30+']
    barh(
        "How many friends do you have in the SYDE 2019 class?",
        'syde_friends_variant',
        bar_order=syde_friends_variant_bar_order[::-1])

    syde_social_bar_order = [2, 3, 4, 6, 7, 8]
    barh(
        "Out of 8 academic terms, how many of them did you attend at least one student-organized SYDE social event?",
        'syde_social',
        bar_order=syde_social_bar_order[::-1])

    inter_gen_syde_activites = []
    for el in df[
            'Which of the following inter-generational SYDE activities did you participate in, if any?']:
        # remove text between ()
        inter_gen_syde_activites += re.sub(r'\([^()]*\)', '', el).split(', ')

    barh(
        "inter_gen_syde_activites",
        'inter_gen_syde_activites',
        data=inter_gen_syde_activites)

    upper_year_contacts = []
    for el in df['How many upper years are you still in contact with?']:
        if el == 0:
            upper_year_contacts.append('0')
        elif 1 <= el <= 4:
            upper_year_contacts.append('1-4')
        elif 5 <= el <= 9:
            upper_year_contacts.append('5-9')
        elif el > 9:
            upper_year_contacts.append('10+')

    upper_year_contacts_order = ['0', '1-4', '5-9', '10+']
    barh(
        'How many upper years are you still in contact with?',
        'upper_year_contact',
        data=upper_year_contacts,
        bar_order=upper_year_contacts_order[::-1])

    lower_year_contacts = []
    for el in df['How many lower years are you still in contact with?']:
        if el == 0:
            lower_year_contacts.append('0')
        elif 1 <= el <= 4:
            lower_year_contacts.append('1-4')
        elif 5 <= el <= 9:
            lower_year_contacts.append('5-9')
        elif el > 9:
            lower_year_contacts.append('10+')

    lower_year_contacts_order = ['0', '1-4', '5-9', '10+']
    barh(
        'How many lower years are you still in contact with?',
        'lower_year_contact',
        data=lower_year_contacts,
        bar_order=lower_year_contacts_order[::-1])

alum_donations = []
for el in df['Which, if any, do you plan on donating to as an alumni?']:
    if el in ('not sure', 'not sure yet') or 'Mostly undecided' in el:
        continue
    alum_donations += el.split(', ')

barh(
    'Which, if any, do you plan on donating to as an alumni?',
    'alum_donations',
    data=alum_donations)

uni_extras = []
for el in df['Did you do any of the following during university?']:
    uni_extras += el.split(', ')

barh(
    'Did you do any of the following during university?',
    'uni_extras',
    data=uni_extras)
print(df['Did you do any of the following during university?'].unique())
####################################################
# Part 2
####################################################
# df2 = pd.read_excel('part_2.xlsx')
# for col in df2.columns:
#     print(col)