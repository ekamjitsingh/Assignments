import os
import csv
import collections

# This is the starting function of the program
def run_program():
    filePath = os.path.join("Resources","election_data.csv")
    listElecData = []         #to hold the list of the election data
    
    #read the data into the listElecData dictionary list
    with open(filePath) as csvFile:
        reader = csv.DictReader(csvFile)
    
        for row in reader:
            voterID = row["Voter ID"] 
            county = row["County"] 
            candidate = row["Candidate"]
            listElecData.append(
                {
                    "VoterID"   : voterID,
                    "County"    : candidate,
                    "Candidate" : candidate
                }
            )
 
    #set election summary results
    elecSummary = collections.Counter([d['Candidate'] for d in listElecData])    
    totalVotes = sum(elecSummary.values())
    winner = max(elecSummary, key=elecSummary.get)
    
    #set election result text
    result = f"""
    Election Results
    -------------------------------------------------
    Total Votes : {totalVotes}
    -------------------------------------------------
    
    """
    
    #iterate through the election summary counter
    for elem in elecSummary:    
        result = result + f"{elem} :  {'{:.2%}'.format(elecSummary[elem]/totalVotes)} ({elecSummary[elem]})\n    "
  
    result = result + f"""
    -------------------------------------------------
    Winner: {winner}
    -------------------------------------------------    
    """
    
    output_result(result)

# This will display the results on the terminal and also export it in an output file
   
def output_result(result):

    print(result);
    
    filePath = os.path.join("Output","election_results.txt")

    with open(filePath,"w") as resultFile:
        resultFile.write(result)
        resultFile.close()
    
    print(f"The above result is also saved in {filePath}")
    
# Start the program

run_program()
