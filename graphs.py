import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re

figsize = (12, 9)


def apply_styling(style_params=None):
    sns.set()
    params = {
        'axes.titlesize': 24,
        'axes.labelsize': 18,
        'xtick.labelsize': 18,
        'ytick.labelsize': 18,
        'axes.titlepad': 20,
        'axes.titlepad': 20,
        'legend.fontsize': 18
    }
    if style_params:
        params.update(style_params)
    plt.rcParams.update(params)


df1 = pd.read_excel('part_1.xlsx')
df2 = pd.read_excel('part_2.xlsx')
df = pd.merge(df1, df2, left_index=True, right_index=True)
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


def barh(col, fname, data=None, bar_order=None, title=None, style_params=None):
    if data is None:
        data = df[col]
    data = [x for x in data if not (type(x) == float and np.isnan(x))]
    c = Counter(data)
    bar_df = pd.DataFrame({'keys': list(c.keys()), 'vals': list(c.values())})
    if bar_order:
        bar_df['ii'] = [bar_order.index(x) for x in bar_df['keys']]
        bar_df = bar_df.sort_values(by='ii', ascending=True)
    else:
        bar_df = bar_df.sort_values(by='vals', ascending=True)

    labels = bar_df['keys']
    y_pos = np.arange(len(bar_df))
    plt.figure(figsize=figsize)
    apply_styling(style_params)
    plt.barh(y_pos, bar_df['vals'], align='center', color=sns.color_palette())
    plt.yticks(y_pos, labels)
    plt.gca().set_xticklabels(
        ['{:.0f}%'.format(x * 100 / len(data)) for x in plt.gca().get_xticks()])
    plt.xlabel('Percentage of Respondents')
    if title:
        plt.title(title)
    else:
        plt.title(col)
    plt.tight_layout()
    plt.savefig('graphs/' + fname + '_bar')
    plt.close()


def boxplot(cols, fname, title, xlabels, ylabel):
    boxplot_data = [df[col].dropna() for col in cols]
    plt.figure(figsize=figsize)
    apply_styling()
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
            hist=True,
            normed=False,
            bins=None,
            labels=None,
            xlims=None,
            ylims=None,
            line_labels=None,
            data=None,
            colors=None):
    plt.figure(figsize=figsize)
    apply_styling()
    if type(cols) is not list:
        cols = [cols]

    if data is None:
        data = df[cols].fillna(0)

    for idx, col in enumerate(cols):
        plot_params = {'rug': False}
        line_label = None
        if line_labels:
            plot_params['label'] = line_labels[idx]
        if len(cols) == 1:
            data = {col: data}
        if hist:
            plot_params['hist'] = True
            plot_params['hist_kws'] = {'align': 'left'}
            if normed:
                plot_params['hist_kws']['density'] = True
            plot_params['kde'] = False
            if bins is not None:
                plot_params['bins'] = bins
        else:
            plot_params['hist'] = False
            plot_params['kde'] = True
            plot_params['kde_kws'] = {'shade': True, 'linewidth': 3}

        if colors:
            plot_params['color'] = colors[idx]
        sns.distplot(data[col], **plot_params)
    if xlims:
        plt.xlim(xlims)
    if ylims:
        plt.ylim(ylims)
    if labels:
        plt.gca().set_xticklabels(labels)
    if hist and line_labels:
        plt.legend()

    if hist and not normed:
        plt.ylabel('Number of Respondents')
    else:
        plt.ylabel('Proportion of Respondents')
    plt.xlabel(title)
    plt.title(title)
    plt.tight_layout()
    plt.savefig('graphs/' + fname + '_density')
    plt.close()


def line(y_col, fname, title, data, ylims=None):
    plt.figure(figsize=figsize)
    apply_styling()
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
    plt.figure(figsize=figsize)
    apply_styling()
    plt.stackplot(
        uppercase_work_terms, list(data.values()), labels=list(data.keys()))
    plt.legend(loc='lower right')
    # plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.savefig('graphs/' + fname + '_stacked_lineplot')
    plt.close()


# plt.figure(figsize=figsize)
# apply_styling()
# plt.hist(df['Timestamp'], bins=20)
# plt.title('Timestamp')
# plt.tight_layout()
# plt.savefig('graphs/' + 'timestamp' + '_hist')
# plt.close()

# barh('What gender do you identify with?', 'gender')
# birth_years = [1991, 1992, 1994, 1995, 1996, 1997]
# barh('What year were you born in?', 'birth_year', bar_order=birth_years)
# ethnic_data = []
# for el in df['Which ethnic background(s) do you identify with?']:
#     ethnic_data += el.split(', ')
# barh(
#     'Which ethnic background(s) do you identify with?',
#     'ethnicity',
#     data=ethnic_data)
# barh('What most closely describes your religious school of thought?',
#      'religion')

# city_grow_up_data = []
# for el in df['What city did you grow up in?']:
#     if el == 'Waterloo':
#         city_grow_up_data.append('KW')
#     else:
#         city_grow_up_data.append(el)
# barh('What city did you grow up in?', 'home_town', data=city_grow_up_data)

# school_stress_qs = [
#     term + 'How stressful was this term?' for term in school_terms
# ]
# boxplot(
#     school_stress_qs,
#     'school_stress',
#     'Stress',
#     xlabels=uppercase_school_terms,
#     ylabel='Stress Level (1-10)')
# school_stress_df = pd.DataFrame({'Term': [], 'Stress Level (1-10)': []})
# for term in school_terms:
#     responses = df[term + 'How stressful was this term?']
#     c = Counter(responses)
#     school_stress_df = school_stress_df.append(
#         pd.DataFrame({
#             'Term': [term.upper()] * len(responses),
#             'Stress Level (1-10)': responses
#         }),
#         ignore_index=True)
# line(
#     y_col='Stress Level (1-10)',
#     fname='school_stress',
#     title='School Stress',
#     ylims=None,
#     data=school_stress_df)

# work_stress_qs = [term + 'How stressful was this term?' for term in work_terms]
# boxplot(
#     work_stress_qs,
#     'coop_stress',
#     'Co-op Stress',
#     xlabels=uppercase_work_terms,
#     ylabel='Stress Level (1-10)')
# work_stress_df = pd.DataFrame({'Term': [], 'Stress Level (1-10)': []})
# for term in work_terms:
#     responses = df[term + 'How stressful was this term?']
#     c = Counter(responses)
#     work_stress_df = work_stress_df.append(
#         pd.DataFrame({
#             'Term': [term.upper()] * len(responses),
#             'Stress Level (1-10)': responses
#         }),
#         ignore_index=True)
# line(
#     y_col='Stress Level (1-10)',
#     fname='coop_stress',
#     title='Co-op Stress',
#     ylims=None,
#     data=work_stress_df)

# political_labels = [' '] + ['Far Left'] + [''] * 5 + ['Far Right']
# density(
#     cols='How would you describe your political leanings?',
#     fname='political',
#     title='Political Leaning',
#     labels=political_labels,
#     xlims=(0, 8),
#     bins=np.arange(1, 7 + 2, 1))
# density(
#     'What was your entrance average from high-school (top 6 grades only)?',
#     'hs_avg',
#     'High School Entrance Average',
#     xlims=(80, 100))
# accelerated_programs = []
# for el in df[
#         'Which of the following accelerated programs, if any, did you graduate from?']:
#     accelerated_programs += el.split(', ')
# barh(
#     'Which of the following accelerated programs, if any, did you graduate from?',
#     'accelerated_programs',
#     accelerated_programs,
#     title='Which accelerated programs did you graduate from?')
# hs_extras = []
# for el in df[
#         'Which of the following extracurricular activities did you do in high school, if any?']:
#     el = el.replace(
#         'Participate in a leadership program (SHAD, build a school in Africa)',
#         'Leadership Program')
#     hs_extras += el.split(', ')
# barh(
#     'Which of the following extracurricular activities did you do in high school, if any?',
#     'hs_extras',
#     hs_extras,
#     title='High school Extracurricular Activities')

# hs_industry_data = []
# for el in df[
#         'Before starting university, what industry did you see yourself working in?']:
#     if type(el) == float:  # NaN check
#         pass
#     elif 'Manufacturing' in el:
#         hs_industry_data.append('Manufacturing')
#     elif 'Software' in el:
#         hs_industry_data.append('Software')
#     elif 'Hardware' in el:
#         hs_industry_data.append('Hardware')
#     elif 'Tech/Design' in el:
#         hs_industry_data.append('Consulting')
#     else:
#         hs_industry_data.append(el)
# barh(
#     'Before university, what industry did you see yourself working in?',
#     'hs_industry',
#     data=hs_industry_data,
#     title='Before university, what industry did you want to work in?')

# faculties_applied_to = []
# for el in df['What university faculties did you apply to?']:
#     faculties_applied_to += el.split(', ')
# faculties_applied_to = [
#     fac for fac in faculties_applied_to if fac != 'Engineering'
# ]

# barh('What other university faculties did you apply to?',
#      'faculties_applied_to', faculties_applied_to)
# incomes = [
#     '$0 - 50k', '$50 - 100k', '$100 - 150k', '$150 - 200k', '$200 - 250k',
#     '$250 - 300k', '$300k+', "Don't Know"
# ]
# incomes = [x for x in incomes]
# barh(
#     "What was your parents' combined income at the time you entered university?",
#     'household_income',
#     bar_order=incomes)

# term_avg_qs = [
#     'What was your term average in ' + term.upper() + '?'
#     for term in school_terms
# ]
# boxplot(
#     term_avg_qs,
#     fname='term_avg',
#     title='Term Average',
#     xlabels=uppercase_school_terms,
#     ylabel='Term Average')

# barh(
#     'What is the highest level of education achieved by either of your parents?',
#     'parent_education',
#     title="Parents' highest level of education")

# barh(
#     'Have either of your parents studied/worked in a STEM-related field?',
#     'parent_stem',
#     title='Have your parents worked in a STEM-related field?')
# barh('Were either of your parents born in North America?',
#      'parent_north_america')

# parent_tuition_bar_order = [
#     '81 - 100%', '61 - 80%', '41 - 60%', '21 - 40%', '0 - 20%'
# ]
# barh(
#     'Approximately how much of your total university expenses were funded by your family? ',
#     'parent_tuition',
#     title='How much of your university expenses were funded by your family?',
#     bar_order=parent_tuition_bar_order[::-1])
# debt_savings_order = [
#     'None', '0-5k', '5k-10k', '10-20k', '20-50k', '50k+', 'Prefer not to say'
# ]
# debt_savings_order.reverse()
# debt_savings_order = [x for x in debt_savings_order]
# barh(
#     'How much debt are you graduating with?',
#     'debt',
#     bar_order=debt_savings_order)
# barh(
#     'How much do you have in savings?', 'savings', bar_order=debt_savings_order)
# density(
#     "Of your 5 closest friends you've made in university, how many are in SYDE?",
#     title=
#     "Of your 5 closest friends you've made in university, how many are in SYDE?",
#     fname='syde_friends',
#     bins=np.arange(0, 5 + 2, 1))
# lecture_attendance_df = pd.DataFrame({
#     'Term': [],
#     'Percentage of Lectures Attended': []
# })
# for term in school_terms:
#     orig_vals = df[term + 'How often did you attend lectures this term?']
#     new_vals = []
#     for val in orig_vals:
#         if val == 'Almost always':
#             new_vals.append(100)
#         elif val == 'Most of the time':
#             new_vals.append(75)
#         elif val == 'About half the time':
#             new_vals.append(50)
#         elif val == 'Occasionally':
#             new_vals.append(25)
#         elif val == 'Almost never':
#             new_vals.append(0)
#         else:
#             print(val)
#     df[term + 'lecture_attendance'] = new_vals
#     lecture_attendance_df = lecture_attendance_df.append(
#         pd.DataFrame({
#             'Term': [term.upper()] * len(new_vals),
#             'Percentage of Lectures Attended': new_vals
#         }),
#         ignore_index=True)

# lecture_attendance_qs = [term + 'lecture_attendance' for term in school_terms]
# boxplot(
#     lecture_attendance_qs,
#     'lecture_attendance',
#     'Lecture Attendance',
#     xlabels=uppercase_school_terms,
#     ylabel='Percentage of Lectures Attended')

# line(
#     y_col='Percentage of Lectures Attended',
#     fname='lecture_attendance',
#     title='Lecture Attendance',
#     ylims=(0, 100),
#     data=lecture_attendance_df)

# employment_rate_df = pd.DataFrame({'Term': [], 'Employment Rate': []})
# for term in school_terms[:6]:
#     responses = df[term + 'Did you find a co-op job this term?']
#     c = Counter(responses)
#     employment_rate_df = employment_rate_df.append(
#         {
#             'Term': term.upper(),
#             'Employment Rate': c['Yes'] / len(responses)
#         },
#         ignore_index=True)
# line(
#     y_col='Employment Rate',
#     fname='employment_rate',
#     title='Co-op Employment Rate',
#     ylims=(0.95, 1.01),
#     data=employment_rate_df)

# rent_qs = [
#     term +
#     'How much did you pay for rent? Format as amount, currency, rate. For example: 600, CAD, monthly'
#     for term in terms
# ]
# boxplot(
#     rent_qs,
#     'rent',
#     'How much did you pay for rent each term?',
#     xlabels=uppercase_terms,
#     ylabel='Rent (CAD/month)')

# rent_qs = [
#     term +
#     'How much did you pay for rent? Format as amount, currency, rate. For example: 600, CAD, monthly'
#     for term in school_terms
# ]
# boxplot(
#     rent_qs,
#     'school_rent',
#     'How much did you pay for rent each school term?',
#     xlabels=uppercase_school_terms,
#     ylabel='Rent (CAD/month)')

# rent_qs = [
#     term +
#     'How much did you pay for rent? Format as amount, currency, rate. For example: 600, CAD, monthly'
#     for term in work_terms
# ]
# boxplot(
#     rent_qs,
#     'work_rent',
#     'How much did you pay for rent each work term?',
#     xlabels=uppercase_work_terms,
#     ylabel='Rent (CAD/month)')

# commute_qs = []
# for term in terms:
#     location = 'school'
#     if 'c' in term:
#         location = 'work'
#     commute_qs.append(
#         term + 'How long was your commute to ' + location + ' in minutes?')
# boxplot(
#     commute_qs,
#     'commute',
#     'Commute Time to School or Work',
#     xlabels=uppercase_terms,
#     ylabel='Commute Time (Minutes)')

# commute_qs = []
# for term in school_terms:
#     location = 'school'
#     if 'c' in term:
#         location = 'work'
#     commute_qs.append(
#         term + 'How long was your commute to ' + location + ' in minutes?')
# boxplot(
#     commute_qs,
#     'school_commute',
#     'How long was your commute to school?',
#     xlabels=uppercase_school_terms,
#     ylabel='Commute Time (Minutes)')

# commute_qs = []
# for term in work_terms:
#     location = 'school'
#     if 'c' in term:
#         location = 'work'
#     commute_qs.append(
#         term + 'How long was your commute to ' + location + ' in minutes?')
# boxplot(
#     commute_qs,
#     'work_commute',
#     'How long was your commute to work?',
#     xlabels=uppercase_work_terms,
#     ylabel='Commute Time (Minutes)')

# original_job_search_methods = [
#     'Jobmine / Waterloo Works', 'External Application / Cold Applying',
#     'Networking', 'Referral', 'Returned to an old job', 'CECA',
#     'Facebook page: HH Job Listings', 'Previous offer'
#     'SYDE Department Reached out', 'Self-employed', 'nan',
#     'returned to old company for a new position'
# ]
# job_search_methods = [
#     'Waterloo Works', 'Cold Applying', 'Networking/Referral',
#     'Previous Employer', 'Self-employed'
# ]

# job_search_method_counts = {m: [] for m in job_search_methods}
# for term in work_terms:
#     c = Counter(df[term + 'How did you find this job?'])
#     temp_dict = {m: 0 for m in job_search_methods}
#     for key, val in c.items():
#         if key in ('Jobmine / Waterloo Works', 'CECA',
#                    'SYDE Department Reached out'):
#             temp_dict['Waterloo Works'] += val
#         elif key in ('Facebook page: HH Job Listings',
#                      'External Application / Cold Applying'):
#             temp_dict['Cold Applying'] += val
#         elif key in ('Previous offer', 'Networking', 'Referral'):
#             temp_dict['Networking/Referral'] += val
#         elif key in (
#                 'returned to old company for a new position',
#                 'Returned to an old job',
#         ):
#             temp_dict['Previous Employer'] += val
#         elif key == 'Self-employed':
#             temp_dict['Self-employed'] += val
#     for k, v in temp_dict.items():
#         job_search_method_counts[k].append(v)

# stacked_line(
#     data=job_search_method_counts,
#     fname='job_search_methods',
#     title='How did you find your job?')

# feel_integrated = []
# for x in df[
#         'If you were not part of the original SYDE 2019 cohort, do you feel like the class has integrated you into the 2019 community?']:
#     if x != 'I am a part of the original SYDE 2019 cohort':
#         feel_integrated.append(x)

# barh(
#     'Do you feel the class has integrated you into the 2019 community?',
#     'feel_integrated',
#     data=feel_integrated)

# syde_friends_variant_bar_order = ['0-5', '5-10', '10-20', '20-30', '30+']
# barh(
#     "How many friends do you have in the SYDE 2019 class?",
#     'syde_friends_variant',
#     bar_order=syde_friends_variant_bar_order[::-1])

# density(
#     "Out of 8 academic terms, how many of them did you attend at least one student-organized SYDE social event?",
#     fname='syde_social',
#     title='How many terms did you attend at least one SYDE event?',
#     xlims=(0, 9),
#     bins=np.arange(0, 8 + 2, 1))

# inter_gen_syde_activites = []
# for el in df[
#         'Which of the following inter-generational SYDE activities did you participate in, if any?']:
#     # remove text between ()
#     inter_gen_syde_activites += re.sub(r'\([^()]*\)', '', el).split(', ')

# barh(
#     "inter_gen_syde_activites",
#     'inter_gen_syde_activites',
#     data=inter_gen_syde_activites,
#     title='Inter-generational SYDE activities')

# upper_year_contacts = []
# for el in df['How many upper years are you still in contact with?']:
#     if el == 0:
#         upper_year_contacts.append('0')
#     elif 1 <= el <= 4:
#         upper_year_contacts.append('1-4')
#     elif 5 <= el <= 9:
#         upper_year_contacts.append('5-9')
#     elif el > 9:
#         upper_year_contacts.append('10+')

# upper_year_contacts_order = ['0', '1-4', '5-9', '10+']
# barh(
#     'How many upper years are you still in contact with?',
#     'upper_year_contact',
#     data=upper_year_contacts,
#     bar_order=upper_year_contacts_order[::-1])

# lower_year_contacts = []
# for el in df['How many lower years are you still in contact with?']:
#     if el == 0:
#         lower_year_contacts.append('0')
#     elif 1 <= el <= 4:
#         lower_year_contacts.append('1-4')
#     elif 5 <= el <= 9:
#         lower_year_contacts.append('5-9')
#     elif el > 9:
#         lower_year_contacts.append('10+')

# lower_year_contacts_order = ['0', '1-4', '5-9', '10+']
# barh(
#     'How many lower years are you still in contact with?',
#     'lower_year_contact',
#     data=lower_year_contacts,
#     bar_order=lower_year_contacts_order[::-1])

# alum_donations = []
# for el in df['Which, if any, do you plan on donating to as an alumni?']:
#     if el in ('not sure', 'not sure yet') or 'Mostly undecided' in el:
#         continue
#     alum_donations += el.split(', ')
# for i, el in enumerate(alum_donations):
#     if el == 'Department of Systems Design Engineering':
#         alum_donations[i] = 'Systems Design Engineering'

# barh(
#     'Which do you plan on donating to as an alumni?',
#     'alum_donations',
#     data=alum_donations)

# uni_extras = []
# for el in df['Did you do any of the following during university?']:
#     uni_extras += el.split(', ')
# for i, el in enumerate(uni_extras):
#     if el == 'Participate in athletic competition at the university level (not intramurals)':
#         uni_extras[i] = 'Varsity Athletics'
# barh(
#     'Did you do any of the following during university?',
#     'uni_extras',
#     data=uni_extras)

# barh(
#     'Which of the following is the most important factor for you when considering a job/career?',
#     fname='career_factor',
#     title='For your career, what do you care about most?')

# year_from_now_data = []
# for el in df['What do you expect to be doing a year from now?']:
#     if 'Working at a company' in el:
#         year_from_now_data.append('Working at a company')
#     else:
#         year_from_now_data.append(el)

# barh(
#     'What do you expect to be doing a year from now?',
#     'year_from_now',
#     data=year_from_now_data)

# future_industry_data = []
# for el in df[
#         'Which industry best describes the company you will be working at?']:
#     if type(el) == float:  # NaN check
#         pass
#     elif 'Manufacturing' in el:
#         future_industry_data.append('Manufacturing')
#     elif 'Software' in el:
#         future_industry_data.append('Software')
#     elif 'Hardware' in el:
#         future_industry_data.append('Hardware')
#     else:
#         future_industry_data.append(el)

# barh(
#     'Which industry best describes the company you will be working at?',
#     'future_industry',
#     data=future_industry_data,
#     title='Which industry best describes your next company?')

# job_offer_dates = [
#     x.replace(',', '')
#     for x in df['When did you receive the job offer?']
#     if str(x) != 'nan'
# ]
# job_offer_dates_order = [
#     'August 2018', 'September 2018', 'October 2018', 'February 2018',
#     'December 2018', 'January 2019', 'February 2019', 'March 2019',
#     'April 2019', 'May 2019', 'June 2019'
# ]
# barh(
#     'When did you receive the job offer?',
#     'job_offer_date',
#     data=job_offer_dates,
#     bar_order=job_offer_dates_order[::-1])

# barh(
#     'Will you be working for a company you previously worked for during one of your co-ops?',
#     'previous_company',
#     data=[
#         x for x in
#         df['Will you be working for a company you previously worked for during one of your co-ops?']
#         if str(x) != 'nan'
#     ],
#     title='Will you be working for a company you interned at?')

# barh(
#     'Of those leaving, do you plan to come back to Canada?',
#     'return_to_canada',
#     data=[
#         x for x in df['Do you plan to come back to Canada?'] if str(x) != 'nan'
#     ])

# when_return_to_canada_order = [
#     'Not sure',
#     '20+ years',
#     '7-10 years',
#     '4-7 years',
#     '2-3 years',
#     '1 year',
# ]
# barh(
#     'When do you plan to return?',
#     'when_return_to_canada',
#     data=[x for x in df['When do you plan to return?'] if str(x) != 'nan'],
#     bar_order=when_return_to_canada_order)

# distant_future_industry_data = []
# for el in df['10 years from now, which industry do you hope to be working in?']:
#     if type(el) == float:  # NaN check
#         pass
#     elif 'Manufacturing' in el:
#         distant_future_industry_data.append('Manufacturing')
#     elif 'Software' in el:
#         distant_future_industry_data.append('Software')
#     elif 'Hardware' in el:
#         distant_future_industry_data.append('Hardware')
#     elif 'Tech/Design Consulting' in el:
#         distant_future_industry_data.append('Tech/Design Consulting')
#     else:
#         distant_future_industry_data.append(el)

# barh(
#     'In 10 years, which industry do you hope to work in?',
#     'distant_future_industry',
#     data=distant_future_industry_data)

# barh(
#     "10 years from now, how many people from our class do you think you'll be in touch with?",
#     'distant_future_syde_friends',
#     bar_order=['10-15', '5-10', '1-5', 0],
#     title="In 10 years, how many 2019 SYDEs will you be in touch with?")

# distant_future_education_data = []
# for el in df[
#         'In the next 10 years do you plan to pursue any of the following forms of higher education?']:
#     distant_future_education_data += el.split(',')
# for i, el in enumerate(distant_future_education_data):
#     if 'MBA' in el:
#         distant_future_education_data[i] = 'MBA'
#     elif 'Assorted' in el:
#         distant_future_education_data[i] = 'Certifications'

# barh(
#     'In the next 10 years do you plan to pursue any of the following forms of higher education?',
#     'distant_future_education',
#     data=distant_future_education_data,
#     title='In 10 years do you plan to pursue any higher education?')

# marriage_age_data = [
#     x for x in df[
#         'If you intend to get married, at what age do you expect to do so?']
#     if str(x) not in ('Not anytime soon', 'nan')
# ]
# density(
#     'If you intend to get married, at what age do you expect to do so?',
#     fname='marriage_age',
#     title='If you intend to get married, at what age do you expect to do so?',
#     data=marriage_age_data,
#     bins=np.arange(22, 30 + 2, 1))

# children_age_data = [
#     x for x in df[
#         'If you intend to have children, at what age do you expect to do so?']
#     if str(x) not in ('Not sure', 'nan')
# ]
# density(
#     'If you intend to have children, at what age do you expect to do so?',
#     fname='children_age',
#     title='If you intend to have children, at what age do you expect to do so?',
#     data=children_age_data,
#     bins=np.arange(27, 35 + 2, 1))

# barh('What sexuality do you identify with?', 'sexuality')

# drug_data = []
# for el in df[
#         'Which of the following recreational drugs did you try for the first time at university?']:
#     drug_data += el.split(', ')
# barh(
#     'Which of the following recreational drugs did you try for the first time at university?',
#     'drugs',
#     data=drug_data,
#     title='Which recreational drugs did you try for the first time?',
# )

# cheating_data = []
# for a in df['Have you ever engaged in any of the following?']:
#     s = "Unauthorized use of previous term's assignments, tests, solutions"
#     if s in a:
#         cheating_data.append("Unauthorized use of previous term's materials")
#         cheating_data += (a[:a.index(s)] + a[a.index(s) + len(s):]).split(', ')
#     else:
#         cheating_data += a.split(', ')
# cheating_data = [x for x in cheating_data if x != '']
# barh(
#     'Have you ever engaged in any of the following?',
#     'cheating',
#     data=cheating_data,
#     title='Did you engage in any forms of cheating?')

# failing_data = []
# for el in df['Have you failed a course or term in SYDE?']:
#     if el == 'Have not failed either':
#         failing_data.append('Have not failed')
#     else:
#         failing_data += el.split(', ')
# barh('Have you failed a course or term in SYDE?', 'failing', data=failing_data)

# mental_health_data = []
# for el in df[
#         'Have you experienced or been diagnosed with any of the following mental health concerns?']:
#     mental_health_data += el.split(', ')
# mental_health_data[mental_health_data.index(
#     'Impulse control and addiction disorders')] = 'Addictive disorder'
# barh(
#     'Have you experienced or been diagnosed with any of the following mental health concerns?',
#     'mental_health',
#     data=mental_health_data,
#     title='Have you experienced any mental health concerns?')

# depression_causes_data = []
# for el in df[
#         'With regards to anxiety and/or depression, what was the source(s) of distress?']:
#     if el != 'Not Applicable, I have not experienced anxiety and/or depression.':
#         depression_causes_data += el.split(', ')
# barh(
#     'With regards to anxiety and/or depression, what was the source(s) of distress?',
#     'depression_causes',
#     data=depression_causes_data,
#     title='What caused your anxiety and/or depression?')

# mental_health_support_data = []
# for el in df[
#         'Have you sought any of the following forms of mental health support?']:
#     if el == 'I did not seek any form of mental health support':
#         mental_health_support_data.append('No')
#     elif el == 'I did not seek any form of mental health support, but wish that I did':
#         mental_health_support_data.append('No, but wish that I did')
#     else:
#         mental_health_support_data += re.sub(r'\([^()]*\)', '', el).split(', ')
# for i, el in enumerate(mental_health_support_data):
#     if el == 'Professional support from non-university resources':
#         mental_health_support_data[i] = 'Professional support outside UW'
# barh(
#     'Have you sought any of the following forms of mental health support?',
#     'mental_health_support',
#     data=mental_health_support_data,
#     title='Have you sought any forms of mental health support?')

# density(
#     'How many relationships did you have during university?',
#     title='How many relationships did you have during university?',
#     fname='num_relationships',
#     xlims=(-1, 6),
#     bins=np.arange(0, 5 + 2, 1))

# job_titles = [
#     'Software', 'Product Management', 'Other', 'Analyst', 'Data Science',
#     'Hardware', 'Mechanical', 'Project Management', 'Research', 'UI/UX'
# ]

# job_title_counts = {m: [] for m in job_titles}
# for term in work_terms:
#     c = Counter(df[term + 'What was your job title?'])
#     temp_dict = {m: 0 for m in job_titles}
#     for key, val in c.items():
#         if type(key) == float:  #nan check
#             pass
#         elif key in ('QA'):
#             temp_dict['Software'] += val
#         elif key in ('Co-Founder & CTO', 'Finance', 'Consultant'):
#             temp_dict['Other'] += val
#         elif key == 'Program Management':
#             temp_dict['Project Management'] += val
#         elif key == 'Product Design':
#             temp_dict['UI/UX'] += val
#         else:
#             temp_dict[key] += val
#     for k, v in temp_dict.items():
#         job_title_counts[k].append(v)

# stacked_line(
#     data=job_title_counts,
#     fname='job_titles',
#     title='What did you do on co-op?')

# job_locations = [
#     'GTA', 'KW', 'Bay Area', 'Other Canada', 'New York',
#     'Other USA/International', 'Seattle'
# ]

# job_location_counts = {m: [] for m in job_locations}
# for term in work_terms:
#     c = Counter(df[term + 'In which city did you work?'])
#     temp_dict = {m: 0 for m in job_locations}
#     for key, val in c.items():
#         if type(key) == float:  #nan check
#             pass
#         else:
#             temp_dict[key] += val
#     for k, v in temp_dict.items():
#         job_location_counts[k].append(v)

# stacked_line(
#     data=job_location_counts,
#     fname='job_locations',
#     title='In which city did you work?')

# job_industrys = [
#     'Software', 'Academia/Research', 'Construction', 'Finance/Insurance',
#     'Government/Advocacy/Non-Profit', 'Hardware', 'Healthcare/Biotech',
#     'Consulting', 'Manufacturing', 'Other'
# ]

# job_industry_counts = {m: [] for m in job_industrys}
# for term in work_terms:
#     c = Counter(
#         df[term + 'Which industry best describes the company you worked for?'])
#     temp_dict = {m: 0 for m in job_industrys}
#     for key, val in c.items():
#         if type(key) == float:  #nan check
#             pass
#         elif 'Manufacturing' in key:
#             temp_dict['Manufacturing'] += val
#         elif 'Software' in key:
#             temp_dict['Software'] += val
#         elif 'Hardware' in key:
#             temp_dict['Hardware'] += val
#         elif 'Consulting' in key:
#             temp_dict['Consulting'] += val
#         elif key == 'Arts/Media/Publishing':
#             temp_dict['Other'] += val
#         else:
#             temp_dict[key] += val
#     for k, v in temp_dict.items():
#         job_industry_counts[k].append(v)

# stacked_line(
#     data=job_industry_counts,
#     fname='job_industrys',
#     title='Which industry best describes the company you worked for?')

# company_sizes = [
#     'Extra Large (1000+)',
#     'Large (250-1000)',
#     'Medium (50-250)',
#     'Small (10-50)',
#     'Micro (<10)',
# ]

# company_size_counts = {m: [] for m in company_sizes}
# for term in work_terms:
#     c = Counter(df[term + 'What size was the company when you worked there?'])
#     temp_dict = {m: 0 for m in company_sizes}
#     for key, val in c.items():
#         if type(key) == float:  #nan check
#             pass
#         else:
#             temp_dict[key] += val
#     for k, v in temp_dict.items():
#         company_size_counts[k].append(v)

# stacked_line(
#     data=company_size_counts,
#     fname='company_sizes',
#     title='What size was the company when you worked there?')

# coop_ratings = [
#     'Outstanding',
#     'Excellent',
#     'Very Good',
#     'Good',
#     'Satisfactory',
# ]
# coop_rating_counts = {m: [] for m in coop_ratings[::-1]}
# for term in work_terms:
#     c = Counter(df[term + 'What was your Jobmine performance rating?'])
#     temp_dict = {m: 0 for m in coop_ratings}
#     for key, val in c.items():
#         if type(key) == float:  #nan check
#             pass
#         else:
#             temp_dict[key] += val
#     for k, v in temp_dict.items():
#         coop_rating_counts[k].append(v)

# stacked_line(
#     data=coop_rating_counts,
#     fname='coop_ratings',
#     title='What was your Jobmine performance rating?')

# salary_qs = [
#     term +
#     'What was your base salary (not including benefits)? Format as "Amount, Currency, Rate". '
#     for term in work_terms
# ]
# boxplot(
#     salary_qs,
#     'coop_salary',
#     'Co-op Salary',
#     xlabels=uppercase_work_terms,
#     ylabel='CAD/hour')

# barh('Did your FYDP group consist solely of SYDE students?', 'fydp_all_syde')

# fydp_domain_data = []
# for el in df['What domain most accurately describes your FYDP?']:
#     el = el.replace(
#         'Manufacturing (automotive, aerospace, factory, production line etc)',
#         'Manufacturing')
#     el = el.replace('Software (Consumer, B2B, Ad-tech, gaming etc)', 'Software')
#     el = el.replace('Hardware (Devices, electronics etc)', 'Hardware')
#     if type(el) == float:  #nan check
#         pass
#     else:
#         fydp_domain_data += el.split(', ')

# barh(
#     'What domain most accurately describes your FYDP?',
#     'fydp_domain',
#     data=fydp_domain_data)

# barh('Are you proud of your FYDP?', 'fydp_proud')

# barh('Do you or your group plan to pursue your FYDP further beyond 4B?',
#      'fydp_future')

# syde_discovery_data = []
# for el in df['How did you find out about SYDE?']:
#     if el in ('my dad', 'Family', 'Father', 'parent (waterloo Alumnus)',
#               'Family friend', 'My cousin graduated from SYDE',
#               'Was referred/pitched it by an older friend in SYDE', 'Mother'):
#         syde_discovery_data.append('Word of mouth')
#     else:
#         syde_discovery_data.append(el)
# barh(
#     'How did you find out about SYDE?',
#     'syde_discovery',
#     data=syde_discovery_data)

# syde_join_date_order = [
#     '1A (September 2014)',
#     '1B (May 2015)',
#     '2A (January 2016)',
#     '2B (September 2016)',
#     '3A (May 2017)',
# ]
# barh(
#     'When did you join the SYDE 2019 cohort?',
#     'syde_join_date',
#     bar_order=syde_join_date_order[::-1])

# density(
#     'How many years did it take to finish your degree?',
#     title='How many years did it take to finish your degree?',
#     fname='years_to_complete',
#     bins=np.arange(5, 10 + 1, 1))

# barh(
#     'When (if at all) did you go on exchange?',
#     'exchange_date',
#     data=[
#         x for x in df['When (if at all) did you go on exchange?']
#         if x != 'Did not go on exchange'
#     ])

# barh(
#     'What exchange university did you attend?',
#     'exchange_uni',
#     data=df['If you went on exchange, what university did you attend?']
#     .dropna())

# design_course_satisfaction_bar_order = [
#     'Very satisfied',
#     'Moderately satisfied',
#     'Slightly satisfied',
#     'Neutral',
# ]
# barh(
#     'How satisfied were you with the design courses and projects?',
#     'design_course_satisfaction',
#     bar_order=design_course_satisfaction_bar_order[::-1])

# barh('If you could go back in time, would you still do SYDE?', 'syde_again')

# if_not_syde_data = []
# for el in df[
#         'If you answered "No" to the above question. What would you do instead?']:
#     if type(el) == float:
#         pass
#     elif 'Software Engineering' in el:
#         if_not_syde_data.append('Software Engineering')
#     elif 'tron' in el.lower():
#         if_not_syde_data.append('Mechatronics Engineering')
#     else:
#         if_not_syde_data.append(el)
# barh(
#     "If you wouldn't do SYDE again, what would you do?",
#     'if_not_syde',
#     data=if_not_syde_data)

# interesting_course_data = df[
#     'What the most interesting course you took?'].str.upper().tolist()
# interesting_course_data[interesting_course_data.index('SYDE348')] = 'SYDE 348'
# interesting_course_data[interesting_course_data.index('SYDE252')] = 'SYDE 252'
# barh(
#     'What the most interesting course you took?',
#     'interesting_course',
#     data=interesting_course_data)

# useful_course_data = df[
#     'What the most useful course you took?'].str.upper().tolist()
# useful_course_data[useful_course_data.index('SYDE348')] = 'SYDE 348'
# barh(
#     'What the most useful course you took?',
#     'useful_course',
#     data=useful_course_data)

# cse_data = []
# for el in df['What CSEs did you take?']:
#     letters = []
#     for course in el.upper().split(', '):
#         letters.append(
#             course[:re.search('\d', course.replace(' ', '')).start()])
#     cse_data += letters
# barh(
#     'What CSEs did you take?',
#     'cses',
#     data=cse_data,
#     style_params={
#         'ytick.labelsize': 12,
#     })

# te_data = []
# for el in df['What TEs did you take?']:
#     letters = []
#     for course in el.upper().split(', '):
#         letters.append(
#             course[:re.search('\d', course.replace(' ', '')).start()])
#     te_data += letters

# te_data[te_data.index(' SYD')] = 'SYDE'

# barh('What TEs did you take?', 'tes', data=te_data)

# cooking_labels = ['PB&J all day'] + [''] * 4 + ['3 Michelin Stars']
# density(
#     cols=[
#         'How would you rate your cooking ability before university?',
#         'How would you rate your cooking ability after university?'
#     ],
#     fname='cooking',
#     title='Cooking Ability',
#     xlims=(0, 10),
#     line_labels=['First Year', 'Final Year'],
#     labels=cooking_labels,
#     bins=None)

# fitness_labels = ['Couch Potato'] + [''] * 4 + ['Elite Athlete']
# density(
#     cols=[
#         'How would you rate your fitness level before university?',
#         'How would you rate your fitness level after university?'
#     ],
#     fname='fitness',
#     title='Fitness Level',
#     xlims=(0, 11),
#     line_labels=['First Year', 'Final Year'],
#     labels=fitness_labels,
#     bins=np.arange(1, 10 + 2, 1))

# food_establishment_data = []
# for el in df[
#         'What was your favourite food establishment on/near campus throughout the past 5 years? ']:
#     food_establishment_data += el.split(', ')
# barh(
#     'What was your favourite food establishment on/near campus?',
#     'food_establishment',
#     data=food_establishment_data,
#     title='What was your favourite restaurant?',
#     style_params={
#         'ytick.labelsize': 16,
#     })

# barh('What will be your job title?', 'future_job_title')

# barh('What city will you be working in?', 'future_work_city')

# barh('Do you consider this city to be within your hometown / region?',
#      'future_work_city_hometown')

# barh('Does your job require you to relocate outside Canada?',
#      'future_job_outside_canada')

# barh('Where in the world would you like to settle down?', 'settle_down')

# drinking_smoking_map = {
#     'Never': 1,
#     'Once or twice a term': 2,
#     'Monthly': 3,
#     'Bi-weekly': 4,
#     'Weekly': 5,
#     '2-3 times/week': 6,
#     '4-7 times/week': 7,
# }
# drinking_smoking_labels = [
#     '', 'Never', 'Once a term', 'Monthly', 'Bi-weekly', 'Weekly', '2-3/week',
#     '4-7/week'
# ]
# marijuana_data = {
#     'In your FIRST year at school, on average how often did you consume marijuana?':
#     [],
#     'In your FINAL year at school, on average how often did you consume marijuana?':
#     []
# }
# for el in df[
#         'In your FIRST year at school, on average how often did you consume marijuana?']:
#     marijuana_data[
#         'In your FIRST year at school, on average how often did you consume marijuana?'].append(
#             drinking_smoking_map[el])
# for el in df[
#         'In your FINAL year at school, on average how often did you consume marijuana?']:
#     marijuana_data[
#         'In your FINAL year at school, on average how often did you consume marijuana?'].append(
#             drinking_smoking_map[el])

# density(
#     cols=[
#         'In your FIRST year at school, on average how often did you consume marijuana?',
#         'In your FINAL year at school, on average how often did you consume marijuana?'
#     ],
#     fname='marijuana',
#     title='Marijuana Consumption',
#     xlims=(0, 8),
#     line_labels=['First Year', 'Final Year'],
#     labels=drinking_smoking_labels,
#     data=marijuana_data,
#     bins=np.arange(1, 7 + 2, 1))

# drinking_data = {
#     'In your FIRST year at school, on average how often did you drink socially?':
#     [],
#     'In your FINAL year at school, on average how often did you drink socially?':
#     []
# }
# for el in df[
#         'In your FIRST year at school, on average how often did you drink socially?']:
#     drinking_data[
#         'In your FIRST year at school, on average how often did you drink socially?'].append(
#             drinking_smoking_map[el])
# for el in df[
#         'In your FINAL year at school, on average how often did you drink socially?']:
#     drinking_data[
#         'In your FINAL year at school, on average how often did you drink socially?'].append(
#             drinking_smoking_map[el])

# density(
#     cols=[
#         'In your FIRST year at school, on average how often did you drink socially?',
#         'In your FINAL year at school, on average how often did you drink socially?'
#     ],
#     fname='drinking',
#     title='Alcohol Consumption',
#     xlims=(0, 8),
#     line_labels=['First Year', 'Final Year'],
#     labels=drinking_smoking_labels,
#     data=drinking_data,
#     bins=np.arange(1, 7 + 2, 1))

# how_meet_partners_data = []
# for el in df['How did you meet your significant others?']:
#     if type(el) == float or el in ('wasnt in a relationship',
#                                    'no significant other....'):
#         pass
#     elif el == 'Tinder':
#         how_meet_partners_data.append('Online/App')
#     else:
#         how_meet_partners_data += el.split(', ')

# barh(
#     'How did you meet your significant others?',
#     'how_meet_partners',
#     data=how_meet_partners_data)

# density(
#     'How much of your university career, in months, was spent in a relationship?',
#     title=
#     'How much of your university career, in months, was spent in a relationship?',
#     fname='total_relationship_months',
#     # xlims=(None, 60),
#     bins=10)

# barh('Did you have sex before beginning university?', 'sex_before_uni')

# barh('Did you have sex for the first time in university?', 'lost_virginity_uni')

density(
    'How many unique sexual partners have you had in university, if any?',
    fname='sexual_partners',
    title='How many unique sexual partners have you had in university, if any?',
    xlims=(-1, 31),
    bins=np.arange(0, 30 + 2, 1))

df['coop_mean_salary'] = df[[
    term +
    'What was your base salary (not including benefits)? Format as "Amount, Currency, Rate". '
    for term in work_terms
]].mean(axis=1)
df['last_3_coop_mean_salary'] = df[[
    term +
    'What was your base salary (not including benefits)? Format as "Amount, Currency, Rate". '
    for term in work_terms[-3:]
]].mean(axis=1)

print(
    df[['What gender do you identify with?', 'coop_mean_salary'
       ]].groupby('What gender do you identify with?').mean(),
    file=open("graphs/Gender vs Wage.txt", "w+"))

print(
    df[[
        "What was your parents' combined income at the time you entered university?",
        'coop_mean_salary'
    ]].groupby(
        "What was your parents' combined income at the time you entered university?"
    ).mean(),
    file=open("graphs/Parental Income vs Wage.txt", "w+"))

term_avg_qs = [
    'What was your term average in ' + term.upper() + '?'
    for term in school_terms
]
df['cumulative_average'] = df[term_avg_qs].mean(axis=1)
density(
    'cumulative_average',
    fname='cumulative_average',
    title='Cumulative Average',
    xlims=(40, 100),
    hist=False)

density(
    'coop_mean_salary',
    fname='coop_mean_salary',
    title='Mean Coop Salary (CAD/hour)',
    bins=10)

cumulative_average_bins = []
for avg in df['cumulative_average']:
    if avg < 65:
        cumulative_average_bins.append('< 65%')
    elif 65 < avg < 75:
        cumulative_average_bins.append('65% - 75%')
    elif 75 < avg < 85:
        cumulative_average_bins.append('75% - 85%')
    elif 85 < avg < 95:
        cumulative_average_bins.append('85% - 95%')
df['cumulative_average_bins'] = cumulative_average_bins

print(
    df[['cumulative_average_bins',
        'coop_mean_salary']].groupby("cumulative_average_bins").mean(),
    file=open("graphs/Marks vs Wage.txt", "w+"))

print(
    df[['Which ethnic background(s) do you identify with?', 'coop_mean_salary'
       ]].groupby('Which ethnic background(s) do you identify with?').mean(),
    file=open("graphs/Ethnicity vs Wage.txt", "w+"))

print(
    df[[
        'What gender do you identify with?',
        'How many relationships did you have during university?'
    ]].groupby('What gender do you identify with?').mean(),
    file=open("graphs/Gender vs Relationships.txt", "w+"))

print(
    df[[
        'What gender do you identify with?',
        'How many unique sexual partners have you had in university, if any?'
    ]].groupby('What gender do you identify with?').mean(),
    file=open("graphs/Gender vs Sexual Partners.txt", "w+"))

for term in school_terms:
    lecture_attendance_numerical_vals = []
    for val in df[term + 'How often did you attend lectures this term?']:
        if val == 'Almost always':
            lecture_attendance_numerical_vals.append(100)
        elif val == 'Most of the time':
            lecture_attendance_numerical_vals.append(75)
        elif val == 'About half the time':
            lecture_attendance_numerical_vals.append(50)
        elif val == 'Occasionally':
            lecture_attendance_numerical_vals.append(25)
        elif val == 'Almost never':
            lecture_attendance_numerical_vals.append(0)
    df[term +
       'How often did you attend lectures this term? (numerical)'] = lecture_attendance_numerical_vals
df['lecture_attendance_avg'] = df[[
    term + 'How often did you attend lectures this term? (numerical)'
    for term in school_terms
]].mean(axis=1)

lecture_attendance_avg_categorical = []
for el in df['lecture_attendance_avg']:
    if 0 <= el < 12.5:
        lecture_attendance_avg_categorical.append('Almost never')
    elif 12.5 <= el < 37.5:
        lecture_attendance_avg_categorical.append('Occasionally')
    elif 37.5 <= el < 62.5:
        lecture_attendance_avg_categorical.append('About half the time')
    elif 62.5 <= el < 87.5:
        lecture_attendance_avg_categorical.append('Most of the time')
    elif 87.5 <= el <= 100:
        lecture_attendance_avg_categorical.append('Almost always')
df['lecture_attendance_avg_categorical'] = lecture_attendance_avg_categorical
print(
    df[['lecture_attendance_avg_categorical', 'cumulative_average'
       ]].groupby('lecture_attendance_avg_categorical').mean(),
    file=open("graphs/Lecture Attendance vs Marks.txt", "w+"))

tc_data = []
for el in df['TC Over 1 Year']:
    if el == 0:
        continue
    tc_data.append(el)
density(
    'TC Over 1 Year',
    fname='total_compensation',
    title='Total Annual Compensation',
    data=tc_data,
    bins=10)

gender_vs_wage_data = {}
gender_vs_wage_data['Male'] = df[df['What gender do you identify with?'] ==
                                 'Male']['coop_mean_salary']
gender_vs_wage_data['Female'] = df[df['What gender do you identify with?'] ==
                                   'Female']['coop_mean_salary']
density(
    cols=['Male', 'Female'],
    fname='gender_vs_wage',
    title='Mean co-op salary separated by gender',
    data=gender_vs_wage_data,
    line_labels=['Male', 'Female'],
    bins=np.arange(19, 47 + 2, 2),
    normed=True,
    colors=[sns.color_palette('bright')[0],
            sns.color_palette('bright')[6]])

gender_vs_relationships_data = {}
gender_vs_relationships_data['Male'] = df[df[
    'What gender do you identify with?'] == 'Male'][
        'How many relationships did you have during university?']
gender_vs_relationships_data['Female'] = df[df[
    'What gender do you identify with?'] == 'Female'][
        'How many relationships did you have during university?']
density(
    cols=['Male', 'Female'],
    fname='gender_vs_relationships',
    title='Number of relationships separated by gender',
    data=gender_vs_relationships_data,
    line_labels=['Male', 'Female'],
    bins=np.arange(0, 6 + 2, 1),
    normed=True,
    colors=[sns.color_palette('bright')[0],
            sns.color_palette('bright')[6]])

gender_vs_sexual_partners_data = {}
gender_vs_sexual_partners_data['Male'] = df[df[
    'What gender do you identify with?'] == 'Male'][
        'How many unique sexual partners have you had in university, if any?']
gender_vs_sexual_partners_data['Female'] = df[df[
    'What gender do you identify with?'] == 'Female'][
        'How many unique sexual partners have you had in university, if any?']
density(
    cols=['Male', 'Female'],
    fname='gender_vs_sexual_partners',
    title='Number of sexual partners separated by gender',
    data=gender_vs_sexual_partners_data,
    line_labels=['Male', 'Female'],
    bins=np.arange(0, 30 + 2, 1),
    normed=True,
    colors=[sns.color_palette('bright')[0],
            sns.color_palette('bright')[6]])

print(df['coop_mean_salary'].min(), df['coop_mean_salary'].max())