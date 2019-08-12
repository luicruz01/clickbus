from flask_restful import Resource, reqparse, inputs

from api.sql import SQLConnection

conn = SQLConnection('test')


class User(Resource):

    def get(self, **kwargs):
        args = _get_parser().parse_args()
        if not args['user_name'] or not args['password']:
            return {'error': 'Not user_name or password'}, 400
        query = """
            SELECT us.user_id FROM User AS us
            WHERE us.user_name = {user_name}
            AND us.password = '{password}'
        """
        user = conn.execute(query=query.format(user_name=args['user_name'], password=args['password']))
        if user[0][0]:
            return {'user_id': user[0][0]}, 200
        return {'error': 'User not found'}, 404


def _get_parser():
    parser = reqparse.RequestParser(bundle_errors=True).copy()
    parser.add_argument('user_name', type=str, default=None)
    parser.add_argument('password', type=str, default=None)
    return parser