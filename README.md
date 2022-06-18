# AI BASED EARHTHQUAKE DAMAGE PREDICTION
This is a AI based Earthquake damage prediction system which is used to predict the grade of house considering various technical feature after the earthquake has occured.  

## Want to Use?
You can clone this branch and use it right now using the methods given below.  

## Building
It is best to use python **virtualenv** tool to build locally:  
> virtualenv venv  
> source venv/bin/activate  
> git clone https://github.com/RochakSedai/EarthQuake-Damage-Prediction.git

Then you navigate to the base directory of the project and install the requirements in your vitual environment  
> cd  
> pip install -r requirements.txt  

And finally you make migration to the database, create a super user, and run the server  
> python manage.py makemigrations  
>python manage.py migrate  
> python manage.py createsuperuser  
> python manage.py runserver  

You can predict the house grade as **_normaluser_** and also as **_profesionaluser_**