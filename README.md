# Item Catalog Project
An Udacity Full Stack Web Developer  Nanodegree project.

## About
This application provides a list of bicycles items within a variety of 
  categories as well as provide a user registration and authentication 
  system. Registered users will have the ability to post, edit, and delete 
  their own  bicycle items from the app.

### Features
- Proper authentication and authorisation check.
- Full CRUD support using SQLAlchemy and Flask.
- JSON endpoints.
- Implements oAuth using Google Sign-in  and facebook API.

## In This Repo
This project has one main Python module `app.py` which runs the Flask 
  application. A SQL database is created using the `database_setup.py` 
  module and you can populate the database with test data using 
  `lotsofbicyclesitems.py`.
The Flask application uses stored HTML templates in the tempaltes folder to build the front-end of the application. CSS/JS/Images are stored in the static directory.
## Skills
1. Python
2. HTML
3. CSS
4. OAuth
5. Flask Framework


## Dependencies
- [Vagrant](https://www.vagrantup.com/)
- [Udacity Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

## Steps to run this project and configure the VM

   ```bash
   vagrant up
   ```

   This will cause Vagrant to download the Ubuntu operating system and install it. This may take quite a while depending on how fast your Internet connection is.

 After the above command succeeds, connect to the newly created VM by typing the following command:

   ```bash
   vagrant ssh
   ```

Navigate to the shared repository:
```bash
 cd /vagrant
```


Install or upgrade Flask:
  ``` bash
  sudo python -m pip install --upgrade flask
   ```

Run the following command to set up the database:
  ```bash
   python database_setup.py
   ```

 Run the following command to insert dummy values. 

```bash
    python lotsofbicycleitems.py
```
 Run this application to run the application:
   ``` bash
    python app.py:
```

 Open  the local host:
  ``` bash
  http://localhost:5000/`
```
## JSON Endpoints

Catalog JSON: 
```bash
  /catalog/JSON
```
- Displays  all the categories:
```bash
/catalog/categories/JSON`
```
## Acknowledgments
* [VM configuration](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip) was provided by [udacity](https://www.udacity.com).
* [The bicycles image thanks to yelp.com](https://www.yelp.com/biz_photos/bicycle-heaven-pittsburgh?start=30)


