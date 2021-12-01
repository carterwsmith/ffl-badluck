from statistics import stdev
from espn_api.football import League
import numpy as np
from scipy.stats import norm
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sb

#init league with ID, year, cookies (see readme)
id_val = XXXXX
year_val = XXXX
s2_val = 'XXXXX'
swid_val = 'XXXXX'

league = League(league_id=id_val, year=year_val, espn_s2=s2_val, swid=swid_val)
teams = league.teams
metrics = []

WEEKS_COMPLETED = league.current_week - 1
if WEEKS_COMPLETED <= 0:
    raise ValueError('No weeks have completed.')

league_pfs = []
league_pas = []

league_weekly_scores = [[0] * len(teams) for x in range(WEEKS_COMPLETED)]
league_weekly_avg = []
league_weekly_std_dev = []

for i, team in enumerate(teams):
    #add team pf/pa to list
    league_pfs.append(team.points_for)
    league_pas.append(team.points_against)

    #add team scores to weekly score list
    for wk in range(WEEKS_COMPLETED):
        league_weekly_scores[wk][i] = team.scores[wk]

#compute league pf / pa averages
league_pf_avg = sum(league_pfs) / len(league_pfs)
league_pa_avg = sum(league_pas) / len(league_pas)

#compute avg weekly score, std dev
for i in range(WEEKS_COMPLETED):
    league_weekly_avg.append(sum(league_weekly_scores[i]) / len(league_weekly_scores[i]))
    league_weekly_std_dev.append(stdev(league_weekly_scores[i]))

#compute metric for each team
for i in range(len(teams)):
    metric = 0
    team = teams[i]

    team_avg = sum(team.scores) / len(team.scores)
    team_dev = stdev(team.scores)

    perf_comparison_sum = 0
    for i in range(WEEKS_COMPLETED):
        opp_avg = sum(team.schedule[i].scores) / len(team.schedule[i].scores)
        opp_dev = stdev(team.schedule[i].scores)

        perf = (1/league_weekly_std_dev[i])*((league_weekly_avg[i])/(team.scores[i]))
        opp_perf = (1/league_weekly_std_dev[i])*((team.schedule[i].scores[i])/(league_weekly_avg[i]))
        perf_comparison_sum += (opp_perf / perf) - 1

    prod_coeff = (team.points_for + team.points_against) / (league_pf_avg + league_pa_avg)

    metric = perf_comparison_sum * prod_coeff
    wl_format = '(' + str(team.wins) + '-' + str(team.losses) + ')'
    metrics.append((team.team_name, wl_format, metric))

metrics.sort(reverse=True, key=lambda x : x[2])

#calculate norm curve
res = np.fromiter((entry[2] for entry in metrics), float)
mean = np.mean(res)
std = np.std(res)

#print normalized percentages
for entry in metrics:
    prob = round(norm(loc=mean, scale=std).cdf(entry[2]), 2)
    out_ptile = str(prob)[-2:] if str(prob)[-2] != 0 and str(prob)[-2] != '.' else '100' if str(prob)[-3] == '1' else str(prob)[-1] + '0'
    print(entry[0], entry[1], 'is in the', out_ptile, 'percentile of bad luck.')

#create and display graph
y_pos = np.arange(len(metrics))

matplotlib.rc('ytick', labelsize=7) 
fig, ax = plt.subplots()

labels = [entry[0] for entry in metrics]

hbars = ax.barh(y_pos, res, align='center')
ax.set_yticks(y_pos)
ax.set_yticklabels(labels)
ax.invert_yaxis()
ax.set_xlabel('Bad Luck Metric')
ax.set_title('FFL matchup inequalities, ' + str(year_val))

#add formatted labels
ax.bar_label(hbars, fmt='%.2f')
ax.set_xlim(left=-4, right=4) #typical bounds, can be changed if necessary

plt.show()
