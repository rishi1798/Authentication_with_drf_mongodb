First of all create a folder on local
now after creating the folder open terminal and run this command "git clone https://github.com/rishi1798/Authentication_with_drf_mongodb.git"
Now create python virtual environment by running this command "python -m venv env"
Now enter into virtual environment and activate it by "cd env/scripts" and "activate"
enter into "cd Authentication_with_drf_mongodb"
now install all the required dependecies by command "pip install -r requirements.txt"

now run the server by "python manage.py runserver 4000" i have used port 4000 in my api collection u can use also use default port i.e. 8000 but make sure to change the port number
from 4000 to your port number in my postman api collection.

Login Api : http://127.0.0.1:4000/login/
request body : {
    "phone": "7891350412",
    "password": "abababab1"
}
Method : POST

Profile Api: http://127.0.0.1:4000/profile/
In Headers tab : In Authorization key fill the value of token
Method : GET

Logout Api : http://127.0.0.1:4000/logout/
In Headers tab : In Authorization key fill the value of token
Method : POST
