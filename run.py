from articlee import create_app
# articleenv\Scripts\activate --> activate env
# deactivate
app,_ = create_app()
if __name__ == '__main__':
    app.run(debug=True)

