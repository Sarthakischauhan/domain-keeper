from main_app import app

if __name__ == "__main__":
    print(app.config["ENCRYPTION_KEY"])
    app.run(debug=True)

