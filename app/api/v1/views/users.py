"""
    This module holds the views for the users
"""
from flask_restful import Resource, reqparse, Api
from flask_jwt_extended import (jwt_required, get_jwt_identity,
 jwt_refresh_token_required, get_raw_jwt, create_access_token)
from flask import request, Flask, jsonify
from app.api.v1.models.users import UserModel, RevokedTokenModel
from app.api.v1.validators.validators import Validate

app = Flask(__name__)
api = Api(app)


class Users(Resource):
    """
        This class defines methods for getting all users and signing up
    """

    # @api.doc(params={
    #                 'username': 'Enter a unique username',
    #                 'email': 'Enter email',
    #                 'phoneNumber': 'Enter phone number',
    #                 'password': 'Enter password'
    #                 })
    def post(self):
        """
            This method registers a user to the database.
        """

        parser = reqparse.RequestParser(bundle_errors=True)

        parser.add_argument("username",
                            type=str,
                            required=True,
                            help="Username field is required.")
        parser.add_argument("password",
                            type=str,
                            required=True,
                            help="Password field is required.")
        parser.add_argument("email",
                            type=str,
                            required = True,
                            help="Email field is required.")
        parser.add_argument("phoneNumber",
                            type=int,
                            help="Phone number field is optional.")

        args = parser.parse_args()
        users = UserModel(**args)
        Valid = Validate()
        username = args.get('username').strip()
        email    = args.get('email').strip()
        password = args.get('password').strip()
        phoneNumber = str(args.get('phoneNumber')).strip()
        if not request.json:
            return {'status': 400,"error" : "check your request type"},400
        if not email or not Valid.valid_string(username) or not bool(username) :
            return {'status': 400,"error" : "Username is invalid or empty"}, 400
        if not Valid.check_phone(phoneNumber):
            return {'status': 400, 'error': 'phone number is invalid, start at [7] like 712345678'},400
        if not Valid.valid_email(email) or not bool(email):
            return {'status': 400,"error" : "Email is invalid or empty!"}, 400
        if not Valid.valid_password(password) or not bool(password):
            return {'status': 400,
            "error" : "Password is should contain atleast 8 characters"}, 400

        if users.find_by_username(username):
            return {"status": 400,  "error": "Username already in use." }, 400
        if users.find_by_email(email):
            return {"status": 400, "error": "Email already in use."}, 400
        token = users.save_to_db()
        if token:
            return {"status": 201,
                    "data": [
                        {
                            "id" : users.find_user_id(username),
                            "token": "Bearer"+" "+ token
                        }],
                        "message": 'User created Succesfully.'
                    }, 201
        return {"status":500, "error": "Oops! something went Wrong!"},500


class User(Resource):
    """
        This class defines mthods for login in
    """

    def post(self):
        """
            This method logs in the user
        """

        parser = reqparse.RequestParser(bundle_errors=True)

        parser.add_argument("username",
                            type=str,
                            required=True,
                            help="Username field is required.")
        parser.add_argument("password",
                            type=str,
                            required=True,
                            help="Password field is required.")

        args = parser.parse_args()
        users = UserModel(**args)
        Valid = Validate()

        username = args.get('username').strip()
        password = args.get('password').strip()

        if not request.json:
            return jsonify({"error" : "check your request type"})

        if not Valid.valid_string(username) or not bool(username) :
            return {"error" : "Username is invalid or empty"}, 400

        if not Valid.valid_password(password) or not bool(password):
            return {
                "error" : "Passord is should contain atleast 8 characters, a letter, a number and a special character"}, 400

        if not users.find_by_username(username):
            return {"status": 404, "error": "user not found"}, 404
        if not users.check_password_match(username, password):
            return {"status": 401, "error": "wrong credntials!"}, 401
        user_id = users.find_user_id(username)
        token = users.login_user(username)
        if token:
            return {"status": 200,
                        "data": [{
                            "id": user_id,
                            "access_token": "Bearer"+" "+ token["access_token"]
                        }],
                        "message": "successful"}, 201
        return {"status":500, "error": "Oops! something went Wrong!"},500

    @jwt_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        try:
            RevokedTokenModel().revoke_token(jti)
            return {"status": 200,
                        "message": "successful logout"}, 2
        except:
            return {'error': 'Something went wrong'}, 500

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {"status": 200,
                        "data": [{
                            "user": current_user,
                            "access_token": "Bearer"+" "+ access_token
                        }],
                        "message": "successful"}, 201

    @jwt_refresh_token_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        try:
            RevokedTokenModel().revoke_token(jti)
            return {'message': 'User successfuly logged out'}
        except:
            return {'message': 'Something went wrong'}, 500

class ViewUsers(Resource):
    """
        manage all users
    """
    @jwt_required
    def get(self):
        """
             view al users
        """
        self.users = UserModel()
        users = self.users.get_all_users()
        if not users:
            return {
                "status": 404,
                "error": "No users found"
            },404
        return jsonify({
            "status":200,
            "data":[{
                "users": users
            }],
            "message": "All users found Successfully"
        }
        )
   

class ManageUsers(Resource):
    """
        manage specific users
    """
    
    @jwt_required
    def get(self, user_id):
        """
            get a single user
        """
        id = get_jwt_identity()   
        self.user = UserModel()
        user = self.user.find_user_by_id(user_id)
        admin = self.user.find_user_role(id)
        print(admin)
        if not admin:
            return {
                "status":403,
                "error": "This action is forbidden"
            }, 403
        if not user:
            return {
                "status":404,
                "error": "User not found"
            }, 404
        return jsonify({
            "status":200,
            "data":[{
                "user":user
            }],
            "message":"User successfully retieved"
        })
        
    @jwt_required
    def patch(self, user_id):
        """
            change user status to admin
        """
        id = get_jwt_identity()
        self.user = UserModel()
        user = self.user.find_user_by_id(user_id)
        user_role = self.user.find_user_role(user_id)
        admin = self.user.find_user_role(id)
        if not admin or id !=1 or user_id ==1:
            return {
                "status":403,
                "error": "This action is forbidden"
            }, 403
        if not user:
            return {
                "status": 404,
                "error": "User not found"
            },404
        if user_role:
            return {
                "status": 200,
                "error":"User is already an Admin"
            }, 200
        self.user.promote_user(user_id)
        return {
            "status": 200,
            "message": "User "+ str(user_id)+" successfully promoted to admin"
        }

    
    @jwt_required
    def delete(self, user_id):
        """
            delete a user
        """
        id = get_jwt_identity()
        self.user = UserModel()
        user = self.user.find_user_by_id(user_id)
        admin = self.user.find_user_role(id)
        if not admin or user_id == 1:
            return {
                "status":403,
                "error": "This action is forbidden"
            }, 403
        if not user:
            return {
                "status": 404,
                "error": "User not found"
            },404
        self.user.delete_user(user_id)
        return {
            "status": 200,
            "message": "User successfully deleted"
        }