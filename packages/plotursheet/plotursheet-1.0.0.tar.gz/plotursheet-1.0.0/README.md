# Plotursheet Package
The package acts as a wrapper on gsheets and retrieves a sheet from google drive.<br>
Further it uses the same to plot a graph(currently scatterplot for continuos values)<br>
# How to install the library using pip
```
pip install plotursheet
```
Or if you want it in cwd
```
pip install plotursheet -t .
```
This would do the work

# How to initialize the library and select the desired Google sheet

Now once the package is installed,<br>
import the module and run the plotty() function within it <br>
The required values url, column_name1, column_name2(the axes for plot),sheet number<br>
are all to be present in a config.txt file<br>
```
python   #invoke python interpreter
import plotursheet #imports the package to be used
```
N
# How to use the various methods in the library

The package has a single method plotty()
And can be invoked by running
```
import plotursheet
plotursheet.plotty()

```
Once the function is invoked, Google sheet specified at url,sheet_no<br>
is loaded into file "detail.csv" at the working directory<br>
Further pandas is invoked and the sheet is taken in as a pandas dataframe<br>
Then the column names are used to plot with (currently scatterplot for 2 continuous<br>
values is written) 


# IMPORTANT NOTE

1. This package uses authentication for google sheets api
The client_secrets.json must be put in root directory (for authenticaation)<br>
And at the first run authentication flow must be completed from the google account <br>
where the sheet is present in drive<br>
Directory to put in client_secrets
```
"C:/Users/<Usernaame>/"
```
2. In order to supply url and column names and sheet number<br>
The  file config.txt has to be created and placed in current working directory.<br>
The content has to be<br>
```
# config.txt
[sheet]
#url for ur sheet
url="https://docs.google.com/spreadsheets/d/1SrZfvr2ee54r7HR1jGtAE9zHIj_Y-UzK9ok8bdwkpqc/edit?usp=sharing"
#sheet number
n=0
#x_axis
x=offer_price
#y-axis
y=average_sales
```
