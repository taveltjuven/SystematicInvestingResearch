# Pandas to read csv file and other things
import pandas as pd
# Datareader to download price data from Yahoo Finance
import pandas_datareader as web
# Statsmodels to run our multiple regression model
import statsmodels.api as smf
# To download the Fama French data from the web
import urllib.request
# To unzip the ZipFile
import zipfile

def get_fama_french():
    # Web url
    ff_url = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip"

    # Download the file and save it
    # We will name it fama_french.zip file

    urllib.request.urlretrieve(ff_url, 'fama_french.zip')
    zip_file = zipfile.ZipFile('fama_french.zip', 'r')

    # Next we extact the file data

    zip_file.extractall()

    # Make sure you close the file after extraction

    zip_file.close()

    # Now open the CSV file

    ff_factors = pd.read_csv('F-F_Research_Data_Factors.csv', skiprows=3, index_col=0)
    # We want to find out the row with NULL value
    # We will skip these rows

    ff_row = ff_factors.isnull().any(1).nonzero()[0][0]

    # Read the csv file again with skipped rows
    ff_factors = pd.read_csv('F-F_Research_Data_Factors.csv', skiprows=3, nrows=ff_row, index_col=0)

    # Format the date index
    ff_factors.index = pd.to_datetime(ff_factors.index, format='%Y%m')

    # Format dates to end of month
    ff_factors.index = ff_factors.index + pd.offsets.MonthEnd()

    # Convert from percent to decimal
    ff_factors = ff_factors.apply(lambda x: x / 100)
    return ff_factors

ff_data = get_fama_french()
print(ff_data.tail())