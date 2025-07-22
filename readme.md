# Cloudstore

I decided to create a second version of my Azure Fileshare App, as the first version had too many dependencies and was confusing to host and set up.

This new version is built using **Django**, a lightweight and powerful web framework for Python.

### To Run the Django App:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/cloudstore.git
   cd cloudstore
   ```

2. **Set up a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**

   ```bash
   python manage.py migrate
   ```

5. **Create a Demo User**
    ```bash
    python manage.py create_demo_user
    ```
    You can customise username & password in the file located at _apps > users > management > commands > create_demo_user.py_

6. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

7. **Access the app:**
   Open your browser and go to `http://127.0.0.1:8000/`
