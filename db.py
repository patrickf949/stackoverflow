import psycopg2
from pprint import pprint
import os


class DatabaseConnection:

    def __init__(self):
        # if os.getenv('APP_SETTINGS') == 'test_db':
        #     self.db = 'test_db'
        # else:
        #     self.db = 'stackoverflow'

        try:
            self.connection = psycopg2.connect(
                dbname='ddhe72t8a8473k', user='casrdwnqztpfjp', host='ec2-23-23-101-25.compute-1.amazonaws.com', password='7d28e10dfc21e8c32555be04944aec2b5763a18f124236395129befb00319024', port='5432'
            )

            self.connection.autocommit = True
            self.cursor = self.connection.cursor()

            pprint('Database connected.')
            create_user_table = "CREATE TABLE IF NOT EXISTS users (userId TEXT NOT NULL PRIMARY KEY, username TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL);"
            create_answers_table = "CREATE TABLE IF NOT EXISTS answers (answerId SERIAL NOT NULL PRIMARY KEY, details TEXT NOT NULL, questionId INTEGER NOT NULL, username TEXT NOT NULL, fav BOOLEAN NOT NULL DEFAULT 'False');"
            create_questions_table = "CREATE TABLE IF NOT EXISTS questions (questionId SERIAL NOT NULL PRIMARY KEY, details TEXT NOT NULL, username TEXT NOT NULL);"

            self.cursor.execute(create_user_table)
            self.cursor.execute(create_questions_table)
            self.cursor.execute(create_answers_table)

        except:
            pprint('Cannot connect to the database.')

    def insert_users(self, userId, username, email, password):
        insert_user = "INSERT INTO users(userId, username, email, password) VALUES('{}', '{}', '{}', '{}')".format(
            userId, username, email, password)
        pprint(insert_user)
        self.cursor.execute(insert_user)

    def insert_question(self, details, username):
        insert_question = "INSERT INTO questions(details, username) VALUES('{}', '{}')".format(
            details, username)
        pprint(insert_question)
        self.cursor.execute(insert_question)

    def login(self, username):
        query = "SELECT * FROM users WHERE username='{}'".format(username)
        pprint(query)
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        return user

    def user(self, username):
        query = "SELECT username FROM users WHERE username='{}'".format(
            username)
        pprint(query)
        self.cursor.execute(query)
        userId = self.cursor.fetchone()
        return userId

    def check_username(self, username):
        query = "SELECT username FROM users WHERE username='{}'".format(
            username)
        pprint(query)
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        return user

    def check_email(self, email):
        query = "SELECT email FROM users WHERE email='{}'".format(email)
        pprint(query)
        self.cursor.execute(query)
        email = self.cursor.fetchone()
        return email

    def check_question(self, username):
        query = "SELECT details FROM questions WHERE username='{}'".format(
            username)
        pprint(query)
        self.cursor.execute(query)
        questions = self.cursor.fetchall()
        return questions

    def insert_answer(self, details, username, questionId):
        insert_answer = "INSERT INTO answers(details, username, questionId) VALUES('{}','{}','{}')".format(
            details, username, questionId)
        pprint(insert_answer)
        self.cursor.execute(insert_answer)

    def get_answers(self, questionId):
        query = "SELECT * FROM answers WHERE questionId='{}'".format(
            questionId)
        pprint(query)
        self.cursor.execute(query)
        answers = self.cursor.fetchall()
        return answers
    
    def get_an_answer(self, questionId):
        query_ans = "SELECT details FROM answers WHERE questionId='{}'".format(questionId)
        pprint(query_ans)
        self.cursor.execute(query_ans)
        answer = self.cursor.fetchone()
        return answer

    def get_a_question(self, questionId):
        query_qn = "SELECT details FROM questions WHERE questionId='{}'".format(questionId)
        pprint(query_qn)
        self.cursor.execute(query_qn)
        question = self.cursor.fetchone()
        return question

    def get_all_questions(self):
        query = "SELECT questionId, details FROM questions"
        pprint(query)
        self.cursor.execute(query)
        question = self.cursor.fetchall()
        return question

    def get_one_question(self, questionId):
        query = "SELECT * FROM questions WHERE questionId='{}'".format(
            questionId)
        pprint(query)
        self.cursor.execute(query)
        question = self.cursor.fetchone()
        return question

    def delete_question(self, questionId, username):
        query = "DELETE FROM questions WHERE questionId='{}' AND username='{}'".format(
            questionId, username)
        pprint(query)
        self.cursor.execute(query)

    def asked(self, questionId):
        query = "SELECT userId FROM questions WHERE questionId='{}'".format(
            questionId)
        pprint(query)
        self.cursor.execute(query)
        userId = self.cursor.fetchone()
        return userId

    def answered(self, answerId, questionId):
        query = "SELECT userId FROM answers WHERE answerId='{}' and questionId='{}'".format(
            answerId, questionId)
        pprint(query)
        self.cursor.execute(query)
        userId = self.cursor.fetchone()
        return userId

    def preferred(self, username):
        add_fav = "UPDATE answers SET fav='True' WHERE userId='{}'".format(
            username)
        pprint(add_fav)
        self.cursor.execute(add_fav)

    def edit_answer(self, details, username, questionId):
        edit_ans = "UPDATE answers SET details='{}' WHERE username='{}' and questionId='{}'".format(
            details, username, questionId)
        pprint(edit_ans)
        self.cursor.execute(edit_ans)

    def drop_tables(self):
        drop = "DROP TABLE users, questions, answers"
        pprint(drop)
        self.cursor.execute(drop)


if __name__ == '__main__':
    database_connection = DatabaseConnection()
