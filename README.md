# Bad Luck Metric: ESPN Fantasy Football

Automatically calculate each team's 'bad luck' in your ESPN Fantasy Football league.

The following equation, the **Bad Luck Metric**, quantifies differences in matchup quality over the course of a fantasy football season. A higher number = worse luck.

<p align="center">
  <img src="https://i.ibb.co/t4pbFDr/lagrida-latex-editor.png">
</p>

_where **n** = num. weeks_, **_Pn_** = _pts. scored in week n_, **_POn_**  _= opponent pts. in week n_, **_σn_** = _standard deviation of league scores in week n_, **_PF/A_** = total points for/against, _**bar** indicates the league average_

## Metric breakdown

The metric considers a **comparison of weekly matchup strength** through a summation of performance comparisons normalized by both the league average and the standard deviation of scores in each week. 

The Bad Luck Metric also includes a **season-long productivity index**. This is a simple ratio of **_PF + PA_**  to **_PFbar + PAbar_**  which  is maximized by good performances and good competition compared to the league average. This serves to provide more global context.

## How to use

 1. `conda env create --file requirements.txt`
 2. Change the `id_val`, `year_val`, `s2_val`, and `swid_val` in `run_evaluation.py` to your own custom values.

`id_val` = your league ID. Visit your ESPN Fantasy Football league and take the `leagueId` argument from the URL.

`year_val` = the season from which the calculation will run on.

**TO GET THE NEXT TWO VALUES, DO THE FOLLOWING:**

 - Open your ESPN Fantasy Football league on Chrome or another browser that supports 'developer' operations
 - Right-click on the page and select 'Inspect', or enter 'Inspect Elements' mode
 - Select 'Application' from the menu, then select 'Cookies' in the left sidebar
 - Use the search bar in the Inspect menu to filter for the next two values

`s2_val` = the cookie with name `espn_s2` (should be a long string)

`swid_val` = the cookie with name `SWID`  (should be in format '{XXXXXXXXX}')

3. `python3 run_evaluation.py`
