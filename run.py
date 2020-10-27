from articlee import create_app
# articleenv\Scripts\activate --> activate env
# deactivate

# Instanzio l'app attraverso la funzione create_app()

app, _ = create_app()
if __name__ == '__main__':
    app.run(debug=True)
