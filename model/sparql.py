import requests
import json
import _conf as conf
from rdflib import Graph, Namespace


def query(sparql_query, format_mimetype='application/sparql-results+json'):
    """Make a SPARQL query"""
    auth = (conf.SPARQL_AUTH_USR, conf.SPARQL_AUTH_PWD)
    data = {'query': sparql_query}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': format_mimetype
    }
    try:
        r = requests.post(conf.SPARQL_QUERY_URI, auth=auth, data=data, headers=headers, timeout=1)
        if r.status_code != 200:
            return None
        else:
            return json.loads(r.content.decode('utf-8'))
    except Exception as e:
        raise e


def query_turtle(sparql_query):
    """Make a SPARQL query with turtle format response"""
    data = {'query': sparql_query, 'format': 'text/turtle'}
    auth = (conf.SPARQL_AUTH_USR, conf.SPARQL_AUTH_PWD)
    headers = {'Accept': 'text/turtle'}
    r = requests.post(conf.SPARQL_QUERY_URI, data=data, auth=auth, headers=headers, timeout=1)
    try:
        return r.content
    except Exception as e:
        raise


def insert(g, named_graph_uri=None):
    """ Securely insert a named graph into the DB"""
    if named_graph_uri is not None:
        data = {'update': 'INSERT DATA { GRAPH <' + named_graph_uri + '> { ' + g.serialize(format='nt').decode('utf-8') + ' } }'}
    else:  # insert into default graph
        data = {'update': 'INSERT DATA { ' + g.serialize(format='nt') + ' }'}
    auth = (conf.SPARQL_AUTH_USR, conf.SPARQL_AUTH_PWD)
    headers = {'Accept': 'text/turtle'}
    try:
        r = requests.post(conf.SPARQL_UPDATE_URI, headers=headers, data=data, auth=auth, timeout=1)
        if r.status_code != 200 and r.status_code != 201:
            raise Exception('The INSERT was not successful. The SPARQL _database\' error message is: ' + r.content)
        return True
    except requests.ConnectionError as e:
        print(str(e))
        raise Exception()


def update(sparql_update_query, format_mimetype='application/sparql-results+json'):
    """ Make a SPARQL update"""
    auth = (conf.SPARQL_AUTH_USR, conf.SPARQL_AUTH_PWD)
    data = {'update': sparql_update_query}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': format_mimetype
    }
    try:
        r = requests.post(conf.SPARQL_UPDATE_URI, auth=auth, data=data, headers=headers, timeout=1)
        return r.text
    except Exception as e:
        raise e


def total_orgs():
    orgs = '''
        PREFIX org: <http://www.w3.org/ns/org#>
        SELECT (COUNT(*) AS ?count)
        WHERE {{
            ?uri a org:Organization .
            MINUS {{ ?uri a <http://test.linked.data.gov.au/def/auorg#DirectorySubStructure> }}
            MINUS {{ ?uri a <http://test.linked.data.gov.au/def/auorg#DirectoryRole> }}
        }}
       '''
    data = query(orgs)
    if data is None:
        return None
    return int(data.get('results').get('bindings')[0].get('count').get('value'))


def total_boards():
    orgs = '''
        PREFIX auorg: <http://test.linked.data.gov.au/def/auorg#>
        SELECT (COUNT(*) AS ?count)
        WHERE {{
            ?uri a auorg:Board .
        }}
       '''
    data = query(orgs)
    if data is None:
        return None
    return int(data.get('results').get('bindings')[0].get('count').get('value'))


def total_persons():
    orgs = '''
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        SELECT (COUNT(*) AS ?count)
        WHERE {{
            ?uri a foaf:Person .
        }}
       '''
    data = query(orgs)
    if data is None:
        return None
    return int(data.get('results').get('bindings')[0].get('count').get('value'))


def total_portfolios():
    orgs = '''
        SELECT (COUNT(*) AS ?count)
        WHERE {{
            ?uri a <http://test.linked.data.gov.au/def/auorg#Portfolio> .
        }}
       '''
    data = query(orgs)
    if data is None:
        return None
    return int(data.get('results').get('bindings')[0].get('count').get('value'))


# TODO: change the dtc:description to rdfs:comment for all classes
def instance_details(uri):
    q = '''
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX auorg: <http://linked.data.gov.au/def/ont/auorg#>
        SELECT *
        WHERE {{
            <{0[uri]}>  rdfs:label ?label .
            OPTIONAL {{ <{0[uri]}> dct:description ?desc . }}
            OPTIONAL {{ <{0[uri]}> auorg:classification ?classification . }}
            OPTIONAL {{ <{0[uri]}> auorg:portfolio ?portfolio . }}
            OPTIONAL {{ <{0[uri]}> dct:created ?created . }}
        }}
    '''.format({'uri': uri})

    d = query(q)
    if d is None:
        return None
    d = d.get('results').get('bindings')
    if d is None or len(d) < 1:  # handle no result
        return None

    d = d[0]
    deets = {
        'label': d.get('label').get('value'),
        'desc': d.get('desc').get('value') if d.get('desc') else None,
        'classification': d.get('classification').get('value') if d.get('classification') else None,
        'portfolio': d.get('portfolio').get('value') if d.get('portfolio') else None,
        'created': d.get('created').get('value') if d.get('created') else None
    }
    return deets


def object_describe(uri, rdf_format):
    q = 'DESCRIBE <{}>'.format(uri)
    # convert the result from the SPARQL query to turtle and back to tidy it up for viewing
    triples = query_turtle(q)
    if len(triples) < 1 or triples is None:
        return None
    g = Graph().parse(data=triples.decode('utf-8'), format='turtle')

    g.bind('auorg', Namespace('http://linked.data.gov.au/def/ont/auorg#'))
    g.bind('dct', Namespace('http://purl.org/dc/terms/'))

    if rdf_format in ['application/rdf+json', 'application/json']:
        return g.serialize(format='json-ld')
    else:
        return g.serialize(format=rdf_format)


if __name__ == '__main__':
    pass

