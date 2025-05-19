from rdflib import Namespace

from apis_core.utils.settings import apis_base_uri

CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")

APPELLATION = Namespace(apis_base_uri() + "/appellation/")
ATTRIBUTES = Namespace(apis_base_uri() + "/attributes/")
