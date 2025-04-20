# ISAAC AGUSTIN GARCIA ALONSO

**Requirements**

- Connect to Open Brewery API.
- Retrieve a list of selected items.
- Display the fetched data in a table or list view. Use Vue.js for the front end.
- Filtering: Provide at least one filter input or dropdown (e.g., search by name, type, or category).
- Grouping: Group items by a relevant attribute (e.g., brewery type, etc.) and display grouped totals or subtotals.
- Include a simple chart to visualize the grouped data (pie chart, bar chart, etc.).

**Development plan**

Step 1:
- Build a Flask app with Python.

Step 2:
- Connect the flask app to Open Brewery API.
- Retrieve a list of selected items.

Step 4:
- Create a Vue3 application using Vuetify3.
- Add CORS to the Flask app.
- Add a v-data-table to display the data fetched from Open Brewery API.

Step 5:
- Add filter search field.

Step 6:
- Add a combo to group by the desired property and group the table accordingly to display subtotals.

Step 7:
- Add a chart pie to visualize grouped data.

**How to run it**

cd nordhealth

python -m venv venv

Activate the virtual enviroment:
    - Windows: venv\Scripts\activate.bat
    - Linux: source venv/bin/activate

pip install -r requirements.txt

python ./app.py

cd client

npm install

npm run dev

http://localhost:3000/


**Role / Tech used**

- Senior Fullstack Developer

- It is deliver a complete solution using a backend in Flask with python and a frontend using Vue 3 with Vuetify 3 that display a v-data-table and a pie chart from chart.js using vue-chartjs wrapper.

  
