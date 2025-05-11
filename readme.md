This is a FastAPI-based authentication app to understand how auth works. 

### App to understand the authenticaion workflows

The app provides the following features:

- **User Registration:**
    - Users can register by providing a username and password.
    - Passwords are securely hashed before being stored in the database.

- **User Login:**
    - Registered users can log in by providing their credentials.
    - If the login is successful, the user is redirected to the "Borrowed Books" page.
    - If the login fails, an appropriate error message is displayed on the home page.

- **Borrowed Books:**
    - After logging in, users can view a list of books they have borrowed.
    - The page displays the book title, borrow date, and due date.

- **Session Management:**
    - The app uses cookies to manage user sessions, ensuring that only logged-in users can access the "Borrowed Books" page.
    - If an unauthenticated user tries to access the page, they are redirected to the home page.

The app uses Jinja2 templates to render dynamic HTML pages.

Error messages and success messages are displayed directly on the home page for better user experience.

The app uses SQLite to store user credentials and borrowed book details.

### How to deploy this app to azure

#### Prerequisites
- Make sure you have an azure subscription and a resource group created in it beforehand. 
- Most of the tutorials try to create resource group for you as well but I generally prefer to do it manually to keep track of things. 
- Rest of the things can be automated.

#### Steps to deploy
- Create a python web app in the resource group.

    ```az webapp up --os-type linux --runtime python:3.12 --resource-group <resource-group-name> --name <web-app-name> --track-status --sku F1 --location westus```

    - Use the location `westus` since generally you don't get available quota in india specific regions (like `westindia`).

- Set the startup.sh as the startup config.
    
    ```az webapp config set --startup-file "startup.sh" --name <web-app-name> --resource-group <resource-group-name>```

- Zip the app into a zip file

    ```zip -r webapp1.zip . -x ".*" -x "*__pycache__*"```

  - Make sure you do it so that when you extract the zip the contents of that matches the root folder contents. For instance,
  requirements.txt, main.py etc.

  

- Deploy the zip.

  ```az webapp deploy --name <web-app-name> --resource-group <resource-group-name> --src-path webapp1.zip```
