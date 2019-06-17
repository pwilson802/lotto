import requests
import bs4
from collections import Counter
import itertools
import ast

start_url = 'https://australia.national-lottery.com/oz-lotto/results-archive-'


all_results = []
for year in range(1994,2020):
    url = start_url + str(year)
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text)
    groups = soup.find_all('td')
    for group in groups:
        all_numbers = group.find_all('span', {'class' : 'result small oz-lotto-ball'})
        week_result = []
        for num in all_numbers:
            week_result.append(int(num.text))
        all_results.append(week_result)

all_results = [x for x in all_results if len(x) != 0]

all_pairs = []
for x in list(itertools.permutations(range(46),2)):
    i = sorted(x)
    if i not in all_pairs:
        all_pairs.append(i)

all_ball_count = Counter()
for balls in all_results:
    for x in balls:
        all_ball_count[x] += 1

pair_ball_count = Counter()
for balls in all_results:
    for pair in all_pairs:
        if pair[0] and pair[1] in balls:
            pair_ball_count[str(pair)] += 1

least_common_pairs = pair_ball_count.most_common()[-50:]
most_common_pairs = pair_ball_count.most_common()[:720]
least_common_numbers = all_ball_count.most_common()[-14:]

numbers = [x[0] for x in least_common_numbers]
most_common = [ast.literal_eval(x[0]) for x in most_common_pairs]
common_pairs_in_numbers = [x for x in most_common if ( (x[0] in numbers) and (x[1] in numbers) )]
option_to_remove = set([x for i in common_pairs_in_numbers for x in i])

result = [x for x in numbers if x not in option_to_remove]
