# Analytics

import turns_3 as t3

# Deck size [monster, spell, trap].
dA=[20, 10, 10]
dB=[20, 10, 10]

# weights for using/setting spell
# Use spell on field.
wa=[0.5,0.5]
# Use spell from hand.
wb=[0.5,0.5]
# Set a spell or trap from hand to field.
wc=[0.5,0.5]

# weights for attacking
# opponent has monsters and spells or traps
wx=[0.5,0.5]
# opponent has monsters and no spell and traps
wy=[0.5,0.5]
# opponent has no monsters but spell or traps
wz=[0.5,0.5]


# data
#gameplay = t3.Game(n, dA, dB, lp, hs, r, wa, wb, wc, wx, wy, wz)
gameplay = t3.Game(10000, dA, dB, 8, 5, False, wa, wb, wc, wx, wy, wz)

# fequency of wins and losses
gameplay["LP_A"].value_counts()
gameplay["LP_B"].value_counts()

# change non-ones to zeros if not zero
# sometimes loss can have negatives
# a negative can show that you are lossing worse though
gameplay.loc[gameplay.LP_A <= 0, "LP_A"] = 0
gameplay.loc[gameplay.LP_B <= 0, "LP_B"] = 0
# make winning binomial
gameplay.loc[gameplay.LP_A >= 1, "LP_A"] = 1
gameplay.loc[gameplay.LP_B >= 1, "LP_B"] = 1

# descriptive statistics
descripitive = gameplay.describe()

# train-test split
from sklearn.model_selection import train_test_split

train_data, test_data = train_test_split(gameplay,
                                         test_size = 0.20,
                                        random_state = 42)


# GLM binomial family

import statsmodels.api as sm
from patsy import dmatrices

formula = ('LP_A ~ Turns + MgyA + MgyB + SgyA + SgyB + TgyA + TgyB + HAmr + \
           HAsr + HAtr + HBmr + HBsr + HBtr')

#Carve out the training matrices from the training data frame using the regression formula
y_train, X_train = dmatrices(formula, train_data, return_type='dataframe')
#Carve out the testing matrices from the testing data frame using the regression formula
y_test, X_test = dmatrices(formula, test_data, return_type='dataframe')


binom_model = sm.GLM(y_train, X_train, family=sm.families.Binomial())
bm_results = binom_model.fit()
bm_results.summary()

# export results.summary
with open('../Output/bm_summary.txt', 'w') as fh:
    fh.write(bm_results.summary().as_text())


# confusion matrix
import numpy as np
import pandas as pd

# Compute prediction
predicted = bm_results.predict(X_test)

# Define the cutoff
cutoff = 0.5

# Compute class predictions: y_prediction
y_prediction = np.where(predicted > cutoff, 1, 0)

# Assign actual class labels from the test sample to y_actual
y_actual = test_data["LP_A"]


# Compute and print confusion matrix using crosstab function
conf_matrix = pd.crosstab(y_actual, y_prediction,
                       rownames = ["Actual"], 
                       colnames = ["Predicted"], 
                       margins = True)
                      
# Print the confusion matrix
print(conf_matrix)

# Accuracy
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_actual, y_prediction)

print('Accuracy: %.2f' % accuracy + "%")


# odds
odds = np.exp(bm_results.params)
prob = odds / (1+odds)

# prob A wins
# v = b_0 + b_1 * x_1 + ... + b_n * x_n
# A_w = np.exp(v)/(1+np.exp(v))

# Source:
# https://towardsdatascience.com/the-binomial-regression-model-everything-you-need-to-know-5216f1a483d3

###########################################################################################


# linear regression OLS

model_lm = sm.OLS(y_train, X_train)
results_lm = model_lm.fit()
results_lm.summary()

# export results.summary
with open('../Output/lm_summary.txt', 'w') as fh:
    fh.write(results_lm.summary().as_text())


# confusion matrix
# Compute prediction
prediction = results_lm.predict(X_test)

# Define the cutoff
cutoff = 0.5

# Compute class predictions: y_prediction
y_prediction = np.where(prediction > cutoff, 1, 0)

# Assign actual class labels from the test sample to y_actual
y_actual = test_data["LP_A"]


# Compute and print confusion matrix using crosstab function
conf_matrix = pd.crosstab(y_actual, y_prediction,
                       rownames = ["Actual"], 
                       colnames = ["Predicted"], 
                       margins = True)
                      
# Print the confusion matrix
print(conf_matrix)


# Accuracy
accuracy = accuracy_score(y_actual, y_prediction)

print('Accuracy: %.2f' % accuracy + "%")


# saving dataframe to csv
# gameplay.round(4).iloc[:,2:23].head(10).to_csv('../Output/gameplay.csv', encoding='utf-8', index=False)

# descriptive statistics
#trey = X_train.describe()
#trey.round(4).to_csv('Desktop/des.csv', encoding='utf-8', index=True)

# trying still
#import matplotlib.pyplot as plt

#fig = plt.figure()

#plt.scatter(np.exp(y_actual)/(1+np.exp(y_actual)), np.exp(prediction)/(1+np.exp(y_actual)))
#plt.ylabel("Predicted")
#plt.xlabel("Actual")

#plt.show()

#fig.savefig('../Figures/scatter_1.png')