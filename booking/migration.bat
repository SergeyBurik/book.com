v
echo "start_migration_done"
pause
python manage.py makemigrations
echo "migrations_created"
pause
python manage.py migrate
echo "migration_done"
pause