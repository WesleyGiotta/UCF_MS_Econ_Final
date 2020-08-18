# Graphs
import matplotlib.pyplot as plt
import pandas as pd

fixed = pd.DataFrame()
for play in range(0,1000):
    fixed = fixed.append(Game(1000, [0.2, 0.6, 0.2], [0.4, 0.5, 0.1]))
# reset the index
fixed = fixed.reset_index()
# delete old index
fixed = fixed.drop(columns=['index'])

# histogram of all the plays
fig = plt.figure()
plt.hist(fixed['ScoreA'], bins=30)
plt.hist(fixed['ScoreB'], bins=30, color="red", alpha=0.5)
plt.show()
fig.savefig('./Desktop/Yugioh_final/Presentation_7_3/Pictures/hist_1.png')



fixed = pd.DataFrame()
for play in range(0,1000):
    fixed = fixed.append(Game(1000, [1/3, 1/3, 1/3], [1/3, 1/3, 1/3]))
# reset the index
fixed = fixed.reset_index()
# delete old index
fixed = fixed.drop(columns=['index'])

# histogram of all the plays
fig = plt.figure()
plt.hist(fixed['ScoreA'], bins=30, label="Player A")
plt.hist(fixed['ScoreB'], bins=30, color="red", alpha=0.5, label="Player B")
plt.xlabel("Total Score from 1000 Rounds")
plt.legend(loc="upper right")
plt.show()
fig.savefig('./Desktop/Yugioh_final/Presentation_7_3/Pictures/hist_2.png')



fixed = pd.DataFrame()
for play in range(0,1000):
    fixed = fixed.append(Game(1000, [0.4, 0.5, 0.1], [0.2, 0.6, 0.2]))
# reset the index
fixed = fixed.reset_index()
# delete old index
fixed = fixed.drop(columns=['index'])

# histogram of all the plays
fig = plt.figure()
plt.hist(fixed['ScoreA'], bins=30)
plt.hist(fixed['ScoreB'], bins=30, color="red", alpha=0.5)
plt.show()
fig.savefig('./Desktop/Yugioh_final/Presentation_7_3/Pictures/hist_3.png')


# maybe try a box plot for each weight distribution
# https://seaborn.pydata.org/tutorial/categorical.html



# saving dataframe to csv
fixed = fixed.drop(fixed.columns[[3,4,5,6,7,8]], axis=1, inplace=True)
fixed.head(10).to_csv('./Desktop/Yugioh_final/Appendix/csv/head_rps.csv', encoding='utf-8', index=False)

