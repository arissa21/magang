"# setelah pull ini yang dilakukan:" 
1. buat environment kemudian diaktifkan
2. install dependency
    pip install -r requirement.txt
3. migrasi database
    python manage.py makemigrations
    python manage.py migrate
4. create superuser
   python manage.py createsuperuser
5. run server
    python manage.py runserver