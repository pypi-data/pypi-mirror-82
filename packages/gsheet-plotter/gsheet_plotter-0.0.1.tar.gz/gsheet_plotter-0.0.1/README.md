<h1 style="text-align:center;">GSheet Plotter</h1>

An interface to plot graphs using data from your Google Spreadsheets.

Features:

- Fetch spreadsheet from ID
- Plot 2D graphs using any two columns
- Export graphs in .png

---

# Quick Links to get up and running
- [Installation](#Installation)
- [Usage](#Usage)
- [Available Methods](#Available-methods)


# Installation:
## Install GSheet Plotter
```sh
pip install gsheet_plotter
```
---
## Create a credentials file(.json) to allow access to GSheet Plotter to access your spreadsheets.
- Go to [Google-Developer-Console](https://console.developers.google.com) and login with your Google account.

- In the left pane click on ```Credentials```

![Step1](https://iili.io/3nHAZX.png)

- Click on ```Create Credentials```

![Step2](https://iili.io/3nIqMv.png)
- In the dropdown, choose ```Service Account```

![Step3](https://iili.io/3nIslp.png)

- Fill in the details, and click on ```Create```

![Step4](https://iili.io/3nIpxs.png)

- Click on ```Done```

- Go back to your dashboard and you'll see new credentials added with the information you entered.

- Click on the <strong>Edit</strong> icon

![Step5](https://iili.io/3nTqbe.png)

- Goto <strong>Keys</strong> on ```Add Key```.

- Download the <strong>JSON</strong> file and move to the working directory.

---
# Usage:

  - Instantiate the class by passing Google Service Account json file,Sheet Id found in the Google Sheet URL and the work sheet name

![Initialize](https://iili.io/3nTwIn.png)

  - Fetch data from the sheet to a pandas dataframe. The dataframe is saved in the ```data``` attribute.
  
![plot_data](https://iili.io/3nuw8B.png)

  - Plot the graph by using two column names
 
![plot_data](https://iili.io/3nABPj.png)

  - Additional method- Fetch the data and plot the graph in one go by passing the column list 
 
![plot_data](https://iili.io/3n5Jj9.png)

---
# Available methods 

![method_dteials](https://iili.io/3nc5xI.png)











