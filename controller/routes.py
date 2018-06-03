from flask import Blueprint, request
from flask_paginate import Pagination
from model import sparql
from pyldapi import *
import _config as conf


routes = Blueprint('controller', __name__)


#
#   Pages
#
@routes.route('/')
def home():
    return render_template('page_home.html')


@routes.route('/about')
def about():
    return render_template('page_about.html')


#
#   Registers
#
@routes.route('/reg/')
def reg():
    return RegisterOfRegistersRenderer(
        request,
        'http://localhost:5000/reg/',
        'Register of Registers',
        'The master register of this API',
        conf.APP_DIR + '/rofr.ttl'
    ).render()


@routes.route('/board/')
def boards():
    per_page = request.args.get('per_page', type=int, default=20)
    page = request.args.get('page', type=int, default=1)

    total = sparql.total_orgs()
    if total is None:
        return Response('data store is unreachable', status=500, mimetype='text/plain')

    # get list of org URIs and labels from the triplestore
    q = '''
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX auorg: <http://test.linked.data.gov.au/def/auorg#>
        SELECT ?uri ?label
        WHERE {{
            ?uri a auorg:Board ;
                 rdfs:label ?label .
        }}
        ORDER BY ?label
        LIMIT {}
        OFFSET {}
    '''.format(per_page, (page - 1) * per_page)
    register = []
    orgs = sparql.query(q)['results']['bindings']

    for org in orgs:
        o = str(org['uri']['value'])
        l = str(org['label']['value'])
        register.append((o, l))

    return RegisterRenderer(
        request,
        'http://localhost:5000/board/',
        'Register of Boards',
        'This contains all the Boards listed in directory.gov.au',
        register,
        ['http://test.linked.data.gov.au/def/auorg#Board'],
        total,
        super_register='http://localhost:5000/reg/'
    ).render()


@routes.route('/org/')
def organisations():
    per_page = request.args.get('per_page', type=int, default=20)
    page = request.args.get('page', type=int, default=1)

    total = sparql.total_orgs()
    if total is None:
        return Response('data store is unreachable', status=500, mimetype='text/plain')

    # get list of org URIs and labels from the triplestore
    q = '''
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX org: <http://www.w3.org/ns/org#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        SELECT ?uri ?label
        WHERE {{
          ?uri a org:Organization ;
               rdfs:label ?label .
          MINUS {{ ?uri a <http://test.linked.data.gov.au/def/auorg#DirectorySubStructure> }}
          MINUS {{ ?uri a <http://test.linked.data.gov.au/def/auorg#DirectoryRole> }}
          MINUS {{ ?uri a foaf:Person }}
        }}
        ORDER BY ?label
        LIMIT {}
        OFFSET {}
    '''.format(per_page, (page - 1) * per_page)
    register = []
    orgs = sparql.query(q)['results']['bindings']

    for org in orgs:
        o = str(org['uri']['value'])
        l = str(org['label']['value'])
        register.append((o, l))

    return RegisterRenderer(
        request,
        'http://localhost:5000/org/',
        'Register of Organisations',
        'This contains all the different sorts of Organisations listed in directory.gov.au '
        'but not sub-organisational units',
        register,
        ['http://www.w3.org/ns/org#Organization'],
        total,
        super_register='http://localhost:5000/reg/'
    ).render()


@routes.route('/person/')
def persons():
    per_page = request.args.get('per_page', type=int, default=20)
    page = request.args.get('page', type=int, default=1)

    total = sparql.total_persons()
    if total is None:
        return Response('data store is unreachable', status=500, mimetype='text/plain')
    pagination = Pagination(page=page, total=total, per_page=per_page, record_name='Persons')

    # translate pagination vars to query
    limit = pagination.per_page
    offset = (pagination.page - 1) * pagination.per_page

    # get list of org URIs and labels from the triplestore
    q = '''
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        SELECT ?uri ?label
        WHERE {{
          ?uri a foaf:Person ;
               rdfs:label ?label .
        }}
        ORDER BY ?label
        LIMIT {}
        OFFSET {}
    '''.format(limit, offset)
    register = []
    orgs = sparql.query(q)['results']['bindings']

    for org in orgs:
        o = str(org['uri']['value'])
        l = str(org['label']['value'])
        register.append((o, l))

    return RegisterRenderer(
        request,
        'http://localhost:5000/person/',
        'Register of Persons',
        'This contains all the people listed in directory.gov.au',
        register,
        ['http://xmlns.com/foaf/0.1/Person'],
        total,
        super_register='http://localhost:5000/reg/'
    ).render()


@routes.route('/portfolio/')
def portfolios():
    per_page = request.args.get('per_page', type=int, default=20)
    page = request.args.get('page', type=int, default=1)

    total = sparql.total_orgs()
    if total is None:
        return Response('data store is unreachable', status=500, mimetype='text/plain')
    pagination = Pagination(page=page, total=total, per_page=per_page, record_name='Portfolios')

    # translate pagination vars to query
    limit = pagination.per_page
    offset = (pagination.page - 1) * pagination.per_page

    # get list of org URIs and labels from the triplestore
    q = '''
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX org: <http://www.w3.org/ns/org#>
        SELECT ?uri ?label
        WHERE {{
          ?uri a <http://test.linked.data.gov.au/def/auorg#Portfolio> ;
               rdfs:label ?label .
        }}
        ORDER BY ?label
        LIMIT {}
        OFFSET {}
    '''.format(limit, offset)
    register = []
    orgs = sparql.query(q)['results']['bindings']

    for org in orgs:
        o = str(org['uri']['value'])
        l = str(org['label']['value'])
        register.append((o, l))

    return RegisterRenderer(
        request,
        'http://localhost:5000/portfolio/',
        'Register of Portfolios',
        'This contains all the Portfolios listed in directory.gov.au',
        register,
        ['http://test.linked.data.gov.au/def/auorg#Portfolio'],
        total,
        super_register='http://localhost:5000/reg/'
    ).render()


@routes.route('/object')
def object():
    if request.args.get('uri') is not None and str(request.args.get('uri')).startswith('http'):
        uri = request.args.get('uri')
    else:
        return Response('You must supply the URI if a resource with ?uri=...', status=400, mimetype='text/plain')

    # declare the one auorg view for all the individuals in this API
    views = {
            'auorg': View(
                'AU Org View',
                'A view of basic properties of main classes in the AU Org Ontology',
                ['text/html'] + Renderer.RDF_MIMETYPES,
                'text/turtle',
                namespace='http://test.linked.data.gov.au/def/auorg#'
            )
    }

    return AuOrgObjectRenderer(
        request,
        uri,
        'Named Individual',
        'An individual object from directory.gov.au',
        views,
        'auorg'
    ).render()


class AuOrgObjectRenderer(Renderer):
    def __init__(
            self,
            request,
            uri,
            label,
            comment,
            views,
            default_view_token
            ):
        super().__init__(
            request,
            uri,
            views,
            default_view_token
        )
        self.label = label
        self.comment = comment

    def render(self):
        if hasattr(self, 'vf_error'):
            return Response(self.vf_error, status=406, mimetype='text/plain')
        else:
            if self.view == 'alternates':
                return self._render_alternates_view()
            elif self.view == 'auorg':
                return self._render_auorg_view()

    def _render_auorg_view(self):
        if self.format in Renderer.RDF_MIMETYPES:
            rdf = sparql.object_describe(self.uri, self.format)
            if rdf is None:
                return Response('No triples contain that URI as subject', status=404, mimetype='text/plain')
            else:
                return Response(rdf, mimetype=self.format)
        else:  # only the HTML format left
            deets = sparql.instance_details(self.uri)
            if deets is None:
                return Response('That URI yielded no data', status=404, mimetype='text/plain')
            else:
                return render_template(
                    'object.html',
                    deets=deets
                )
