from flask_restful import Resource, reqparse, inputs

from api.sql import SQLConnection

conn = SQLConnection('test')


class Pay(Resource):

    def post(self, **kwargs):
        args = _post_parser().parse_args()
        if not args['user_id'] or not args['account_id']:
            return {'error': 'Not user_id or account_id'}, 400
        result = {'user_id': args['user_id'], 'accounts': {'debit': [], 'credit': []}}
        query = """
            SELECT ac.amount, ac.debt, ac.account_type_id FROM Account AS ac 
            WHERE ac.user_id = {user_id}
            AND ac.account_id = {account_id}
        """
        accounts = conn.execute(query=query.format(user_id=args['user_id'], account_id=args['account_id']))
        if accounts and len(accounts) > 0:
            for account in accounts:
                # debit
                if account[2] == 1:
                    if 0 <= args['amount'] < 0:
                        self.update_amount(args['user_id'], args['account_id'], account[0], args['amount'])
                        return {'status': 'OK'}, 202
                    else:
                        return {'error': 'The amount requested is mayor that the amount in your account'}, 400
                # credit
                elif 0 <= account[2] == 2:
                    if args['amount'] <= account[0]*1.1:
                        self.update_amount_credit_card(args['user_id'], args['account_id'], account[0], account[1], args['amount'])
                    else:
                        return {'error': 'The amount requested is mayor that the amount in your account'}, 400
        return result, 200

    @staticmethod
    def update_amount(user_id, account_id, amount, pay):
        query = """
            UPDATE Account SET amount = {amount}
            WHERE ac.user_id = {user_id}
            AND ac.account_id = {account_id}
        """
        return conn.execute(query=query.format(amount=amount+pay, user_id=user_id, account_id=account_id), commit=True)

    @staticmethod
    def update_amount_credit_card(user_id, account_id, amount, debt, pay):
        query = """
                    UPDATE Account SET amount = {amount}, debt = {debt}
                    WHERE ac.user_id = {user_id}
                    AND ac.account_id = {account_id}
                """
        return conn.execute(query=query.format(amount=amount+pay, user_id=user_id, account_id=account_id, debt=debt-pay), commit=True)


def _post_parser():
    parser = reqparse.RequestParser(bundle_errors=True).copy()
    parser.add_argument('user_id', type=int, default=-1)
    parser.add_argument('account_id', type=int, default=-1)
    parser.add_argument('amount', type=float, default=0)
    return parser