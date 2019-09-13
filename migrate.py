from articlee import create_app

'''
If there're edits in one of the table, commands for migration
1) PROJECTS\BLOG_WEBAPP_FLASK>python migrate.py db init --> only first time
2) python migrate.py db migrate
3) python migrate.py db upgrade
'''
_,manager = create_app()

if __name__ =="__main__":
    manager.run()
