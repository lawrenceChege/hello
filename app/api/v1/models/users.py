"""
    This module holds the Model for the Users
"""
import time
import psycopg2
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash
from migrations import DbModel




class UserModel(DbModel):
    """
        This class manages the data for the users
    """

    def __init__(self, active=False,  isAdmin=False,email=None,
                phoneNumber=None, username=None, password=None):
        super().__init__()
        self.active = active
        self.email = email
        self.password = password
        self.phoneNumber = phoneNumber
        self.username = username
        self.registered = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.isAdmin = isAdmin
        


    def generate_pass_hash(self):
        """
        encrypt password
        """

        private_key = generate_password_hash(request.json.get("password"))
        self.password = private_key
        return self.password

    def check_password_match(self, username, password):
        """
        Check if pass match
        :param :password: password
        return: Boolean
        """
        self.password = self.get_password(username).get('btrim')
        match = check_password_hash(self.password, password)
        return match

    def generate_access_token(self, username):
        self.user_id = self.find_user_id(username)
        token = create_access_token(identity=self.user_id)
        return token

    def generate_refresh_token(self, username):
        self.user_id = self.find_user_id(username)
        token = create_refresh_token(identity=self.user_id)
        return token

    def get_password(self, username):
        """ gets hash password from db """
        try:
            self.cur.execute(
                "SELECT TRIM(password) FROM users WHERE user_name=%s", (username,)
                )
            password = self.findOne()
            return password
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None

    def get_all_users(self):
        """
            get all users
        """
        try:
            self.cur.execute(
                "SELECT * FROM users"
            )
            users = self.findAll()
            return users
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None

    def find_user_id(self, username):
        """
        Find user  id
        """
        try:
            self.cur.execute(
                "SELECT user_id FROM users WHERE user_name=%s", (username,)
                )
            user_id = self.findOne()
            id = user_id.get('user_id')
            return id
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None
    def find_user_by_id(self, user):
        """
        Find user email and phoneNumber
        """
        try:
            self.cur.execute(
                "SELECT * FROM users WHERE user_id=%s", (user,)
                )
            self.user = self.findOne()
            return self.user
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None
    
    def find_user_role(self, user):
        """
        Find user role
        """
        try:
            self.cur.execute(
                "SELECT isAdmin FROM users WHERE user_id=%s", (user,)
                )
            user_role = self.findOne()
            isAdmin = user_role.get('isadmin')
            return isAdmin
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None

    def find_by_email(self,email):
        """
        Find user by email
        """
        try:
            self.cur.execute(
                "SELECT TRIM(user_email) FROM users WHERE user_email=%s", (email,)
                )
            email = self.findOne()
            return email
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None

    def find_by_username(self, username):
        """
        Find user by username
        """
        try:
            self.cur.execute(
                "SELECT user_name FROM users WHERE user_name=%s", (username,)
                )
            username = self.findOne()
            return username
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None
    
    def promote_user(self, user_id):
        """
            make a user an admin
        """
        try:
            self.cur.execute(
                """
                    UPDATE users
                    SET
                    isAdmin = %s
                    WHERE
                    user_id = %s;
                """,("True", user_id,)
            )
            self.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None

    def delete_user(self, user_id):
        """
            delete a user
        """
        try:
            self.cur.execute(
                """
                    DELETE * FROM users
                    WHERE
                    user_id = %s;
                """,(user_id,)
            )
            self.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None

    def save_to_db(self):
        """
            This method saves the user to the database.
        """
        self.generate_pass_hash()
        try:
            data =(self.username, self.email, self.phoneNumber, self.password, self.registered, self.isAdmin, self.active, )
            self.cur.execute(
                """
                    INSERT INTO users (user_name, user_email, user_phone, password, created_at, is_Admin, active)
                    VALUES(%s, %s, %s, %s, %s, %s, %s);
                """, data
            )
            self.commit()
            self.token = self.generate_access_token(self.username)
            return self.token
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('Error creating user in database')

    def login_user(self, username):
        """
            This method logs in the user.
            It takes username and password as parameters and
            It returns jwt token
        """
        access_token = self.generate_access_token(username)
        refresh_token = self.generate_refresh_token(username)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def uplink_company(self, company_id, user_id):
        """
            Link user to company
        """
        try:
            self.cur.execute(
                """
                    UPDATE users
                    SET
                    company_id= %s
                    WHERE
                    user_id = %s;
                """,(company_id, user_id,)
            )
            self.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None


class RevokedTokenModel(DbModel):
    """
        Revoke tokens
    """
    def __init__(self):
        super().__init__()

    def find_revoked_token(self, token):
        """
        Find token in revoked tokens
        """
        try:
            self.cur.execute(
                "SELECT token FROM revoked_tokens WHERE token=%s", (token,)
                )
            token = self.findOne()
            return token
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None

    def is_jti_blacklisted(self, token):
        query = self.find_revoked_token(token)
        return bool(query)

    def revoke_token(self, token):
        """
            This method revokes a token.
        """
        try:
            self.cur.execute(
                """
                    INSERT INTO revoked_tokens (token)
                    VALUES(%s);
                """, (token,)
            )
            self.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('Error creating user in database')