from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import threading
import os
from dotenv import load_dotenv
from werkzeug.serving import make_server
from databasemodule import BackendEndpoint


class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = "supersecretkey"  # Needed for session management
        #self.user_manager = UserManager()
        self.__sql = BackendEndpoint()
        # Define Routes
        self.app.add_url_rule("/", "home", self.home)
        self.app.add_url_rule("/login", "login", self.login, methods=["GET", "POST"])
        self.app.add_url_rule("/logout", "logout", self.logout)
        self.app.add_url_rule("/fetch_data/", "fetch_data", self.fetch_data, methods=["GET"])
        self.app.add_url_rule("/admin_query/", "admin_query", self.admin_query, methods=["GET"])
        load_dotenv()
        self.__admin_pass = os.getenv('ADMIN_FLASK_PASS')
        self.__admin_user_name = os.getenv('ADMIN_FLASK_USER_NAME')

    def admin_query(self):
        pass

    def fetch_data(self):
        tab = request.args.get("tab", "tab1")

        try:
            if tab == "tab1":
                data = self.__sql.get_messages_table()
                if not isinstance(data, list):
                    raise TypeError("Database function must return a list")
                return jsonify(data)

            elif tab == "tab2":
                data = self.__sql.get_users_table()
                if not isinstance(data, list):
                    raise TypeError("Database function must return a list")
                return jsonify(data)

            return jsonify({"error": "Invalid tab"}), 400

        except Exception as e:
            print("ERROR:", str(e))  # Debug in terminal
            return jsonify({"error": str(e)}), 500  # Return error as JSON

    def home(self):
        """Home page - Redirects to login if user is not logged in"""
        if "username" not in session:
            return redirect(url_for("login")) 

        return render_template("home.html", username=session["username"])

    def login(self):
        """Login page - Validates user and redirects after login"""
        if request.method == "POST":
            data = request.get_json()  # Get JSON data from AJAX
            user_name = data.get("user_name", "")
            user_password = data.get("user_password", "")
            #response = {"message": "WRONG CREDENTIALS","redirect": url_for("home")}

            #if self.sql.validate_user(user_name, user_password):
            if user_name == self.__admin_user_name and user_password == self.__admin_pass:
                session["username"] = user_name  # Store user session
                return jsonify({"redirect": url_for("home")})  # ✅ Return JSON redirect
            else:
               return jsonify({"error": "Invalid credentials"})  # ✅ Return error message

        return render_template("login.html")

    def logout(self):
        """Logs out the user and redirects to login"""
        session.pop("username", None)
        response = redirect(url_for("login"))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    def run(self):
        """Starts the Flask app in a background thread using a threaded WSGI server"""
        self.server = make_server("127.0.0.1", 5000, self.app)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        print("✅ Flask server started on http://127.0.0.1:5000")

    def stop(self):
        """Stops the Flask app"""
        if self.server:
            self.server.shutdown()
            self.thread.join()
            print("❌ Flask server stopped.")

if __name__ == "__main__":
    flask_app = FlaskApp()
    flask_app.run()
    try:
        while True:
            pass  # Keep the script running
    except KeyboardInterrupt:
        print("\nStopping Flask app...")
        flask_app.stop()
