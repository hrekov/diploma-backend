from typing import Any
from SPARQLWrapper import SPARQLWrapper, JSON
from backend.mics import return_none_on_error


def get_optional_field(result, field):
    return result[field]['value'] if field in result else None


@return_none_on_error
def search_vehicle_in_knowledge_base(vehicle_model: str) -> dict[str, Any] | None:
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    sparql.setQuery(f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dbp: <http://dbpedia.org/property/>

        SELECT ?vehicle ?abstract ?height ?length ?width ?manufacturer ?wheelbase ?transmission ?class ?production ?predecessor
        WHERE {{
            ?vehicle rdf:type dbo:Automobile .
            ?vehicle rdfs:label ?label .
            ?vehicle dbo:abstract ?abstract .
            OPTIONAL {{ ?vehicle dbo:height ?height . }}
            OPTIONAL {{ ?vehicle dbo:length ?length . }}
            OPTIONAL {{ ?vehicle dbp:width ?width . }}
            OPTIONAL {{ ?vehicle dbo:manufacturer ?manufacturer_uri . }}
            OPTIONAL {{ ?vehicle dbo:wheelbase ?wheelbase . }}
            OPTIONAL {{ ?vehicle dbo:transmission ?transmission . }}
            OPTIONAL {{ ?vehicle dbp:bodyStyle ?bodyStyle . }}
            OPTIONAL {{ ?vehicle dbp:class ?class . }}
            OPTIONAL {{ ?vehicle dbp:production ?production . }}
            OPTIONAL {{ ?vehicle dbp:predecessor ?predecessor_uri . }}
            OPTIONAL {{ ?vehicle dbp:successor ?successor_uri . }}
            BIND (strafter(str(?manufacturer_uri), "http://dbpedia.org/resource/") AS ?manufacturer) .
            BIND (strafter(str(?predecessor_uri), "http://dbpedia.org/resource/") AS ?predecessor) .
            BIND (strafter(str(?successor_uri), "http://dbpedia.org/resource/") AS ?successor) .
            FILTER (lang(?abstract) = 'en' && regex(?label, "{vehicle_model}", "i")) .
        }}
        LIMIT 1
    """)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()



    if not results["results"]["bindings"]:
        return

    result = results["results"]["bindings"][0]

    return {
        'description': result['abstract']['value'],
        'height_m': get_optional_field(result, 'height'),
        'length_m': get_optional_field(result, 'length'),
        'width_m': get_optional_field(result, 'width'),
        'manufaturer': get_optional_field(result, 'manufacturer'),
        'wheelbase': get_optional_field(result, 'wheelbase'),
        'transmission': get_optional_field(result, 'transmission'),
        'body_style': get_optional_field(result, 'bodyStyle'),
        'vehicle_class': get_optional_field(result, 'class'),
        'production_range': get_optional_field(result, 'production'),
        'predecessor': get_optional_field(result, 'predecessor'),
        'successor': get_optional_field(result, 'successor'),
    }
