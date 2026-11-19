# from datetime import date, datetime

# import mysql.connector
# from flask import Flask, jsonify, redirect, render_template, request, session, url_for
# from werkzeug.security import check_password_hash, generate_password_hash

# app = Flask(__name__)
# app.secret_key = "study_treasure_secure_secret_key"

# # MySQL Database Configuration
# db_config = {
#     "host": "localhost",
#     "user": "root",
#     "password": "Prakrati11",
#     "database": "study_treasure",
# }


# def get_db():
#     conn = mysql.connector.connect(**db_config)
#     return conn


# # ==========================================
# # DAILY CONSECUTIVE STREAK UPDATE FUNCTION
# # ==========================================
# def update_student_streak(student_email):
#     today = date.today()
#     try:
#         conn = get_db()
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute(
#             "SELECT current_streak, last_active_date FROM students WHERE email = %s",
#             (student_email,),
#         )
#         student = cursor.fetchone()

#         if not student:
#             cursor.close()
#             conn.close()
#             return 0

#         current_streak = student.get("current_streak", 0) or 0
#         last_date = student.get("last_active_date")

#         # Safe conversion: Ensure last_date is a datetime.date object
#         if isinstance(last_date, datetime):
#             last_date = last_date.date()
#         elif isinstance(last_date, str):
#             try:
#                 last_date = datetime.strptime(last_date.split()[0], "%Y-%m-%d").date()
#             except:
#                 last_date = None

#         new_streak = current_streak

#         if last_date is None:
#             new_streak = 1
#         elif last_date == today:
#             new_streak = current_streak
#         elif last_date == date.fromordinal(today.toordinal() - 1):
#             new_streak = current_streak + 1
#         else:
#             new_streak = 1

#         # Database update
#         cursor.execute(
#             """
#             UPDATE students 
#             SET current_streak = %s, last_active_date = %s 
#             WHERE email = %s
#         """,
#             (new_streak, today, student_email),
#         )
#         conn.commit()
#         cursor.close()
#         conn.close()

#         # Update session so navbar reflects it immediately
#         session["student_streak"] = new_streak
#         return new_streak
#     except Exception as e:
#         print("Error updating streak:", e)
#         return session.get("student_streak", 0)


# @app.route("/")
# def home():
#     return render_template("index.html")


# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         full_name = request.form["full_name"].strip()
#         roll_number = request.form["roll_number"].strip()
#         email = request.form["email"].strip()
#         student_class = request.form["student_class"]
#         password = request.form["password"]
#         confirm_password = request.form["confirm_password"]

#         if len(password) < 6:
#             return "Password must be at least 6 characters long! <a href='/register'>Go Back</a>"

#         if password != confirm_password:
#             return "Passwords do not match! <a href='/register'>Go Back</a>"

#         try:
#             conn = get_db()
#             cursor = conn.cursor(dictionary=True)

#             cursor.execute(
#                 "SELECT * FROM students WHERE email = %s OR roll_number = %s",
#                 (email, roll_number),
#             )
#             existing_user = cursor.fetchone()

#             if existing_user:
#                 cursor.close()
#                 conn.close()
#                 return "Error: Email or Roll Number already registered! Please use unique credentials. <a href='/register'>Go Back</a>"

#             password_hash = generate_password_hash(password)

#             query = """
#                 INSERT INTO students (full_name, roll_number, email, student_class, password_hash, total_coins, current_streak) 
#                 VALUES (%s, %s, %s, %s, %s, 0, 0)
#             """
#             cursor.execute(
#                 query, (full_name, roll_number, email, student_class, password_hash)
#             )
#             conn.commit()
#             cursor.close()
#             conn.close()
#             return redirect(url_for("home"))
#         except mysql.connector.Error as err:
#             return f"Database Error: {err} <a href='/register'>Try Again</a>"

#     return render_template("student_register.html")


# @app.route("/faculty/register", methods=["GET", "POST"])
# def faculty_register():
#     if request.method == "POST":
#         full_name = request.form.get("full_name", "").strip()
#         faculty_id = request.form.get("faculty_id", "").strip()
#         email = request.form.get("email", "").strip()
#         department = request.form.get("department")

#         classes_list = request.form.getlist("classes_taught")
#         classes_taught = ", ".join(classes_list)

#         password = request.form.get("password")
#         confirm_password = request.form.get("confirm_password")

#         if len(password) < 6:
#             return "Password must be at least 6 characters long! <a href='/faculty/register'>Go Back</a>"

#         if password != confirm_password:
#             return "Passwords do not match! <a href='/faculty/register'>Go Back</a>"

#         try:
#             conn = get_db()
#             cursor = conn.cursor(dictionary=True)

#             cursor.execute(
#                 "SELECT * FROM faculty WHERE email = %s OR faculty_id = %s",
#                 (email, faculty_id),
#             )
#             existing_faculty = cursor.fetchone()

#             if existing_faculty:
#                 cursor.close()
#                 conn.close()
#                 return "Error: Email or Faculty ID already registered! Please use unique credentials. <a href='/faculty/register'>Go Back</a>"

#             password_hash = generate_password_hash(password)

#             query = """
#                 INSERT INTO faculty (full_name, faculty_id, email, department, classes_taught, password_hash) 
#                 VALUES (%s, %s, %s, %s, %s, %s)
#             """
#             cursor.execute(
#                 query,
#                 (
#                     full_name,
#                     faculty_id,
#                     email,
#                     department,
#                     classes_taught,
#                     password_hash,
#                 ),
#             )
#             conn.commit()
#             cursor.close()
#             conn.close()
#             return redirect(url_for("home"))
#         except mysql.connector.Error as err:
#             return f"Database Error: {err} <a href='/faculty/register'>Try Again</a>"

#     return render_template("faculty_register.html")


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         role = request.form.get("role")
#         email = request.form.get("email")
#         password = request.form.get("password")

#         if role == "student":
#             try:
#                 conn = get_db()
#                 cursor = conn.cursor(dictionary=True)
#                 query = "SELECT * FROM students WHERE email = %s"
#                 cursor.execute(query, (email,))
#                 student = cursor.fetchone()
#                 cursor.close()
#                 conn.close()

#                 if student:
#                     if check_password_hash(student["password_hash"], password):
#                         session["student_email"] = student["email"]
#                         session["student_class"] = str(student["student_class"]).strip()
#                         session["student_name"] = student["full_name"]
#                         session["student_coins"] = student.get("total_coins", 0)
#                         session["student_streak"] = (
#                             student.get("current_streak", 0) or 0
#                         )
#                         return render_template(
#                             "login.html",
#                             alert_message="Welcome back, You Successfully Logged in",
#                             redirect_url=url_for("subjects"),
#                         )
#                     else:
#                         return render_template(
#                             "login.html",
#                             alert_message="Incorrect password",
#                             redirect_url=url_for("login"),
#                         )
#                 else:
#                     return render_template(
#                         "login.html",
#                         alert_message="Email not found!",
#                         redirect_url=url_for("login"),
#                     )
#             except mysql.connector.Error as err:
#                 return render_template(
#                     "login.html",
#                     alert_message=f"Database Error: {err}",
#                     redirect_url=None,
#                 )

#         elif role == "faculty":
#             try:
#                 conn = get_db()
#                 cursor = conn.cursor(dictionary=True)
#                 query = "SELECT * FROM faculty WHERE email = %s"
#                 cursor.execute(query, (email,))
#                 faculty = cursor.fetchone()
#                 cursor.close()
#                 conn.close()

#                 if faculty and check_password_hash(faculty["password_hash"], password):
#                     session["faculty_name"] = faculty["full_name"]
#                     session["faculty_classes"] = faculty["classes_taught"]
#                     return render_template(
#                         "login.html",
#                         alert_message="Welcome back, Faculty Login Successful",
#                         redirect_url=url_for("faculty_dashboard"),
#                     )
#                 else:
#                     return render_template(
#                         "login.html",
#                         alert_message="Invalid credentials",
#                         redirect_url=url_for("home"),
#                     )
#             except mysql.connector.Error as err:
#                 return render_template(
#                     "login.html",
#                     alert_message=f"Database Error: {err}",
#                     redirect_url=url_for("home"),
#                 )
#         else:
#             return redirect(url_for("home"))

#     return render_template("login.html", alert_message=None, redirect_url=None)


# # ==========================================
# # ACTIVE GAME COMPLETION API FOR STREAK & COINS
# # ==========================================
# @app.route("/api/complete_game", methods=["POST"])
# def complete_game():
#     if "student_email" not in session:
#         return jsonify({"error": "Unauthorized"}), 401

#     data = request.json or {}
#     earned_coins = data.get("coins", 15)
#     email = session.get("student_email")

#     try:
#         conn = get_db()
#         cursor = conn.cursor()
#         cursor.execute(
#             "UPDATE students SET total_coins = total_coins + %s WHERE email = %s",
#             (earned_coins, email),
#         )
#         conn.commit()
#         cursor.close()
#         conn.close()

#         session["student_coins"] = session.get("student_coins", 0) + earned_coins
#         new_streak = update_student_streak(email)

#         return jsonify(
#             {
#                 "status": "success",
#                 "streak": new_streak,
#                 "coins": session["student_coins"],
#             }
#         )
#     except Exception as e:
#         print("Error completing game:", e)
#         return jsonify({"status": "error", "message": str(e)}), 500


# @app.route("/faculty/dashboard")
# def faculty_dashboard():
#     faculty_name = session.get("faculty_name")
#     faculty_classes_str = session.get("faculty_classes", "")

#     if not faculty_name:
#         return redirect(url_for("login"))

#     allowed_numbers = []
#     for c in faculty_classes_str.split(","):
#         digits = "".join([ch for ch in c if ch.isdigit()])
#         if digits:
#             allowed_numbers.append(digits)

#     try:
#         conn = get_db()
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute(
#             "SELECT full_name, roll_number, email, student_class, total_coins, current_streak FROM students"
#         )
#         all_students = cursor.fetchall()
#         cursor.close()
#         conn.close()

#         filtered_students = []
#         for s in all_students:
#             s_class = str(s["student_class"]).strip()
#             s_digits = "".join([ch for ch in s_class if ch.isdigit()])
#             if s_digits in allowed_numbers:
#                 filtered_students.append(s)

#         return render_template(
#             "faculty_dashboard.html",
#             faculty_name=faculty_name,
#             classes=faculty_classes_str,
#             students=filtered_students,
#         )
#     except Exception as e:
#         return f"Error loading analytics: {e}"


# @app.route("/subjects")
# def subjects():
#     student_class = session.get("student_class", "")
#     student_name = session.get("student_name", "")
#     student_coins = session.get("student_coins", 0)
#     return render_template(
#         "subjects.html",
#         student_class=student_class,
#         student_name=student_name,
#         student_coins=student_coins,
#     )


# @app.route("/subject/mathematics")
# def math_hub():
#     student_class = str(session.get("student_class", "")).lower()
#     if "6" in student_class:
#         return render_template("class6_math.html")
#     return "No Quiz and Games uploaded"


# @app.route("/subject/science")
# def science_hub():
#     student_class = str(session.get("student_class", "")).lower()
#     if "11" in student_class or "12" in student_class:
#         return redirect(url_for("attempt_quiz"))
#     elif "7" in student_class:
#         return redirect(url_for("class7_chemistry"))
#     elif "8" in student_class:
#         return redirect(url_for("class8_physics"))
#     else:
#         return redirect(url_for("attempt_quiz"))


# @app.route("/class7/chemistry")
# def class7_chemistry():
#     return render_template("class7_chemistry.html")


# @app.route("/class8/physics")
# def class8_physics():
#     return render_template("class8_physics.html")


# @app.route("/game/geometry-quest")
# def geometry_quest():
#     if "student_email" not in session:
#         return redirect(url_for("login"))
#     return render_template(
#         "geometry_quest.html",
#         student_name=session.get("student_name", ""),
#         student_coins=session.get("student_coins", 0),
#         student_streak=session.get("student_streak", 0),
#     )


# @app.route("/game/litmus-lab")
# def litmus_lab():
#     if "student_email" not in session:
#         return redirect(url_for("login"))
#     return render_template(
#         "litmus_lab.html",
#         student_name=session.get("student_name", ""),
#         student_coins=session.get("student_coins", 0),
#         student_streak=session.get("student_streak", 0),
#     )


# @app.route("/game/circuit-builder")
# def circuit_builder():
#     if "student_email" not in session:
#         return redirect(url_for("login"))
#     return render_template(
#         "circuit_builder.html",
#         student_name=session.get("student_name", ""),
#         student_coins=session.get("student_coins", 0),
#         student_streak=session.get("student_streak", 0),
#     )


# @app.route("/attempt-quiz")
# def attempt_quiz():
#     student_class = str(session.get("student_class", "")).lower()
#     return render_template("attempt_quiz.html", student_class=student_class)


# @app.route("/quiz/<chapter>")
# def quiz_page(chapter):
#     session["quiz_slot"] = {
#         "chapter": chapter.strip(),
#         "current_q_index": 0,
#         "total_questions": 5,
#         "coins": 0,
#         "streak": 0,
#         "asked_ids": [],
#         "current_difficulty": "medium",
#     }
#     return render_template(
#         "quiz.html",
#         chapter=chapter,
#         student_name=session.get("student_name", "Student"),
#     )


# @app.route("/api/get_question", methods=["GET"])
# def get_question():
#     try:
#         slot = session.get("quiz_slot")
#         if not slot:
#             slot = {
#                 "chapter": "Solutions",
#                 "current_q_index": 0,
#                 "total_questions": 5,
#                 "coins": 0,
#                 "streak": 0,
#                 "asked_ids": [],
#                 "current_difficulty": "medium",
#             }
#             session["quiz_slot"] = slot

#         if slot["current_q_index"] >= slot["total_questions"]:
#             earned_coins = slot["coins"]
#             email = session.get("student_email")
#             if email and earned_coins > 0:
#                 try:
#                     conn = get_db()
#                     cursor = conn.cursor()
#                     cursor.execute(
#                         "UPDATE students SET total_coins = total_coins + %s WHERE email = %s",
#                         (earned_coins, email),
#                     )
#                     conn.commit()
#                     cursor.close()
#                     conn.close()

#                     session["student_coins"] = (
#                         session.get("student_coins", 0) + earned_coins
#                     )
#                     update_student_streak(email)
#                 except Exception as db_err:
#                     print("Error updating score and streak:", db_err)

#             return jsonify({"status": "completed", "total_coins": slot["coins"]})

#         conn = get_db()
#         cursor = conn.cursor(dictionary=True)

#         raw_chapter = str(slot["chapter"]).strip()
#         excluded_ids = slot["asked_ids"] if slot["asked_ids"] else [0]
#         format_strings = ",".join(["%s"] * len(excluded_ids))
#         target_diff = slot["current_difficulty"].strip().lower()

#         query = f"""
#             SELECT * FROM questions 
#             WHERE (LOWER(chapter) = LOWER(%s) OR REPLACE(LOWER(chapter), ' ', '') = REPLACE(LOWER(%s), ' ', '')) 
#               AND LOWER(difficulty) = %s 
#               AND id NOT IN ({format_strings})
#             ORDER BY RAND() LIMIT 1
#         """
#         cursor.execute(query, [raw_chapter, raw_chapter, target_diff] + excluded_ids)
#         q = cursor.fetchone()

#         if not q:
#             fallback_query1 = f"""
#                 SELECT * FROM questions 
#                 WHERE (LOWER(chapter) = LOWER(%s) OR REPLACE(LOWER(chapter), ' ', '') = REPLACE(LOWER(%s), ' ', '')) 
#                   AND id NOT IN ({format_strings})
#                 ORDER BY RAND() LIMIT 1
#             """
#             cursor.execute(fallback_query1, [raw_chapter, raw_chapter] + excluded_ids)
#             q = cursor.fetchone()

#         if not q:
#             fallback_query2 = f"""
#                 SELECT * FROM questions 
#                 WHERE id NOT IN ({format_strings})
#                 ORDER BY RAND() LIMIT 1
#             """
#             cursor.execute(fallback_query2, excluded_ids)
#             q = cursor.fetchone()

#         cursor.close()
#         conn.close()

#         if not q:
#             return jsonify({"status": "completed", "total_coins": slot["coins"]})

#         slot["asked_ids"].append(q["id"])
#         session["current_question"] = q
#         session.modified = True

#         return jsonify(
#             {
#                 "status": "success",
#                 "question_number": slot["current_q_index"] + 1,
#                 "total_slot_questions": slot["total_questions"],
#                 "question_text": q["question_text"],
#                 "options": [q["option_a"], q["option_b"], q["option_c"], q["option_d"]],
#                 "difficulty": q["difficulty"],
#                 "coins": slot["coins"],
#                 "streak": slot["streak"],
#             }
#         )
#     except Exception as e:
#         print("ERROR in /api/get_question:", str(e))
#         return jsonify({"status": "error", "message": str(e)}), 500


# @app.route("/api/submit_answer", methods=["POST"])
# def submit_answer():
#     try:
#         data = request.json
#         selected_idx = data.get("selected")

#         slot = session.get("quiz_slot")
#         curr_q = session.get("current_question")

#         if not slot or not curr_q:
#             return jsonify({"error": "Invalid Session"}), 400

#         is_correct = selected_idx == curr_q["correct_answer"]

#         if is_correct:
#             slot["streak"] += 1
#             earned = curr_q["reward_coins"] + (5 * slot["streak"])
#             slot["coins"] += earned
#         else:
#             slot["streak"] = 0

#         current_diff = slot["current_difficulty"].lower()

#         if is_correct:
#             if current_diff == "medium" or current_diff == "hard":
#                 slot["current_difficulty"] = "hard"
#             elif current_diff == "easy":
#                 slot["current_difficulty"] = "medium"
#         else:
#             if current_diff == "hard":
#                 slot["current_difficulty"] = "medium"
#             elif current_diff == "medium" or current_diff == "easy":
#                 slot["current_difficulty"] = "easy"

#         slot["current_q_index"] += 1
#         session.modified = True

#         return jsonify(
#             {
#                 "is_correct": is_correct,
#                 "correct_answer": curr_q["correct_answer"],
#                 "coins": slot["coins"],
#                 "streak": slot["streak"],
#                 "next_difficulty": slot["current_difficulty"],
#             }
#         )
#     except Exception as e:
#         print("ERROR in /api/submit_answer:", str(e))
#         return jsonify({"error": str(e)}), 500


# @app.route("/logout")
# def logout():
#     session.clear()
#     return redirect(url_for("home"))


# @app.route("/api/sync_offline_progress", methods=["POST"])
# def sync_offline_progress():
#     data = request.get_json()

#     student_id = data.get("student_id")
#     points_earned = data.get("points_earned", 0)
#     streak_count = data.get("streak_count", 0)

#     if not student_id:
#         return jsonify({"status": "error", "message": "Student ID missing"}), 400

#     try:
#         cursor = mysql.connection.cursor()
#         # MySQL database me coins aur streak update karne ki query
#         cursor.execute(
#             """
#             UPDATE students 
#             SET coins = coins + %s, 
#                 streak = GREATEST(streak, %s) 
#             WHERE id = %s
#         """,
#             (points_earned, streak_count, student_id),
#         )
#         mysql.connection.commit()
#         cursor.close()

#         return jsonify(
#             {"status": "success", "message": "Progress synced successfully!"}
#         )
#     except Exception as e:
#         print("Database sync error:", e)
#         return jsonify({"status": "error", "message": str(e)}), 500


# if __name__ == "__main__":
#     app.run(debug=True)

from datetime import date, datetime

import mysql.connector
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "study_treasure_secure_secret_key"

# MySQL Database Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Prakrati11",
    "database": "study_treasure",
}


def get_db():
    conn = mysql.connector.connect(**db_config)
    return conn


# ==========================================
# DAILY CONSECUTIVE STREAK UPDATE FUNCTION
# ==========================================
def update_student_streak(student_email):
    today = date.today()
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT current_streak, last_active_date FROM students WHERE email = %s",
            (student_email,),
        )
        student = cursor.fetchone()

        if not student:
            cursor.close()
            conn.close()
            return 0

        current_streak = student.get("current_streak", 0) or 0
        last_date = student.get("last_active_date")

        # Safe conversion: Ensure last_date is a datetime.date object
        if isinstance(last_date, datetime):
            last_date = last_date.date()
        elif isinstance(last_date, str):
            try:
                last_date = datetime.strptime(last_date.split()[0], "%Y-%m-%d").date()
            except ValueError:
                last_date = None

        new_streak = current_streak

        if last_date is None:
            new_streak = 1
        elif last_date == today:
            new_streak = current_streak
        elif last_date == date.fromordinal(today.toordinal() - 1):
            new_streak = current_streak + 1
        else:
            new_streak = 1

        # Database update
        cursor.execute(
            """
            UPDATE students 
            SET current_streak = %s, last_active_date = %s 
            WHERE email = %s
        """,
            (new_streak, today, student_email),
        )
        conn.commit()
        cursor.close()
        conn.close()

        # Update session so navbar reflects it immediately
        session["student_streak"] = new_streak
        return new_streak
    except mysql.connector.Error as err:
        print("Error updating streak:", err)
        return session.get("student_streak", 0)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form["full_name"].strip()
        roll_number = request.form["roll_number"].strip()
        email = request.form["email"].strip()
        student_class = request.form["student_class"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if len(password) < 6:
            return "Password must be at least 6 characters long! <a href='/register'>Go Back</a>"

        if password != confirm_password:
            return "Passwords do not match! <a href='/register'>Go Back</a>"

        try:
            conn = get_db()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM students WHERE email = %s OR roll_number = %s",
                (email, roll_number),
            )
            existing_user = cursor.fetchone()

            if existing_user:
                cursor.close()
                conn.close()
                return "Error: Email or Roll Number already registered! Please use unique credentials. <a href='/register'>Go Back</a>"

            password_hash = generate_password_hash(password)

            query = """
                INSERT INTO students (full_name, roll_number, email, student_class, password_hash, total_coins, current_streak) 
                VALUES (%s, %s, %s, %s, %s, 0, 0)
            """
            cursor.execute(
                query, (full_name, roll_number, email, student_class, password_hash)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for("home"))
        except mysql.connector.Error as err:
            return f"Database Error: {err} <a href='/register'>Try Again</a>"

    return render_template("student_register.html")


@app.route("/faculty/register", methods=["GET", "POST"])
def faculty_register():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        faculty_id = request.form.get("faculty_id", "").strip()
        email = request.form.get("email", "").strip()
        department = request.form.get("department")

        classes_list = request.form.getlist("classes_taught")
        classes_taught = ", ".join(classes_list)

        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if len(password) < 6:
            return "Password must be at least 6 characters long! <a href='/faculty/register'>Go Back</a>"

        if password != confirm_password:
            return "Passwords do not match! <a href='/faculty/register'>Go Back</a>"

        try:
            conn = get_db()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM faculty WHERE email = %s OR faculty_id = %s",
                (email, faculty_id),
            )
            existing_faculty = cursor.fetchone()

            if existing_faculty:
                cursor.close()
                conn.close()
                return "Error: Email or Faculty ID already registered! Please use unique credentials. <a href='/faculty/register'>Go Back</a>"

            password_hash = generate_password_hash(password)

            query = """
                INSERT INTO faculty (full_name, faculty_id, email, department, classes_taught, password_hash) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                query,
                (
                    full_name,
                    faculty_id,
                    email,
                    department,
                    classes_taught,
                    password_hash,
                ),
            )
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for("home"))
        except mysql.connector.Error as err:
            return f"Database Error: {err} <a href='/faculty/register'>Try Again</a>"

    return render_template("faculty_register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form.get("role")
        email = request.form.get("email")
        password = request.form.get("password")

        if role == "student":
            try:
                conn = get_db()
                cursor = conn.cursor(dictionary=True)
                query = "SELECT * FROM students WHERE email = %s"
                cursor.execute(query, (email,))
                student = cursor.fetchone()
                cursor.close()
                conn.close()

                if student:
                    if check_password_hash(student["password_hash"], password):
                        session["student_email"] = student["email"]
                        session["student_id"] = student["id"]
                        session["student_class"] = str(student["student_class"]).strip()
                        session["student_name"] = student["full_name"]
                        session["student_coins"] = student.get("total_coins", 0)
                        session["student_streak"] = (
                            student.get("current_streak", 0) or 0
                        )
                        return render_template(
                            "login.html",
                            alert_message="Welcome back, You Successfully Logged in",
                            redirect_url=url_for("subjects"),
                        )
                    else:
                        return render_template(
                            "login.html",
                            alert_message="Incorrect password",
                            redirect_url=url_for("login"),
                        )
                else:
                    return render_template(
                        "login.html",
                        alert_message="Email not found!",
                        redirect_url=url_for("login"),
                    )
            except mysql.connector.Error as err:
                return render_template(
                    "login.html",
                    alert_message=f"Database Error: {err}",
                    redirect_url=None,
                )

        elif role == "faculty":
            try:
                conn = get_db()
                cursor = conn.cursor(dictionary=True)
                query = "SELECT * FROM faculty WHERE email = %s"
                cursor.execute(query, (email,))
                faculty = cursor.fetchone()
                cursor.close()
                conn.close()

                if faculty and check_password_hash(faculty["password_hash"], password):
                    session["faculty_name"] = faculty["full_name"]
                    session["faculty_classes"] = faculty["classes_taught"]
                    return render_template(
                        "login.html",
                        alert_message="Welcome back, Faculty Login Successful",
                        redirect_url=url_for("faculty_dashboard"),
                    )
                else:
                    return render_template(
                        "login.html",
                        alert_message="Invalid credentials",
                        redirect_url=url_for("home"),
                    )
            except mysql.connector.Error as err:
                return render_template(
                    "login.html",
                    alert_message=f"Database Error: {err}",
                    redirect_url=url_for("home"),
                )
        else:
            return redirect(url_for("home"))

    return render_template("login.html", alert_message=None, redirect_url=None)


# ==========================================
# ACTIVE GAME COMPLETION API FOR STREAK & COINS
# ==========================================
@app.route("/api/complete_game", methods=["POST"])
def complete_game():
    if "student_email" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json or {}
    earned_coins = data.get("coins", 15)
    email = session.get("student_email")

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE students SET total_coins = total_coins + %s WHERE email = %s",
            (earned_coins, email),
        )
        conn.commit()
        cursor.close()
        conn.close()

        session["student_coins"] = session.get("student_coins", 0) + earned_coins
        new_streak = update_student_streak(email)

        return jsonify(
            {
                "status": "success",
                "streak": new_streak,
                "coins": session["student_coins"],
            }
        )
    except mysql.connector.Error as err:
        print("Error completing game:", err)
        return jsonify({"status": "error", "message": str(err)}), 500


@app.route("/faculty/dashboard")
def faculty_dashboard():
    faculty_name = session.get("faculty_name")
    faculty_classes_str = session.get("faculty_classes", "")

    if not faculty_name:
        return redirect(url_for("login"))

    allowed_numbers = []
    for c in faculty_classes_str.split(","):
        digits = "".join([ch for ch in c if ch.isdigit()])
        if digits:
            allowed_numbers.append(digits)

    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT full_name, roll_number, email, student_class, total_coins, current_streak FROM students"
        )
        all_students = cursor.fetchall()
        cursor.close()
        conn.close()

        filtered_students = []
        for s in all_students:
            s_class = str(s["student_class"]).strip()
            s_digits = "".join([ch for ch in s_class if ch.isdigit()])
            if s_digits in allowed_numbers:
                filtered_students.append(s)

        return render_template(
            "faculty_dashboard.html",
            faculty_name=faculty_name,
            classes=faculty_classes_str,
            students=filtered_students,
        )
    except mysql.connector.Error as err:
        return f"Error loading analytics: {err}"


@app.route("/subjects")
def subjects():
    student_class = session.get("student_class", "")
    student_name = session.get("student_name", "")
    student_coins = session.get("student_coins", 0)
    return render_template(
        "subjects.html",
        student_class=student_class,
        student_name=student_name,
        student_coins=student_coins,
    )


@app.route("/subject/mathematics")
def math_hub():
    student_class = str(session.get("student_class", "")).lower()
    if "6" in student_class:
        return render_template("class6_math.html")
    return "No Quiz and Games uploaded"


@app.route("/subject/science")
def science_hub():
    student_class = str(session.get("student_class", "")).lower()
    if "11" in student_class or "12" in student_class:
        return redirect(url_for("attempt_quiz"))
    elif "7" in student_class:
        return redirect(url_for("class7_chemistry"))
    elif "8" in student_class:
        return redirect(url_for("class8_physics"))
    else:
        return redirect(url_for("attempt_quiz"))


@app.route("/class7/chemistry")
def class7_chemistry():
    return render_template("class7_chemistry.html")


@app.route("/class8/physics")
def class8_physics():
    return render_template("class8_physics.html")


@app.route("/game/geometry-quest")
def geometry_quest():
    if "student_email" not in session:
        return redirect(url_for("login"))
    return render_template(
        "geometry_quest.html",
        student_name=session.get("student_name", ""),
        student_coins=session.get("student_coins", 0),
        student_streak=session.get("student_streak", 0),
    )


@app.route("/game/litmus-lab")
def litmus_lab():
    if "student_email" not in session:
        return redirect(url_for("login"))
    return render_template(
        "litmus_lab.html",
        student_name=session.get("student_name", ""),
        student_coins=session.get("student_coins", 0),
        student_streak=session.get("student_streak", 0),
    )


@app.route("/game/circuit-builder")
def circuit_builder():
    if "student_email" not in session:
        return redirect(url_for("login"))
    return render_template(
        "circuit_builder.html",
        student_name=session.get("student_name", ""),
        student_coins=session.get("student_coins", 0),
        student_streak=session.get("student_streak", 0),
    )


@app.route("/attempt-quiz")
def attempt_quiz():
    student_class = str(session.get("student_class", "")).lower()
    return render_template("attempt_quiz.html", student_class=student_class)


@app.route("/quiz/<chapter>")
def quiz_page(chapter):
    session["quiz_slot"] = {
        "chapter": chapter.strip(),
        "current_q_index": 0,
        "total_questions": 5,
        "coins": 0,
        "streak": 0,
        "asked_ids": [],
        "current_difficulty": "medium",
    }
    return render_template(
        "quiz.html",
        chapter=chapter,
        student_name=session.get("student_name", "Student"),
    )


@app.route("/api/get_question", methods=["GET"])
def get_question():
    try:
        slot = session.get("quiz_slot")
        if not slot:
            slot = {
                "chapter": "Solutions",
                "current_q_index": 0,
                "total_questions": 5,
                "coins": 0,
                "streak": 0,
                "asked_ids": [],
                "current_difficulty": "medium",
            }
            session["quiz_slot"] = slot

        if slot["current_q_index"] >= slot["total_questions"]:
            earned_coins = slot["coins"]
            email = session.get("student_email")
            if email and earned_coins > 0:
                try:
                    conn = get_db()
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE students SET total_coins = total_coins + %s WHERE email = %s",
                        (earned_coins, email),
                    )
                    conn.commit()
                    cursor.close()
                    conn.close()

                    session["student_coins"] = (
                        session.get("student_coins", 0) + earned_coins
                    )
                    update_student_streak(email)
                except mysql.connector.Error as db_err:
                    print("Error updating score and streak:", db_err)

            return jsonify({"status": "completed", "total_coins": slot["coins"]})

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        raw_chapter = str(slot["chapter"]).strip()
        excluded_ids = slot["asked_ids"] if slot["asked_ids"] else [0]
        format_strings = ",".join(["%s"] * len(excluded_ids))
        target_diff = slot["current_difficulty"].strip().lower()

        query = f"""
            SELECT * FROM questions 
            WHERE (LOWER(chapter) = LOWER(%s) OR REPLACE(LOWER(chapter), ' ', '') = REPLACE(LOWER(%s), ' ', '')) 
              AND LOWER(difficulty) = %s 
              AND id NOT IN ({format_strings})
            ORDER BY RAND() LIMIT 1
        """
        cursor.execute(query, [raw_chapter, raw_chapter, target_diff] + excluded_ids)
        q = cursor.fetchone()

        if not q:
            fallback_query1 = f"""
                SELECT * FROM questions 
                WHERE (LOWER(chapter) = LOWER(%s) OR REPLACE(LOWER(chapter), ' ', '') = REPLACE(LOWER(%s), ' ', '')) 
                  AND id NOT IN ({format_strings})
                ORDER BY RAND() LIMIT 1
            """
            cursor.execute(fallback_query1, [raw_chapter, raw_chapter] + excluded_ids)
            q = cursor.fetchone()

        if not q:
            fallback_query2 = f"""
                SELECT * FROM questions 
                WHERE id NOT IN ({format_strings})
                ORDER BY RAND() LIMIT 1
            """
            cursor.execute(fallback_query2, excluded_ids)
            q = cursor.fetchone()

        cursor.close()
        conn.close()

        if not q:
            return jsonify({"status": "completed", "total_coins": slot["coins"]})

        slot["asked_ids"].append(q["id"])
        session["current_question"] = q
        session.modified = True

        return jsonify(
            {
                "status": "success",
                "question_number": slot["current_q_index"] + 1,
                "total_slot_questions": slot["total_questions"],
                "question_text": q["question_text"],
                "options": [q["option_a"], q["option_b"], q["option_c"], q["option_d"]],
                "difficulty": q["difficulty"],
                "coins": slot["coins"],
                "streak": slot["streak"],
            }
        )
    except mysql.connector.Error as err:
        print("ERROR in /api/get_question:", str(err))
        return jsonify({"status": "error", "message": str(err)}), 500


@app.route("/api/submit_answer", methods=["POST"])
def submit_answer():
    try:
        data = request.json
        selected_idx = data.get("selected")

        slot = session.get("quiz_slot")
        curr_q = session.get("current_question")

        if not slot or not curr_q:
            return jsonify({"error": "Invalid Session"}), 400

        is_correct = selected_idx == curr_q["correct_answer"]

        if is_correct:
            slot["streak"] += 1
            earned = curr_q["reward_coins"] + (5 * slot["streak"])
            slot["coins"] += earned
        else:
            slot["streak"] = 0

        current_diff = slot["current_difficulty"].lower()

        if is_correct:
            if current_diff == "medium" or current_diff == "hard":
                slot["current_difficulty"] = "hard"
            elif current_diff == "easy":
                slot["current_difficulty"] = "medium"
        else:
            if current_diff == "hard":
                slot["current_difficulty"] = "medium"
            elif current_diff == "medium" or current_diff == "easy":
                slot["current_difficulty"] = "easy"

        slot["current_q_index"] += 1
        session.modified = True

        return jsonify(
            {
                "is_correct": is_correct,
                "correct_answer": curr_q["correct_answer"],
                "coins": slot["coins"],
                "streak": slot["streak"],
                "next_difficulty": slot["current_difficulty"],
            }
        )
    except Exception as e:
        print("ERROR in /api/submit_answer:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/api/sync_offline_progress", methods=["POST"])
def sync_offline_progress():
    data = request.get_json() or {}

    student_id = data.get("student_id")
    points_earned = data.get("points_earned", 0)
    streak_count = data.get("streak_count", 0)

    if not student_id:
        return jsonify({"status": "error", "message": "Student ID missing"}), 400

    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            UPDATE students 
            SET total_coins = total_coins + %s, 
                current_streak = GREATEST(current_streak, %s) 
            WHERE id = %s
        """,
            (points_earned, streak_count, student_id),
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify(
            {"status": "success", "message": "Progress synced successfully!"}
        )
    except mysql.connector.Error as err:
        print("Database sync error:", err)
        return jsonify({"status": "error", "message": str(err)}), 500

if __name__ == "__main__":
    app.run(debug=True)