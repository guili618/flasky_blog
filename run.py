from flasky_blog import create_app

app = create_app()





if __name__ == '__main__':
    app.run(debug=True)



# POWERSHELL 
# $env:FLASK_APP = "flasky_blog.py"
# $env:FLASK_ENV = "development"