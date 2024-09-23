from config import *
from web_contollers.api_tools.wraplers import *

@cross_origin
@app.route('/addCamera', methods=['POST']) 
@exception_processing
def addCamera():
    return {request.path: True}