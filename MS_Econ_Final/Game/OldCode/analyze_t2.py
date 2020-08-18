# analytics

import turns_2 as t2

# data
gameplay = t2.Game2(1000)

# fequency of wins and losses
gameplay["LP_A"].value_counts()
gameplay["LP_B"].value_counts()

# change non-ones to zeros if not zero
# sometimes loss can have negatives
# a negative can show that you are lossing worse though
gameplay.loc[gameplay.LP_A != 1, "LP_A"] = 0
gameplay.loc[gameplay.LP_B != 1, "LP_B"] = 0

import matplotlib.pyplot as plt
import numpy as np

# fig = plt.figure()

plt.hist(gameplay["Turns"], bins=10, color = 'red', alpha=0.5)
plt.hist(np.log(gameplay["Turns"]), bins=10, color = 'blue', alpha=0.5)

plt.show()

# fig.savefig('...')

# descriptive statistics
descripitive = gameplay.describe()


# binary logistic regression

# train-test split
from sklearn.model_selection import train_test_split

train_data, test_data = train_test_split(gameplay,
                                         test_size = 0.20,
                                         random_state = 42)

# logistic regression
from statsmodels.formula.api import logit 

formula = ('LP_A ~ Turns + mgyA + mgyB + sgyA + sgyB + tgyA + tgyB + A5cards + B5cards')

model = logit(formula = formula, data = train_data).fit()

model.summary()


# Odds Ratio -> marginal effect
AME = model.get_margeff(at='overall', method='dydx')
print(AME.summary())


# confusion matrix
import numpy as np
import pandas as pd

# Compute prediction
prediction = model.predict(exog = test_data)

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
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_actual, y_prediction)

print('Accuracy: %.2f' % accuracy + "%")



# Source: https://towardsdatascience.com/binary-logistic-regression-using-python-research-oriented-modelling-and-interpretation-49b025f1b510



# GLM binomial family

import statsmodels.api as sm
from statsmodels.formula.api import glm

formula = ('LP_A ~ Turns + mgyA + mgyB + sgyA + sgyB + tgyA + tgyB')

model_g = glm(formula = formula, data = train_data, family=sm.families.Binomial()).fit()

model_g.summary()



# linear regression OLS
from statsmodels.formula.api import ols

formula = ('LP_A ~ Turns + mgyA + mgyB + sgyA + sgyB + tgyA + tgyB + A5cards + B5cards ')

model_l = ols(formula = formula, data = train_data).fit()

model_l.summary()


