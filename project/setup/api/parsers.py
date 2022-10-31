from flask_restx.inputs import email
from flask_restx.reqparse import RequestParser

page_parser: RequestParser = RequestParser()
page_parser.add_argument(name='page', type=int, location='args', required=False)

auth_parser: RequestParser = RequestParser()
auth_parser.add_argument(name='email', type=email(), required=True, nullable=False)
auth_parser.add_argument(name='password', type=str, required=True, nullable=False)

