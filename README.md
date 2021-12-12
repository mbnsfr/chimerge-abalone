run this command on main directory

pip install -r requirements.txt

if you want to run python of the project virtual then run this command on main folder

virtualenv venv -p python<your python version>
source venv/bin/activate

now in <chiMerge> folder for run project run this command

there is a bug in python3 so if you want to run it properly you should change directory on line 193 in chiMerge/view/views.py to your own directory --> relative path : chiMerge/static/abalone.data

!!! help : you can get it from file properties.

if you installed and activated virtualenv :

python manage.py runserver

else :

python<your python version> manage.py runserver
