# Graph for Matching Pennies
# make sure no color

import original_MP as mp
import matplotlib.pyplot as plt

game_mp = mp.Game(6000)

fig = plt.figure(figsize=(12,4))

plt.scatter(game_mp["Turns"], game_mp["WeightA_heads"], marker='x', 
            color='grey', label="PlayerA")
plt.scatter(game_mp["Turns"], game_mp["WeightB_heads"], marker='o',
            color='black', label="PlayerB")
plt.axhline(y=0.5, color="black", linestyle="-")
plt.ylabel("Probability of Picking Heads")
plt.xlabel("Number of Turns")
plt.legend(loc="lower right")

# plt.show()

fig.savefig('../Figures/scatter_1.png')

