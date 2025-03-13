# WebApp boilerplate with React JS and Flask API

Build web applications using React.js for the front end and python/flask for your backend API.

- Documentation can be found here: https://start.4geeksacademy.com/starters/react-flask
- Here is a video on [how to use this template](https://www.loom.com/share/f37c6838b3f1496c95111e515e83dd9b)
- Integrated with Pipenv for package managing.
- Fast deployment to heroku [in just a few steps here](https://start.4geeksacademy.com/backend/deploy-heroku-posgres).
- Use of .env file.
- SQLAlchemy integration for database abstraction.

### 1) Installation:

> If you use Github Codespaces (recommended) or Gitpod this template will already come with Python, Node and the Posgres Database installed. If you are working locally make sure to install Python 3.10, Node 

It is recomended to install the backend first, make sure you have Python 3.8, Pipenv and a database engine (Posgress recomended)

1. Install the python packages: `$ pipenv install`
2. Create a .env file based on the .env.example: `$ cp .env.example .env`
3. Install your database engine and create your database, depending on your database you have to create a DATABASE_URL variable with one of the possible values, make sure you replace the valudes with your database information:

| Engine    | DATABASE_URL                                        |
| --------- | --------------------------------------------------- |
| SQLite    | sqlite:////test.db                                  |
| MySQL     | mysql://username:password@localhost:port/example    |
| Postgress | postgres://username:password@localhost:5432/example |

4. Migrate the migrations: `$ pipenv run migrate` (skip if you have not made changes to the models on the `./src/api/models.py`)
5. Run the migrations: `$ pipenv run upgrade`
6. Run the application: `$ pipenv run start`

> Note: Codespaces users can connect to psql by typing: `psql -h localhost -U gitpod example`

### Undo a migration

You are also able to undo a migration by running

```sh
$ pipenv run downgrade
```

### Backend Populate Table Users

To insert test users in the database execute the following command:

```sh
$ flask insert-test-users 5
```

And you will see the following message:

```
  Creating test users
  test_user1@test.com created.
  test_user2@test.com created.
  test_user3@test.com created.
  test_user4@test.com created.
  test_user5@test.com created.
  Users created successfully!
```

### **Important note for the database and the data inside it**

Every Github codespace environment will have **its own database**, so if you're working with more people eveyone will have a different database and different records inside it. This data **will be lost**, so don't spend too much time manually creating records for testing, instead, you can automate adding records to your database by editing ```commands.py``` file inside ```/src/api``` folder. Edit line 32 function ```insert_test_data``` to insert the data according to your model (use the function ```insert_test_users``` above as an example). Then, all you need to do is run ```pipenv run insert-test-data```.

### Front-End Manual Installation:

-   Make sure you are using node version 14+ and that you have already successfully installed and runned the backend.

1. Install the packages: `$ npm install`
2. Start coding! start the webpack dev server `$ npm run start`

### Database population

To correctly populate your database follow these steps:

1. Start by populating the teams using the URL `<YOUR-CODESPACE-URL>/api/populate-db-1`. This will fill the *teams* and *matches* tables
2. Next, we will populate the *coaches* table. Due tho our external API limit of 10 requests per minute, we will have to call the same endpoint two times to correctly populate our 20 coaches. The two URLs are:
```
<YOUR-CODESPACE-BACKEND-URL>/api/populate-coaches?team_ids=529,530,531,532,533,534,536,538,541,542

<YOUR-CODESPACE-BACKEND-URL>/api/populate-coaches?team_ids=543,546,547,548,715,723,724,727,728,798
```

> [!NOTE]  
> Remember waiting 1 minute between petitions

3. Next we will populate our *players* table. We will have to do the same that we did in step 2 due to request rate, but in this case we will have to do 7 petitions, because the squads have various pages. The URLs are
```
<YOUR-CODESPACE-BACKEND-URL>/api/populate-players?team_ids=529,530,531
<YOUR-CODESPACE-BACKEND-URL>/api/populate-players?team_ids=532,533,534
<YOUR-CODESPACE-BACKEND-URL>/api/populate-players?team_ids=536,538,541
<YOUR-CODESPACE-BACKEND-URL>/api/populate-players?team_ids=542,543,546
<YOUR-CODESPACE-BACKEND-URL>/api/populate-players?team_ids=547,548,715
<YOUR-CODESPACE-BACKEND-URL>/api/populate-players?team_ids=723,724,727
<YOUR-CODESPACE-BACKEND-URL>/api/populate-players?team_ids=728,798
```

> [!NOTE]  
> Remember waiting 1 minute between petitions

It's important to **follow these steps in this exact order** because the relationships of the tables may cause failure when populating.

When you finish populating, you will have used 77 of the 100 daily petitions we have currently available in the external API, so please do not use it much

## Publish your website!

This boilerplate it's 100% read to deploy with Render.com and Heroku in a matter of minutes. Please read the [official documentation about it](https://start.4geeksacademy.com/deploy).

### Contributors

This template was built as part of the 4Geeks Academy [Coding Bootcamp](https://4geeksacademy.com/us/coding-bootcamp) by [Alejandro Sanchez](https://twitter.com/alesanchezr) and many other contributors. Find out more about our [Full Stack Developer Course](https://4geeksacademy.com/us/coding-bootcamps/part-time-full-stack-developer), and [Data Science Bootcamp](https://4geeksacademy.com/us/coding-bootcamps/datascience-machine-learning).

You can find other templates and resources like this at the [school github page](https://github.com/4geeksacademy/).
