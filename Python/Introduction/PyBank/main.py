import os
import csv

# This is the starting function of the program
        
def run_program():
    filePath = os.path.join("Resources","budget_data.csv")
    listBudgetData = []         #to hold the list of the budget data

    #read the data into the budgetData dictionary list
    with open(filePath) as csvFile:
        reader = csv.DictReader(csvFile)
        prevProfitLoss = 0                           #to keep track of the previous profit/loss to compute for the profit/loss change
        currProfitLoss = 0                           #to keep track of the current profit/loss to compute for the profit/loss change
        for row in reader:
            budgDate = row["Date"]                   #budget date
            budgProfLoss = int(row["Profit/Losses"]) #profit/losses
            if(prevProfitLoss == 0):
                currProfitLoss = 0
            else:   
                currProfitLoss = budgProfLoss
            listBudgetData.append(
                {
                    "Date"              : budgDate,
                    "ProfitOrLosses"    : budgProfLoss,
                    "ProfLossChange"    : (currProfitLoss - prevProfitLoss)
                }
            )
            prevProfitLoss = budgProfLoss

    #get the list of values from the budgetData dictionary list
    listProfLossesChange = [x["ProfLossChange"] for x in listBudgetData]
    listProfLosses = [x["ProfitOrLosses"] for x in listBudgetData]

    greatestIncProfLosses = '${:,.2f}'.format(max(listProfLossesChange))
    greatestIncDate = [x["Date"] for x in listBudgetData if x["ProfLossChange"] == max(listProfLossesChange)][0]

    greatestDecProfLosses = '${:,.2f}'.format(min(listProfLossesChange))
    greatestDecDate = [x["Date"] for x in listBudgetData if x["ProfLossChange"] == min(listProfLossesChange)][0]

    totalMonths = len(listProfLosses)
    totalProfLosses = '${:,.2f}'.format(sum(listProfLosses)) 
    averageChange = '${:,.2f}'.format(sum(listProfLossesChange)/(totalMonths - 1))

    result = f"""
    Financial Analysis
    --------------------------------------------------------------------
    Total Months:   {totalMonths}
    Total:          {totalProfLosses}
    Average Change: {averageChange}
    Greatest Increase in Profits: {greatestIncDate} ({greatestIncProfLosses})
    Greatest Decrease in Profits: {greatestDecDate} ({greatestDecProfLosses})
    """

    output_result(result)
    
# This will display the results on the terminal and also save it in an output file

def output_result(result):

    print(result);
    
    filePath = os.path.join("Output","budget_results.txt")

    with open(filePath,"w") as resultFile:
        resultFile.write(result)
        resultFile.close()
    
    print(f"The above result is also saved in {filePath}")
       
# Start the program

run_program()
