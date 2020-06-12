from flask import render_template, request, make_response
from . import api


# ################################################################################
# Error Handlers
# ################################################################################


@api.app_errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = make_response({'error': "not found"})
        response.status_code = 404
        return response
    return render_template('404.html'), 404

@api.app_errorhandler(405)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = make_response({'error': "method not allowed"})
        response.status_code = 405
        return response
    return render_template('404.html'), 405



@api.app_errorhandler(500)
def internal_server_error(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = make_response({'error': "internal error"})
        response.status_code = 500
        return response
    return render_template('500.html'), 500
