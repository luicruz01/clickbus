# -*- coding: utf-8 -*-

from flask import request


def support_jsonp(api_instance, callback_name_source='callback'):
    """ Let API instance can respond jsonp request automatically.
    `callback_name_source` can be a string or a callback.
        If it is a string, the system will find the argument that named by this string in `query string`.
         If found, determine this request to be a jsonp request, and use the argument's value as the js callback name.
        If `callback_name_source` is a callback, this callback should return js callback name when request
         is a jsonp request, and return False when request is not jsonp request.
         And system will handle request according to its return value.
    default support format：url?callback=js_callback_name

    :param api_instance: API flask_api instance
    :param callback_name_source: string
    :return: HTTP response
    """
    output_json = api_instance.representations['application/json']

    @api_instance.representation('application/json')
    def handle_jsonp(data, code, headers=None):
        resp = output_json(data, code, headers)

        callback = request.args.get(callback_name_source, False)
        if callback:
            resp.set_data(str(callback) + '(' + resp.get_data().decode("utf-8") + ')')

        return resp
