from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://localhost:3030/movies/query")
q = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX dbc: <http://dbpedia.org/resource/Category:> 
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbort: <http://dbpedia.org/ontology/Work/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ckmv: <http://www.ckmvontology.com/movie.owl#>

SELECT DISTINCT ?movie ?title
FROM NAMED <http://www.ckmvontology.com/hindi_movies>
FROM NAMED <http://www.ckmvontology.com/hindi_movie_actors>
FROM NAMED <http://www.ckmvontology.com/hindi_movie_actresses>
FROM NAMED <http://www.ckmvontology.com/hindi_movie_directors>
{
  	 {	
  		SELECT ?movie ?title
		{
  			GRAPH <http://www.ckmvontology.com/hindi_movie_actors>
    		{	
      			?actor rdf:type ckmv:Actor .
      			{ ?actor rdfs:label "Ranbir Kapoor"@en }
        	
    		}
      		GRAPH <http://www.ckmvontology.com/hindi_movie_actresses>
    		{	
      			?actress rdf:type ckmv:Actress .
      			{ ?actress rdfs:label "Deepika Padukone"@en }
        	
    		}
 
      		GRAPH <http://www.ckmvontology.com/hindi_movies>
    		{
      			?movie rdf:type ckmv:Movie .
        		?movie ckmv:title ?title .
        		
  				?movie ckmv:has_actor ?actor .
        		?movie ckmv:has_actress ?actress.
        		
        		OPTIONAL{?movie ckmv:belongs_to_genre ""} .
        		OPTIONAL{?movie ckmv:release_year ""}.
  				
    		}
    		
    		
    	}
  	}
}
"""


#sparql.setQuery("""
#    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#    SELECT ?label
#    WHERE { <http://dbpedia.org/resource/Asturias> rdfs:label ?label }
#""")
import getQuery
q = getQuery.formQuery({'actor':'Ranbir Kapoor'})
sparql.setQuery(q)
print "q",q
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
print results
for result in results["results"]["bindings"]:
    print(result["title"])