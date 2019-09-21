import pandas as pd

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
for term in terms:
    if 'c' in term:
        work_terms.append(term)
    else:
        school_terms.append(term)

df = pd.read_excel('part_1.xlsx')


def clean_rent_q(rent):
    rent_str = str(rent)
    if (', CAD, monthly' == rent_str[-14:]) or (
            ', cad, monthly' == rent_str[-14:]):
        return rent_str[:-14]
    elif ', USD, monthly' == rent_str[-14:]:
        return str(1.3 * float(rent_str[:-14]))
    else:
        return rent_str


rent_q = 'How much did you pay for rent? Format as amount, currency, rate. For example: 600, CAD, monthly'
rent_qs = [term + rent_q for term in terms]
for rent_q in rent_qs:
    df[rent_q] = df[rent_q].apply(clean_rent_q)


def clean_wage_q(wage):
    wage_str = str(wage)
    if (', CAD, hourly' == wage_str[-13:]) or (
            ', cad, hourly' == wage_str[-13:]):
        return wage_str[:-13]
    elif (', USD, hourly' == wage_str[-13:]) or (
            ', usd, hourly' == wage_str[-13:]):
        return str(1.3 * float(wage_str[:-13]))
    elif (', CAD, weekly' == wage_str[-13:]) or (
            ', cad, weekly' == wage_str[-13:]):
        return str(float(wage_str[:-13]) / 37.5)
    elif (', USD, weekly' == wage_str[-13:]) or (
            ', usd, weekly' == wage_str[-13:]):
        return str(1.3 * float(wage_str[:-13]) / 37.5)
    elif (', CAD, monthly' == wage_str[-14:]) or (
            ', cad, monthly' == wage_str[-14:]):
        return str(float(wage_str[:-14]) / 4 / 37.5)
    elif (', USD, monthly' == wage_str[-14:]) or (
            ', usd, monthly' == wage_str[-14:]):
        return str(1.3 * float(wage_str[:-14]) / 4 / 37.5)
    else:
        return wage_str


wage_q = 'What was your base salary (not including benefits)? Format as "Amount, Currency, Rate". '
wage_qs = [term + wage_q for term in work_terms]
for wage_q in wage_qs:
    df[wage_q] = df[wage_q].apply(clean_wage_q)

df.to_excel('clean_part_1.xlsx')