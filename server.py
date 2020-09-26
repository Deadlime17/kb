# -*- encoding: utf-8 -*-
# kb v0.1.3
# A knowledge base organizer
# Copyright © 2020, gnc.
# See /LICENSE for licensing information.

"""
kbAPI server module

:Copyright: © 2020, gnc.
:License: GPLv3 (see /LICENSE).
"""

import sys
sys.path.append('kb')

# Use the bottle framework
from bottle import get, post, request, run, route, abort

# Import the API functions
from kb.api.search import search
#from kb.api.add import add 

# Get the configuration for the knowledgebase
from kb.config import DEFAULT_CONFIG


parameters = dict(id="",
                    title = "",
                    category = "",
                    query = "",
                    tags = "",
                    author = "",
                    status = "",
                    no_color = False,
                    verbose = False)
# query -> filter for the title field of the artifact
# category -> filter for the category field of the artifact
# tags -> filter for the tags field of the artifact
# author -> filter for the author field of the artifact
# status -> filter for the status field of the artifact
# no_color -> determines whether  a color output is needed
# verbose -> determines if a verbose output is needed

"""
    This function converts an Artifact object to a Json document

    Arguments:
    self   - Artifact object

    Returns:
    A Json document
"""

def toJson(self):
    record = '{"id":%i,"title":"%s", "category":"%s","path":"%s","tags":"%s""status":"%s""author":"%s","template":"%s"}' % (self.id,self.title,self.category,self.path,self.tags,self.status, self.author,self.template)
    return record


"""
    This function constructs a response from thee results obtained by a core function
    
    Arguments:
    result   - Set of results

    Returns:
    Fully fledged Json response

"""

def constructResponse(results):
    response = '['
    for result in results:
        response = response + toJson(result) + ','
    response =  response[:-1] + ']'
    return response


@get('/list')
def getAll():
    results = search( parameters, config=DEFAULT_CONFIG)    
    if len(results) == 0:
        abort(404, "Knowledgebase empty.")
    else:
        return {'knowledge': constructResponse(results) }


@get('/list/category/<category>')
def getCategory(category = ''):

    parameters["category"]=category

    results = search( parameters, config=DEFAULT_CONFIG)
    if len(results) == 0:
        abort(404, "Category not Found.")
    else:
        return {'knowledge': constructResponse(results) }

@get('/list/tags/<tags>')
def getTags(tags = ''):
    parameters["tags"]=tags
    results = search( parameters, config=DEFAULT_CONFIG)
    if len(results) == 0:
        abort(404, "Tag(s) not Found.")
    else:
        return {'knowledge': constructResponse(results) }
@post('/add')
def addArtefact():
    data = request.body.json
    print (data)


# Start the server
run(host='localhost', port=8080, debug=True,reloader=True)
