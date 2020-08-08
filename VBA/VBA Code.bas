Attribute VB_Name = "RibbonX_Code"
'Create a script that will loop through all the stocks for one year for each run and take the following information.
    'The ticker symbol.
    'Yearly change from opening price at the beginning of a given year to the closing price at the end of that year.
    'The percent change from opening price at the beginning of a given year to the closing price at the end of that year.
    'The total stock volume of the stock.
    'You should also have conditional formatting that will highlight positive change in green and negative change in red.
	
Sub stocks2():
Dim openingval As Double
Dim closingval As Double
Dim currentticker As String
Dim nextticker As String
Dim internalcounter As Integer
Dim volumecounter As Double
Dim maxvolumestore As Double
Dim greatestpercentincrease As Double
Dim greatestpercentdecrease As Double
Dim lastrow As Long
Dim WS_Count As Integer
Dim q As Integer

'The following line of code finds the number of active worksheets.
WS_Count = ActiveWorkbook.Worksheets.Count

'The following For Statement loops through all of the worksheets in the file
For q = 1 To WS_Count
    'Selects active worksheet
    Worksheets(q).Select
    'These are my variable initializations:
    'internalcounter is a variable I have used to write to columns 9-12 with my outputs (Ticker Symbol, Yearly Change, Percent Change, Total Stock Volume Traded).
    'I have started it from a count of 2 because the first row is for the column names.
    internalcounter = 2
    'The following is the first stock in the Spreadsheet's opening value.
    openingval = Cells(2, 3)
    'Initializing the variable that counts the total stock volume traded.
    volumecounter = 0
    'The following lines of code initialize the variables that keep count of the Maximum Stock Volume Traded, Greatest Stock % Increase, and Greatest Stock % Decrease with a value of 0.
    maxvolumestore = 0
    greatestpercentincrease = 0
    greatestpercentdecrease = 0
    
    'The following line of code finds the total number of rows in a spreadsheet.
    lastrow = Cells(Rows.Count, "A").End(xlUp).Row
    MsgBox (lastrow)

    'The following lines of code set the column names.
    Cells(1, 9).Value = "Ticker Symbol"
    Cells(1, 10).Value = "Yearly Change"
    Cells(1, 11).Value = "Percent Change"
    Cells(1, 12).Value = "Total Stock Volume Traded"
    Cells(1, 16).Value = "Ticker"
    Cells(1, 17).Value = "Value"
    Cells(2, 15).Value = "Greatest % Increase"
    Cells(3, 15).Value = "Greatest % Increase"
    Cells(4, 15).Value = "Greatest % Increase"
    
    For i = 2 To lastrow
        'Nextticker stores the ticker symbol of the i+1th row, and currentticker stores the ticker symbol of the ith row.
        currentticker = Cells(i, 1).Value
        nextticker = Cells(i + 1, 1).Value
        'The follow line of code sums the total volume of a stock traded cumulatively.
        volumecounter = volumecounter + Cells(i, 7).Value
        'When the tickersymbol changes that means a new stocks information has come.
        If currentticker <> nextticker Then
            'The following line of code collects the closing stock value of the year.
            closingval = Cells(i, 6).Value
            'These following 4 lines of code print out the ticker symbol, Yearly Change, Percent Change, and Total Stock Volume Traded, respectively.
            Cells(internalcounter, 9).Value = currentticker
            Cells(internalcounter, 10).Value = closingval - openingval
            'Fail safe if value ends up being 0:
            If openingval <> 0 Then
                Cells(internalcounter, 11).Value = (Cells(internalcounter, 10) / openingval) * 100
            End If
            Cells(internalcounter, 12).Value = volumecounter
            'The following are some conditionals to keep track of the Maximum Stock Volume Traded, Greatest Stock % Increase, and Greatest Stock % Decrease.
            If volumecounter > maxvolumestore Then
                maxvolumestore = volumecounter
                Cells(4, 16).Value = currentticker
            End If
            If Cells(internalcounter, 11).Value > greatestpercentincrease Then
                greatestpercentincrease = Cells(internalcounter, 11).Value
                Cells(2, 16).Value = currentticker
            End If
            If Cells(internalcounter, 11).Value < 0 Then
                If Abs(Cells(internalcounter, 11).Value) > Abs(greatestpercentdecrease) Then
                    greatestpercentdecrease = Cells(internalcounter, 11)
                    Cells(3, 16).Value = currentticker
                End If
            End If
            'Reset values for next stock
            volumecounter = 0
            openingval = Cells(i + 1, 3).Value
            internalcounter = internalcounter + 1
        End If
    Next i
    'The following code prints the Maximum Stock Volume Traded, Greatest Stock % Increase, and Greatest Stock % Decrease to the workbook.
    Cells(2, 17).Value = greatestpercentincrease
    Cells(3, 17).Value = greatestpercentdecrease
    Cells(4, 17).Value = maxvolumestore
Next q
End Sub

Sub conditionalformatting():
Dim WS_Count As Integer
Dim lastrow As Long
Dim q As Integer

WS_Count = ActiveWorkbook.Worksheets.Count

For q = 1 To WS_Count
    Worksheets(q).Select
    MsgBox (ActiveSheet.Name)
    
    lastrow = Cells(Rows.Count, "J").End(xlUp).Row
    
    'Simple two colour scheme for conditional formatting, 4 = green, 3 = red
    For i = 2 To lastrow
        If Cells(i, 10).Value > 0 Then
            Cells(i, 10).Interior.ColorIndex = 4
        End If
        If Cells(i, 10).Value <= 0 Then
            Cells(i, 10).Interior.ColorIndex = 3
        End If
    Next i
Next q
End Sub
