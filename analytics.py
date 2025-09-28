import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import os

os.makedirs("charts", exist_ok=True)
conn = sqlite3.connect("soccer.db")

# Plotly scatter with slider
query0 = """
SELECT L.name AS league_name,
       substr(M.date, 1, 4) AS year,
       COUNT(M.id) AS matches_count,
       SUM(M.home_team_goal + M.away_team_goal) AS total_goals,
       AVG(M.home_team_goal + M.away_team_goal) AS avg_goals
FROM Match M
JOIN League L ON M.league_id = L.id
WHERE substr(M.date, 1, 4) IS NOT NULL
GROUP BY L.name, year
ORDER BY year;
"""
df0 = pd.read_sql(query0, conn)

fig = px.scatter(
    df0,
    x="matches_count",
    y="total_goals",
    size="avg_goals",
    color="league_name",
    animation_frame="year",
    hover_name="league_name",
    size_max=40,
    title="League Goals vs Matches Over Time"
)
fig.show()

# Pie chart
query1 = """
SELECT L.name AS league_name, COUNT(M.id) AS total_matches
FROM Match M
JOIN League L ON M.league_id = L.id
GROUP BY L.name;
"""
df1 = pd.read_sql(query1, conn)
df1.set_index("league_name")["total_matches"].plot.pie(autopct="%1.1f%%")
plt.title("Distribution of Matches by League")
plt.ylabel("")
plt.savefig("charts/pie_matches_league.png")
plt.close()
print(f"Pie chart saved: {len(df1)} rows -> charts/pie_matches_league.png")

# Bar chart
query2 = """
SELECT L.name AS league_name,
       AVG(M.home_team_goal) AS avg_home_goals,
       AVG(M.away_team_goal) AS avg_away_goals
FROM Match M
JOIN League L ON M.league_id = L.id
GROUP BY L.name;
"""
df2 = pd.read_sql(query2, conn)
df2.set_index("league_name")[["avg_home_goals", "avg_away_goals"]].plot(kind="bar", figsize=(10, 6))
plt.title("Average Home vs Away Goals per League")
plt.savefig("charts/bar_goals_league.png")
plt.close()
print(f"Bar chart saved: {len(df2)} rows -> charts/bar_goals_league.png")
# Horizontal bar chart
query3 = """
SELECT T.team_long_name AS team_name,
       SUM(CASE WHEN M.home_team_api_id = T.team_api_id THEN M.home_team_goal
                WHEN M.away_team_api_id = T.team_api_id THEN M.away_team_goal
           END) AS total_goals
FROM Team T
JOIN Match M ON T.team_api_id = M.home_team_api_id OR T.team_api_id = M.away_team_api_id
GROUP BY T.team_long_name
ORDER BY total_goals DESC
LIMIT 15;
"""
df3 = pd.read_sql(query3, conn)
df3.set_index("team_name")["total_goals"].plot(kind="barh", figsize=(10, 8))
plt.title("Top 15 Teams by Total Goals Scored")
plt.xlabel("Total Goals")
plt.ylabel("Team")
plt.tight_layout()
plt.savefig("charts/hbar_top_teams_goals.png")
plt.close()
print(f"Horizontal bar chart saved: {len(df3)} rows -> charts/hbar_top_teams_goals.png")

# Line chart
query4 = """
SELECT strftime('%Y', M.date) AS year,
       AVG(M.home_team_goal + M.away_team_goal) AS avg_goals
FROM Match M
WHERE year IS NOT NULL
GROUP BY year
ORDER BY year;
"""
df4 = pd.read_sql(query4, conn)
df4.plot(x="year", y="avg_goals", kind="line", marker="o", figsize=(10, 6))
plt.title("Average Goals per Match Over Time")
plt.savefig("charts/line_goals_trend.png")
plt.close()
print(f"Line chart saved: {len(df4)} rows -> charts/line_goals_trend.png")

# Histogram
query5 = """
SELECT (strftime('%Y', '2016-01-01') - strftime('%Y', P.birthday)) AS age
FROM Player P
WHERE age IS NOT NULL;
"""
df5 = pd.read_sql(query5, conn)
df5["age"].astype(float).plot.hist(bins=20)
plt.title("Distribution of Player Ages")
plt.xlabel("Age")
plt.ylabel("Count")
plt.savefig("charts/hist_player_ages.png")
plt.close()
print(f"Histogram saved: {len(df5)} rows -> charts/hist_player_ages.png")

# Scatter plot
query6 = """
SELECT PA.overall_rating, PA.potential
FROM Player_Attributes PA
WHERE overall_rating IS NOT NULL AND potential IS NOT NULL
LIMIT 1000;
"""
df6 = pd.read_sql(query6, conn)
df6.plot.scatter(x="overall_rating", y="potential", alpha=0.5, figsize=(8, 6))
plt.title("Player Overall Rating vs Potential")
plt.xlabel("Overall Rating")
plt.ylabel("Potential")
plt.savefig("charts/scatter_rating_potential.png")
plt.close()
print(f"Scatter plot saved: {len(df6)} rows -> charts/scatter_rating_potential.png")

conn.close()
