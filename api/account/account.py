from flask_restful import Resource, reqparse, inputs

from api.sql import SQLConnection

conn = SQLConnection('test')


class Account(Resource):

    def get(self, **kwargs):
        args = _get_parser().parse_args()
        if not args['user_id'] or not args['account_id']:
            return {'error': 'Not user_id or account_id'}, 400
        result = {'user_id': args['user_id'], 'accounts': {'debit': [], 'credit': []}}
        query = """
            SELECT ac.amount, ac.debt, ac.account_type_id, ac.account_id FROM Account AS ac 
            WHERE ac.user_id = {user_id}
            AND ac.account_id = {account_id}
        """
        accounts = conn.execute(query=query.format(user_id=args['user_id'], account_id=args['account_id']))
        if accounts and len(accounts) > 0:
            for account in accounts:
                # debit
                if account[2] == 1:
                    result['accounts']['debit'].append({
                        'account_id': account[3],
                        'amount': account[0]
                    })
                elif account[2] == 2:
                    result['accounts']['credit'].append({
                        'account_id': account[3],
                        'amount': account[0],
                        'debt': account[1]
                    })
        return result, 200


def _get_parser():
    parser = reqparse.RequestParser(bundle_errors=True).copy()
    parser.add_argument('user_id', type=int, default=-1)
    parser.add_argument('account_id', type=int, default=-1)
    return parser
