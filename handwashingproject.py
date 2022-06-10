import pandas as pd
import matplotlib.pyplot as plt

#Our data came in a messed up txt file so had to load it into data frame and the 
#convert it to csv maybe converting to csv was uncesisary

#convert text file to csv

#since we did this originally we don't need to keep this since we got the clean csv 
#will keep it in but commented for refrence though 

#dataframe1 = pd.read_csv("raw.txt")

#Convert that data frame to a csv
#dataframe1.to_csv('yearlyDeaths.csv', 
                  #index = None)

#get the data file and read it into a df variable using pandas 
yearly = pd.read_csv("yearlyDeaths.csv")

#print(yearly)

#adding a proportional_deaths column that is data from deaths / births
#meaning each corrposonding index divides by each one for example the first 'porportinal death'
# = 237/3036 i.e the deaths divided by the births at the year 1841 and so on for each year

yearly['proportion_deaths'] = yearly['deaths'] / yearly['births']
print(yearly)




#create a variable clinic1 and clinic2 by reading from the clinic column and essentially
#sorting by if the item in the clinic column is 'clinic 1' or 'clinic 2'
clinic_1 = yearly[yearly ['clinic'] == 'clinic 1']
clinic_2 = yearly[yearly ['clinic'] == 'clinic 2']

# x axis is 'year' y is proportianl deaths
# the label is the label of the label of the physical lines (the actual graph itself)
#as you can see a variable can take multiple 'plots' in our case both clinic one and clinic 2
#we are essentially graphing the proprtional deaths at each clinic this is SUPER COOL

ax = clinic_1.plot(x="year", y="proportion_deaths", label="Clinic 1")
clinic_2.plot(x="year", y="proportion_deaths", label="Clinic 2", ax=ax, xlabel = 'pasta', ylabel="Proportion deaths")

#ax - ax means it's just part of the same graph without it they would both be graphed seperatley 
#label is the label of the line. Without label it would default to the Y value 
#above i changed the x label to pasta it is obviously supposed to be dates just wanted to fuck around
#The x label will always default to the name entered in x='whatever' but y will not for some reason
#it will just stay blank


#now lets load in the monthly data set and do the same thing we did with the first fucked
#up data set that was originally in a txt file 

#dataframe2 = pd.read_csv("raw2.txt")

#dataframe2.to_csv('monthlyDeaths.csv', 
                  #index = None)

#this is essentially a copy of the above section the only difference being that 
#we had to to use parse_dates which is GOOD TO KNOW 

#get the data file and read it into a df variable using pandas 
monthly = pd.read_csv("monthlyDeaths.csv", parse_dates=['date'])

monthly["proportion_deaths"] = monthly["deaths"] / monthly["births"]
print(monthly.head())

#we are showing the extreme fall off in porportional deaths when hand washing became a thing check out
#the seconf graph if you fotgot just how extreme it is 
ax = monthly.plot(x="date", y="proportion_deaths", ylabel="Proportion deaths")
#plt.show()


#now lets create a graph using monthly for before and after handwashing 

#date handwashing began
handwashing_start = pd.to_datetime('1847-06-01')

#create data with everything before handwashing
before_washing = monthly[monthly["date"] < handwashing_start]

#everything after and including handwashing 
after_washing = monthly[monthly["date"] >= handwashing_start]

#standard plot 
ax = before_washing.plot(x="date", y="proportion_deaths",
                         label="Before handwashing")
#ax = ax so that we can combine it in the same graph
after_washing.plot(x="date", y="proportion_deaths",
                   label="After handwashing", ax=ax, ylabel="Proportion deaths")

plt.show()

# Difference in mean monthly proportion of deaths due to handwashing
before_proportion = before_washing['proportion_deaths']
after_proportion = after_washing['proportion_deaths']
mean_diff = after_proportion.mean() - before_proportion.mean()



# A bootstrap analysis of the reduction of deaths due to handwashing
boot_mean_diff = []
for i in range(3000):
    boot_before = before_proportion.sample(frac=1, replace=True)
    boot_after = after_proportion.sample(frac=1, replace=True)
    boot_mean_diff.append( boot_after.mean() - boot_before.mean() )

# Calculating a 95% confidence interval from boot_mean_diff 
confidence_interval = pd.Series(boot_mean_diff).quantile([0.025, 0.975])
confidence_interval
