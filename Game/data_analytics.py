import currnent_state as cs 
import gameplay_turns as t4
import numpy as np
import pandas as pd

# Deck size [monster, spell, trap].
dA=[20,10,10]
dB=[20,10,10]

# nothing on field to start
fA = [0,0,0]
fB = [0,0]

#cs.Game(n, dA, dB, r, lpA, lpB, hA, hsB, t, fA, fB, stratA, stratB, games)

# data for adjustment function
games = pd.DataFrame()
# cannot have 100% not attack in infinite deck or else never end
for x in [x/10 for x in range(0, 7)]:
    for y in [x/10 for x in range(0, 7)]:
        for z in [x/10 for x in range(0, 7)]:
            games = games.append(t4.Game(100,dA,dB,False,1,1,5,5,0,fA,fB,
                                         [0,1],[0,1],[0,1],
                                         [x,1-x], [y,1-y], [z,1-z]))

# change non-ones to zeros if not zero
# sometimes loss can have negatives
# a negative can show that you are lossing worse though
games.loc[games.LP_A <= 0, "LP_A"] = 0
# make winning binomial
games.loc[games.LP_A >= 1, "LP_A"] = 1
    
# train-test split
from sklearn.model_selection import train_test_split

train_dataa, test_dataa = train_test_split(games,test_size = 0.20,random_state = 42)

# GLM binomial family

from patsy import dmatrices

formula = ('LP_A ~ FirstA + HAMon + HASpell + HATrap + PrAwMST + PrAwM + PrAwST')
#Carve out the training matrices from the training data frame using the regression formula
y_traina, X_traina = dmatrices(formula, train_dataa, return_type='dataframe')
#Carve out the testing matrices from the testing data frame using the regression formula
y_testa, X_testa = dmatrices(formula, test_dataa, return_type='dataframe')
      
import statsmodels.api as sm
binom_model = sm.GLM(y_traina, X_traina, family=sm.families.Binomial())
bm_results = binom_model.fit()
#bm_results.summary()

# make a nice table
from statsmodels.iolib.summary2 import summary_col
# summary_col([bm_results],stars=True,float_format='%0.3f')

# export table as tex file
with open('../Output/bm_summary_table.tex', 'w') as fh:
    fh.write(summary_col([bm_results],stars=True,float_format='%0.3f',model_names=['Dependent Variable: \n win (1) or lose (0)'],
                         info_dict={'N':lambda x: "{0:d}".format(int(x.nobs))}).as_latex().replace('\caption{}', '\caption{Logistic Model: Starting State}', 1))

##################################################################################

# data for comparing strategies
gametest = cs.Game(200, dA, dB, False, 1, 1, 5, 5, 0, 
                   fA, fB, 'always', 'always', bm_results)
gametest = gametest.append(cs.Game(200, dA, dB, False, 1, 1, 5, 5, 0, 
                                   fA, fB, 'half', 'always', bm_results))
gametest = gametest.append(cs.Game(200, dA, dB, False, 1, 1, 5, 5, 0, 
                                   fA, fB, 'always', 'half', bm_results))
gametest = gametest.append(cs.Game(200, dA, dB, False, 1, 1, 5, 5, 0, 
                                   fA, fB, 'half', 'half', bm_results))
# ADP doesnt work yet
gametest = gametest.append(cs.Game(200, dA, dB, False, 1, 1, 5, 5, 0, 
                                   fA, fB, 'ADP', 'always', bm_results))
gametest = gametest.append(cs.Game(200, dA, dB, False, 1, 1, 5, 5, 0, 
                                   fA, fB, 'ADP', 'half', bm_results))

# test
#gamet = cs.Game(100, dA, dB, False, 1, 1, 5, 5, 0,
#                fA, fB, 'ADP', 'always', games, bm_results)

# gametest['LP_A'].value_counts()
# gametest['LP_B'].value_counts()
# gametest.loc[gametest.LP_A == 1, "AsADP"].value_counts()

# instead of redoing the games for max weight func have a reserve to pick from.
# filter by current state
gametest.loc[gametest.LP_A <= 0, "LP_A"] = 0
# make winning binomial
gametest.loc[gametest.LP_A >= 1, "LP_A"] = 1


# train-test split
from sklearn.model_selection import train_test_split

train_data, test_data = train_test_split(gametest,
                                         test_size = 0.20,
                                        random_state = 42)


# GLM binomial family
formula = ('LP_A ~ FirstA + AsHalf + AsAlways + AsADP')

#Carve out the training matrices from the training data frame using the regression formula
y_train2, X_train2 = dmatrices(formula, train_data, return_type='dataframe')
#Carve out the testing matrices from the testing data frame using the regression formula
y_test2, X_test2 = dmatrices(formula, test_data, return_type='dataframe')


binom_model2 = sm.GLM(y_train2, X_train2, family=sm.families.Binomial())
bm_results2 = binom_model2.fit()
#bm_results2.summary()


# export results.summary as .txt
#with open('../Output/bm_summary.txt', 'w') as fh:
#    fh.write(bm_results2.summary().as_text())

# make a nice table
# summary_col([bm_results2],stars=True,float_format='%0.3f')

# export table as tex file
with open('../Output/bm_summary_table2.tex', 'w') as fh:
    fh.write(summary_col([bm_results2],stars=True,float_format='%0.3f',model_names=['Dependent Variable: \n win (1) or lose (0)'],
                         info_dict={'N':lambda x: "{0:d}".format(int(x.nobs))}).as_latex().replace('\caption{}', '\caption{Logistic Model: Evaluate Strategies}', 1))

# prob of winning
# v = sum(bm_results.params * [1,0.5,0.5,0.5])
# odds = np.exp(bm_results.params)
# prob = odds / (1+odds)

# prob A wins
# v = b_0 + b_1 * x_1 + ... + b_n * x_n
# A_w = np.exp(v)/(1+np.exp(v))

pA_w = pd.DataFrame()
for a in [x for x in range(0, 2)]:
    for b in [x for x in range(0, 2)]:
        for c in [x for x in range(0, 2)]:
            if a + b + c == 1: # must pick only one
                v = sum(bm_results2.params * [1,1,a,b,c])
                pA_w = pA_w.append({'ProbAwins':np.exp(v)/(1+np.exp(v)),
                                    'Weights':[a,b,c]},ignore_index=True)
            else:
                pass

 
max_w = pA_w.loc[pA_w['ProbAwins'].idxmax()]



# confusion matrix
# Compute prediction
predicted = bm_results2.predict(X_test2)

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
#print(conf_matrix)

# Accuracy
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_actual, y_prediction)

#print('Accuracy: %.2f' % accuracy + "%")



# investigating the weights -- did not end up useful

#formula = ('LP_A ~ FirstA + PrAwMST + PrAwM + PrAwST')

#Carve out the training matrices from the training data frame using the regression formula
#y_train3, X_train3 = dmatrices(formula, train_data, return_type='dataframe')
#Carve out the testing matrices from the testing data frame using the regression formula
#y_test3, X_test3 = dmatrices(formula, test_data, return_type='dataframe')


#binom_model3 = sm.GLM(y_train3, X_train3, family=sm.families.Binomial())
#bm_results3 = binom_model3.fit()
#bm_results3.summary()


# make a nice table
#summary_col([bm_results3],stars=True,float_format='%0.3f')

# export table as tex file
#with open('../Output/bm_summary_table3.tex', 'w') as fh:
#    fh.write(summary_col([bm_results3],stars=True,float_format='%0.3f',model_names=['Dependent Variable: \n win (1) or lose (0)'],
#                         info_dict={'N':lambda x: "{0:d}".format(int(x.nobs))}).as_latex().replace('\caption{}', '\caption{Logistic Model: Evaluate Weights}', 1))


#pA_w = pd.DataFrame()
#for x in [x/10 for x in range(0, 11)]:
#    for y in [x/10 for x in range(0, 11)]:
#        for z in [x/10 for x in range(0, 11)]:
#            if x + y + z > 0:
#                v = sum(bm_results3.params * [1,1,x,y,z])
#                pA_w = pA_w.append({'ProbAwins':np.exp(v)/(1+np.exp(v)),
#                                    'Weights':[x,y,z]},ignore_index=True)

 
#max_w = pA_w.loc[pA_w['ProbAwins'].idxmax()]



# saving dataframe to csv
games.round(4).iloc[:,1:9].head(10).to_latex('../Output/game1.tex',index=False)
gametest.round(4).iloc[:,1:12].head(10).to_latex('../Output/game2.tex',index=False)

