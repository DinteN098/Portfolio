import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

#opening csv file with pandas
mpg = pd.read_csv("./mpg.csv")

#removing all cars that have missing values form data
mpg = mpg.dropna()

#reshapes the array into a 2d array with one column and an unknown number of rows
x = mpg[["displacement"]].values.reshape(-1, 1) 
y = mpg[["horsepower"]].values.reshape(-1,1)

#fit a least square regression mode
linModel = LinearRegression()
linModel.fit(x ,y)
yPredicted = linModel.predict(x)

#graph title
plt.title("Linear Regression Test")

#labels
plt.xlabel("Displacement")
plt.ylabel("Horsepower")

#scatter plot styles for (displacement) and (horsepower)
plt.scatter(x, y)

#plotting the line of regression
plt.plot(x, yPredicted)

#plotting the residual
for i in range(len(x)):
    #here's where the location where the residual line will go
    plt.plot([x[i], x[i]], [y[i], yPredicted[i]], color="gray", linewidth=1)

    intercept = linModel.intercept_
    slope = linModel.coef_

    #formula being used to predict values
    print(f"y = {slope[0][0]}x + {intercept[0]}")

    #adding the x values that I would like to predict
    query1 = np.array([189]).reshape(1,1)
    predict1 = linModel.predict(query1)

    query2 = np.array([500]).reshape(1,1)
    predict2 = linModel.predict(query2)

    query3 = np.array([200]).reshape(1,1)
    predict3 = linModel.predict(query3)

    #plotting the predicted values
    plt.scatter(query1, predict1, color='red')
    plt.scatter(query2, predict2, color='red')
    plt.scatter(query3, predict3, color='red')

    #showing the graph with all the information
    plt.show()