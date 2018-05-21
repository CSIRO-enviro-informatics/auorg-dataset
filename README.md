# AU Organisations Register
This is a demonstration system only: 'test.' in web addresses will be removed in production

This is the Linked Data version of directory.gov.au. It allows web requests to be made for directory.gov.au content (no search, direct links only!) and responds with either simple web pages (HTML) or Resource Description Framework (RDF), machine-readable, data. Internet protocol content negotiation can be used to request the different formats.

Importantly, the web addresses used to make requests for this content are persistent URIs meaning they are long-term stable web addresses and thus can be quoted and used without fear that they will become broken links.


## Examples

1. An example organisation persistent URI (web address) for the CSIRO is:

    * <http://test.linked.data.gov.au/dataset/auorg/organisation/O-000886>
    * Machine-readable RDF: <http://test.linked.data.gov.au/dataset/auorg/organisation/O-000886?_format=text/turtle>

...where O-000886 is the Department of Finance's unique record ID for the CSIRO - it's persistent ID.

2. An example of a Register - a list of items - is the Persons Register:

    * Mhttp://test.linked.data.gov.au/dataset/auorg/person/>
    * Machine-readable RDF: <http://test.linked.data.gov.au/dataset/auorg/person/?_format=text/turtle>

...where, since the web address ends with /person/ but includes no specific Person ID, a list of persons is given.

## Registers

The home page of the dataset delivers both the dataset's introductory text and also a top-level register that lists other registers of items delivered by the tool.

All the registers delivered in this dataset are:

URI | Description | Contained Item Class(es)
--|--|--
/ | Register of Registers | Register
/board/ | Govt. Boards | auorg:Board
/org/ | Govt. Orgs (in directory.gov.au) | multiple: org:Organisation and sub-classes of it
/person/ | Govt. Persons (in directory.gov.au) | foaf:Person
/portfolio | Govt. Portfolios | auorg:Portfolio


## Further information

For information about how this data is produced, timelines for its improvement and who's involved, see the About Page of the API.


## Contacts
Lead developer:
**Nicholas Car**  
*Senior Experimental Scientist*  
CSIRO Land & Water  
Brisbane, Australia  
<nicholas.car@csiro.au>  
<http://orcid.org/0000-0002-8742-7730>  
