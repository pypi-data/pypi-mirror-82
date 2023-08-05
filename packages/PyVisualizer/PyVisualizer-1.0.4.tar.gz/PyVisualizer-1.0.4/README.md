# PyVisualizer_Task2
A simple static visualizer, Wrapper around Gspread lib for reading the google sheets.

# Installation
<pre>pip install PyVisualizer</pre>

# Points to keep in mind
<b>You can access any Google sheet, if that google sheet is shared with this user <h4>"new-service-acc@task-2-greendeck.iam.gserviceaccount.com"</h6>. This is because test account has been registered to access a google service account and configured accordingly.</b>

# Overview
<b>This lib has 3 parts</b><br>
  1 - Connect to the Google sheet by passing the <b>service_account.json</b> file path as a parameter<br>
  2 - After successfully connection, Read the Google sheet with the connection object and get the specified sheetobject in return.<br>
  3 - Once the data has been read successfully, Pass the data to pre-defined methods of Visualizer class for plotting.<br>

# QuickStart
<h3><b>1 - Import 2 classes of PyVisualizer package</b><br></h3>
CommonUtilities class holds 2 methods.<br>
  1 - connectAndAutorizeToServiceAccount() : This method accepts a service_account.json file path as a parameter and return clientConnectionObject.<br>
  2 - read_google_sheet() : This method accepts 3 parameters. clientConnectionObject, Google Sheet file name, Worksheet name. It returns sheetObject for access the data.<br>
<pre>
>>> from PyVisualizer.CommonUtilities import CommonUtilities
>>> from PyVisualizer.Visualizer import Visualizer
</pre>

<h3><b>2 - Create a connection and read the data.</b></h3>
<pre>
>>> commonUtils = CommonUtilities()
>>> connectionClient = commonUtils.connectAndAutorizeToSeriveAccount("pass_the_service_account.json file path, you can download it from this repo /PyVisualizer/service_account.json.")
Successfully Authorized and Connected to Google Service Account. :)
>>> sheetObj = com.read_google_sheet(connectionClient,"Copy_of_Greendeck_SE_Assignment_Task_2","Sheet1") # 2nd parameter is the file name, which is already shared with test account
>>> sheet1_data = sheetObj.get_all_records() # This return the json array
</pre>

<h3><b>3 - Converting the sheet data into pandas DataFrame and passing it to pre-defined methods</b></h3>
<pre>
>>> import pandas as pd
>>> df = pd.DataFrame(sheet1_data)
>>> Visualizer().barPlotSalesByYear(pandasDataframe=df,xColName="timestamp",yColName="average_sales",sSaveWithFileName="salesByYear.png")
>>> Visualizer().barPlotSalesByMonth(pandasDataframe=df,xColName="timestamp",yColName="average_sales",sSaveWithFileName="salesByMonth.png")
>>> Visualizer().getSalesByYearsAndMonths(df)
</pre>
