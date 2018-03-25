


def formQuery(params):
	staticInitial = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
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
	"""
	res = ""
  	subsQuery = ""
	for key,val in params.items():
		if key == 'actor' and val:
      			if len(val.split(','))==1:
        			actorQuery = """GRAPH <http://www.ckmvontology.com/hindi_movie_actors>
    		{	
      			?actor rdf:type ckmv:Actor .
      			{ ?actor rdfs:label "%s"@en }
        	
    		}
			     """%(val)
				subsQuery += """?movie ckmv:has_actor ?actor .
                                """
      			else:
        			noOfActors = len(val.split(','))
				Actors = val.split(',')
        			actorQuery = """GRAPH <http://www.ckmvontology.com/hindi_movie_actresses>
        				{ """
    				for i in range(noOfActors):
     					actorQuery += """
                    		?actor%s rdf:type ckmv:Actor .
                    		{ ?actor%s rdfs:label "%s"@en }
                    		"""%(str(i+1),str(i+1),Actors[i])
					subsQuery += """?movie ckmv:has_actor ?actor%s .
                      						"""%(str(i+1))
        			actorQuery += '}'
			staticInitial += actorQuery





		elif key == 'actress' and val:
      


      			actorQuery = """GRAPH <http://www.ckmvontology.com/hindi_movie_actresses>
        { 
            ?actress rdf:type ckmv:Actress .
            { ?actress rdfs:label "%s"@en }
          
        }
				      """%(val)
		        staticInitial += actorQuery
            		subsQuery += """?movie ckmv:has_actress ?actress .
                        """

    		elif key == 'director' and val:
            		actorQuery = """GRAPH <http://www.ckmvontology.com/hindi_movie_directors>
        { 
            ?director rdf:type ckmv:Director .
            { ?director rdfs:label "%s"@en }
          
        }
              """%(val)
            		staticInitial += actorQuery
                	subsQuery += """?movie ckmv:has_director ?director .

                            """
		
        import math
	if params.get('year'):
		subsQuery +="""?movie ckmv:release_year ?release_year .
                            
                            """
	imdb =""
	imdbfloor=""
	imdbceil = ""
	if params.get('imdb'):
	    imdbval = float(params.get('imdb'))
	    imdbfloor = str(math.floor(imdbval))
	    imdbceil = str(math.ceil(imdbval))
	    if imdbval < 5:
		imdbfloor = 0.0
            imdb=""" ?movie ckmv:imdb_rating ?imdb_rating .
        		 FILTER (xsd:double(?imdb_rating)>= %s && xsd:double(?imdb_rating)<= %s)"""%(imdbfloor,imdbceil)
	yearQ = ""
        if params.get('year'):
		yearN = params.get('year')
		
		yearQ = """        		?movie ckmv:release_year ?release_year .
					FILTER (xsd:integer(?release_year)=%s)
			"""%(yearN)
	genreQ = ""
	if params.get('genre'):
		genreN = params.get('genre')

                genreQ = """                      			?movie ckmv:belongs_to_genre ?genre .
                                        FILTER (xsd:string(?genre)='%s')
                        """%(genreN)
	mainQueryInitial = """GRAPH <http://www.ckmvontology.com/hindi_movies>
    		{
      			?movie rdf:type ckmv:Movie .
        		?movie ckmv:title ?title .
            """+subsQuery+ """
        		
  		 %s	
  		 %s	
		 %s	
    		}}}}
        	"""%(imdb,yearQ,genreQ)	
        
        res = res + staticInitial + mainQueryInitial
        return res
	
def getMovieInfo(moviename):
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
SELECT * 
FROM NAMED <http://www.ckmvontology.com/hindi_movies>
FROM NAMED <http://www.ckmvontology.com/hindi_movie_actors>
FROM NAMED <http://www.ckmvontology.com/hindi_movie_actresses>
FROM NAMED <http://www.ckmvontology.com/hindi_movie_cinematographers>
FROM NAMED <http://www.ckmvontology.com/hindi_movie_directors>
FROM NAMED <http://www.ckmvontology.com/hindi_movie_producers>
FROM NAMED <http://www.ckmvontology.com/hindi_movie_music_composers>
FROM NAMED <http://www.ckmvontology.com/hindi_movie_writers>
FROM NAMED <http://www.ckmvontology.com/movie_awards>

{
  { 
      SELECT ?actress
    {
        GRAPH <http://www.ckmvontology.com/hindi_movies>
        {   ?movie rdf:type ckmv:Movie .
            ?movie ckmv:has_actress ?actress_resource .
            ?movie ckmv:title "%s"@en
        }
          GRAPH <http://www.ckmvontology.com/hindi_movie_actresses>
        { 
            
            OPTIONAL{?actress_resource rdfs:label ?actress}
          
        }
      }
    }
    UNION
    { 
      SELECT ?actor
    {
        GRAPH <http://www.ckmvontology.com/hindi_movies>
        {   ?movie rdf:type ckmv:Movie .
            ?movie ckmv:has_actor ?actor_resource .
            ?movie ckmv:title "%s"@en  .
               
        }
          GRAPH <http://www.ckmvontology.com/hindi_movie_actors>
        { 
            
            OPTIONAL{?actor_resource rdfs:label ?actor}
          
        }
      }
    }
    UNION
    { 
      SELECT ?industry
    {
        GRAPH <http://www.ckmvontology.com/hindi_movies>
        {   ?movie rdf:type ckmv:Movie .
            ?movie ckmv:belongs_to_industry ?industry .
            ?movie ckmv:title "%s"@en  .
                
        }
      }
    }
    UNION
    { 
      SELECT ?genre
    {
        GRAPH <http://www.ckmvontology.com/hindi_movies>
        {   ?movie rdf:type ckmv:Movie .
            OPTIONAL{?movie ckmv:belongs_to_genre ?genre}
            ?movie ckmv:title "%s"@en  .
                
        }
      }
    }
     UNION
    { 
      SELECT ?director
    {
        GRAPH <http://www.ckmvontology.com/hindi_movies>
        {   ?movie rdf:type ckmv:Movie .
            ?movie ckmv:has_director ?director_resource .
            ?movie ckmv:title "%s"@en  .
        }
          GRAPH <http://www.ckmvontology.com/hindi_movie_directors>
        { 
            
            OPTIONAL{?director_resource rdfs:label ?director}
          
        }
      }
    }
     UNION
    { 
      SELECT ?plot
    {
        GRAPH <http://www.ckmvontology.com/hindi_movies>
        {   ?movie rdf:type ckmv:Movie .
            OPTIONAL{?movie ckmv:plot ?plot}
            ?movie ckmv:title "%s"@en .
        }
      }
    }
     UNION
    { 
      SELECT ?runtime_in_minutes
    {
        GRAPH <http://www.ckmvontology.com/hindi_movies>
        {   ?movie rdf:type ckmv:Movie .
            OPTIONAL{?movie ckmv:runtime_in_minutes ?runtime_in_minutes}
            ?movie ckmv:title "%s"@en  .
        }
      }
    }
    UNION
    { 
      SELECT ?producer
    {
        GRAPH <http://www.ckmvontology.com/hindi_movies>
        {   ?movie rdf:type ckmv:Movie .
            ?movie ckmv:has_producer ?producer_resource .
            ?movie ckmv:title "%s"@en  .
                
        }
      
          GRAPH <http://www.ckmvontology.com/hindi_movie_producers>
        { 
            
            OPTIONAL{?producer_resource rdfs:label ?producer}
          
        }
      }
    }
    UNION
    { 
      SELECT ?music_composer
    {
        GRAPH <http://www.ckmvontology.com/hindi_movies>
        {   ?movie rdf:type ckmv:Movie .
            ?movie ckmv:has_music_composer ?music_composer_resource .
            ?movie ckmv:title "%s"@en  .
        }
          GRAPH <http://www.ckmvontology.com/hindi_movie_music_composers>
        { 
            
            OPTIONAL{?music_composer_resource rdfs:label ?music_composer}
          
        }
      
      }
    }
     UNION
    { 
      SELECT ?writer
    {
        GRAPH <http://www.ckmvontology.com/hindi_movies>
        {   ?movie rdf:type ckmv:Movie .
            ?movie ckmv:has_writer ?writer_resource .
            ?movie ckmv:title "%s"@en .
        }
          GRAPH <http://www.ckmvontology.com/hindi_movie_writers>
        { 
            
            OPTIONAL{?writer_resource rdfs:label ?writer}
          
        }
      }
    }
     UNION
    { 
      SELECT ?cinematographer
    {
        GRAPH <http://www.ckmvontology.com/hindi_movies>
        {   ?movie rdf:type ckmv:Movie .
            ?movie ckmv:has_cinematographer ?cinematographer_resource .
            ?movie ckmv:title "%s"@en .
        }
            GRAPH <http://www.ckmvontology.com/hindi_movie_cinematographers>
        { 
            
            OPTIONAL{?cinematographer_resource rdfs:label ?cinematographer}
          
        }
      }
    }
     UNION
    { 
      SELECT ?distributor
    {
        GRAPH <http://www.ckmvontology.com/hindi_movies>
        {   ?movie rdf:type ckmv:Movie .
            OPTIONAL{?movie ckmv:has_distributor ?distributor}
            ?movie ckmv:title "%s"@en  .
                FILTER ( bound(?distributor) )
                  
        }
      
      }
    }
    UNION
    { 
      SELECT ?release_date
    {
        GRAPH <http://www.ckmvontology.com/hindi_movies>
        {   ?movie rdf:type ckmv:Movie .
            OPTIONAL{?movie ckmv:release_date ?release_date}
            ?movie ckmv:title "%s"@en 
            
        }
      }
    }
    UNION
    { 
      SELECT ?poster
    {
        GRAPH <http://www.ckmvontology.com/hindi_movies>
        {   ?movie rdf:type ckmv:Movie .
            OPTIONAL{?movie ckmv:poster ?poster}
            ?movie ckmv:title "%s"@en
            
        }
      }
    }
    UNION
    { 
      SELECT ?imdb_rating
    {
        GRAPH <http://www.ckmvontology.com/hindi_movies>
        {   ?movie rdf:type ckmv:Movie .
            OPTIONAL{?movie ckmv:imdb_rating ?imdb_rating}
            ?movie ckmv:title "%s"@en  
            
        }
      }
    }
    UNION
    { 
      SELECT ?metacritic_rating
    {
        GRAPH <http://www.ckmvontology.com/hindi_movies>
        {   ?movie rdf:type ckmv:Movie .
            OPTIONAL{?movie ckmv:metacritic_rating ?metacritic_rating}
            ?movie ckmv:title "%s"@en 
            
        }
      }
    }
    UNION
    { 
      SELECT ?is_shot_in
    {
        GRAPH <http://www.ckmvontology.com/hindi_movies>
        {   ?movie rdf:type ckmv:Movie .
            OPTIONAL{?movie ckmv:is_shot_in ?is_shot_in}
            ?movie ckmv:title "%s"@en 
            
        }
      }
    }
     UNION
    { 
      SELECT ?is_set_in
    {
        GRAPH <http://www.ckmvontology.com/hindi_movies>
        {   ?movie rdf:type ckmv:Movie .
            OPTIONAL{?movie ckmv:is_set_in ?is_set_in}
            ?movie ckmv:title "%s"@en  
            
        }
      }
    }
    UNION
    { 
      SELECT ?award_category ?movie_award_name
    {
        GRAPH <http://www.ckmvontology.com/hindi_movies>
        {   ?movie rdf:type ckmv:Movie .
            ?movie ckmv:title "%s"@en .
                FILTER ( bound(?movie) )
        }
      
          GRAPH <http://www.ckmvontology.com/movie_awards>
        { 
                ?movie_award rdf:type ckmv:Award  .
                ?movie_award ckmv:best_movie_awarded_to ?movie.
                ?movie_award ckmv:name ?movie_award_name .
                BIND ("Best Movie" AS ?award_category)
                
        }
          
      }
  }
  
  UNION 
  { 
      SELECT ?award_category ?movie_award_name
    {
        GRAPH <http://www.ckmvontology.com/hindi_movies>
        {   ?movie rdf:type ckmv:Movie .
            ?movie ckmv:title "%s"@en .
                FILTER ( bound(?movie) )
        }
      
          GRAPH <http://www.ckmvontology.com/movie_awards>
        { 
                ?movie_award rdf:type ckmv:Award  .
                ?movie_award ckmv:best_actor_belongs_to ?movie .
                ?movie_award ckmv:name ?movie_award_name .
                BIND ("Best Actor" AS ?award_category)
                
        }
          
      }
  }
  UNION 
  { 
      SELECT ?award_category ?movie_award_name
    {
        GRAPH <http://www.ckmvontology.com/hindi_movies>
        {   ?movie rdf:type ckmv:Movie .
            ?movie ckmv:title "%s"@en .
                FILTER ( bound(?movie) )
        }
      
          GRAPH <http://www.ckmvontology.com/movie_awards>
        { 
                ?movie_award rdf:type ckmv:Award  .
                ?movie_award ckmv:best_actress_belongs_to ?movie .
                ?movie_award ckmv:name ?movie_award_name .
                BIND ("Best Actress" AS ?award_category)
                
        }
          
      }
  }
  
   UNION 
  { 
      SELECT ?award_category ?movie_award_name
    {
        GRAPH <http://www.ckmvontology.com/hindi_movies>
        {   ?movie rdf:type ckmv:Movie .
            ?movie ckmv:title "%s"@en .
                FILTER ( bound(?movie) )
        }
      
          GRAPH <http://www.ckmvontology.com/movie_awards>
        { 
                ?movie_award rdf:type ckmv:Award  .
                ?movie_award ckmv:best_director_belongs_to ?movie .
                ?movie_award ckmv:name ?movie_award_name  .
                    BIND ("Best Director" AS ?award_category) 
        }
          
      }
  }
   UNION 
  { 
      SELECT ?award_category ?movie_award_name
    {
        GRAPH <http://www.ckmvontology.com/hindi_movies>
        {   ?movie rdf:type ckmv:Movie .
            ?movie ckmv:title "%s"@en .
                FILTER ( bound(?movie) )
        }
      
          GRAPH <http://www.ckmvontology.com/movie_awards>
        { 
             ?movie_award rdf:type ckmv:Award  .
             ?movie_award ckmv:best_cinematographer_belongs_to ?movie .
             ?movie_award ckmv:name ?movie_award_name  .
                 BIND ("Best Cinematographer" AS ?award_category)  
        }
          
      }
  }
   UNION 
  { 
      SELECT ?award_category ?movie_award_name
    {
        GRAPH <http://www.ckmvontology.com/hindi_movies>
        {   ?movie rdf:type ckmv:Movie .
            ?movie ckmv:title "%s"@en .
                FILTER ( bound(?movie) )
        }
      
          GRAPH <http://www.ckmvontology.com/movie_awards>
        { 
            ?movie_award rdf:type ckmv:Award  .
            ?movie_award ckmv:best_music_composer_belongs_to ?movie .
            ?movie_award ckmv:name ?movie_award_name .
            BIND ("Best Music Composer" AS ?award_category)
        }
          
      }
  }
} 
            """%(moviename,moviename,moviename,moviename,moviename,moviename,moviename,moviename,moviename,moviename,moviename,moviename,moviename,moviename,moviename,moviename,moviename,moviename,moviename,moviename,moviename,moviename,moviename,moviename,)
  return q
  				



def genreQuery(params):
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
SELECT * 
FROM NAMED <http://www.ckmvontology.com/hindi_movies>
{
    { 
      SELECT ?title ?imdb_rating ?poster 
    {
        GRAPH <http://www.ckmvontology.com/hindi_movies>
        {   ?movie rdf:type ckmv:Movie .
            ?movie ckmv:title ?title.
            ?movie ckmv:belongs_to_genre "%s" .
            ?movie ckmv:imdb_rating ?imdb_rating .
            ?movie ckmv:poster ?poster .
                FILTER ( bound(?movie) )
                FILTER ( xsd:double(?imdb_rating)>= 0.0)
          }
      }

    }
  
}
ORDER BY DESC (?imdb_rating)
    LIMIT 5
    """%(params)
  return q




def getActorQuery(params):
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
SELECT * 
FROM NAMED <http://www.ckmvontology.com/hindi_movie_actors>
FROM NAMED <http://www.ckmvontology.com/movie_awards>
FROM NAMED <http://www.ckmvontology.com/hindi_movies>
{
  { 
      SELECT ?name
    {
        GRAPH <http://www.ckmvontology.com/hindi_movie_actors>
        {   ?actor rdf:type ckmv:Actor .
            ?actor rdfs:label "%s"@en .
            OPTIONAL{?actor rdfs:label ?name}
                FILTER ( bound(?name) )
            
        }
      }
    }
    UNION
    { 
      SELECT ?birth_name
    {
        GRAPH <http://www.ckmvontology.com/hindi_movie_actors>
        {   ?actor rdf:type ckmv:Actor .
            ?actor rdfs:label "%s"@en .
            OPTIONAL{?actor ckmv:birth_name ?birth_name}
                FILTER ( bound(?birth_name) )
            
        }
      }
    }
     UNION
    { 
      SELECT ?birth_place
    {
        GRAPH <http://www.ckmvontology.com/hindi_movie_actors>
        {   ?actor rdf:type ckmv:Actor .
            ?actor rdfs:label "%s"@en .
            OPTIONAL{?actor ckmv:birth_place ?has_birth_place}
                FILTER ( bound(?has_birth_place) )
            BIND(strafter(str(?has_birth_place),"http://dbpedia.org/resource/") as ?has_birth_place_trimmed)   
            BIND(REPLACE(str(?has_birth_place_trimmed), "_", " ") AS ?birth_place)
            
        }
      }
    }
     UNION
    { 
      SELECT ?birth_date
    {
        GRAPH <http://www.ckmvontology.com/hindi_movie_actors>
        {   ?actor rdf:type ckmv:Actor .
            ?actor rdfs:label "%s"@en .
            OPTIONAL{?actor ckmv:birth_date ?birth_date}
                FILTER ( bound(?birth_date) )
        }
      }
    }
     UNION
    { 
      SELECT ?has_residence
    {
        GRAPH <http://www.ckmvontology.com/hindi_movie_actors>
        {   ?actor rdf:type ckmv:Actor .
            ?actor rdfs:label "%s"@en .
            OPTIONAL{?actor ckmv:has_residence ?residence}
                FILTER ( bound(?residence) )
            BIND(strafter(str(?residence),"http://dbpedia.org/resource/") as ?residence_trimmed)   
            BIND(REPLACE(str(?residence_trimmed), "_", " ") AS ?has_residence)
        }
      }
    }
     UNION
    { 
      SELECT ?is_child_of
    {
        GRAPH <http://www.ckmvontology.com/hindi_movie_actors>
        {   ?actor rdf:type ckmv:Actor .
            ?actor rdfs:label "%s"@en .
            OPTIONAL{?actor ckmv:is_child_of ?child_of}
                FILTER ( bound(?child_of) )
                BIND(strafter(str(?child_of),"http://dbpedia.org/resource/") as ?child_of_trimmed)   
            BIND(REPLACE(str(?child_of_trimmed), "_", " ") AS ?is_child_of)
        }
      }
    }
     UNION
    { 
      SELECT ?is_parent_of
    {
        GRAPH <http://www.ckmvontology.com/hindi_movie_actors>
        {   ?actor rdf:type ckmv:Actor .
            ?actor rdfs:label "%s"@en .
            OPTIONAL{?actor ckmv:is_parent_of ?parent_of}
                FILTER ( bound(?parent_of) )
                BIND(strafter(str(?parent_of),"http://dbpedia.org/resource/") as ?parent_of_trimmed)   
            BIND(REPLACE(str(?parent_of_trimmed), "_", " ") AS ?is_parent_of)
        }
      }
    }
    UNION
    { 
      SELECT ?is_spouse_of
    {
        GRAPH <http://www.ckmvontology.com/hindi_movie_actors>
        {   ?actor rdf:type ckmv:Actor .
            ?actor rdfs:label "%s"@en .
            OPTIONAL{?actor ckmv:is_spouse_of ?spouse_of}
                FILTER ( bound(?spouse_of) )
            BIND(strafter(str(?spouse_of),"http://dbpedia.org/resource/") as ?spouse_of_trimmed)   
            BIND(REPLACE(str(?spouse_of_trimmed), "_", " ") AS ?is_spouse_of)

        }
      }
    }
     UNION
    { 
      SELECT ?acting_since
    {
        GRAPH <http://www.ckmvontology.com/hindi_movie_actors>
        {   ?actor rdf:type ckmv:Actor .
            ?actor rdfs:label "%s"@en .
            OPTIONAL{?actor ckmv:acting_since ?acting_since}
                FILTER ( bound(?acting_since) )
        }
      }
    }
    UNION 
    { 
      SELECT ?award_category ?award_name ?award_for_movie
    {
        GRAPH <http://www.ckmvontology.com/hindi_movie_actors>
        {   ?actor rdf:type ckmv:Actor .
            ?actor rdfs:label "%s"@en .
              
        }
      
          GRAPH <http://www.ckmvontology.com/movie_awards>
        { 
                ?actor_award rdf:type ckmv:Award  .
                ?actor_award ckmv:best_actor_awarded_to ?actor .
                ?actor_award ckmv:best_actor_belongs_to ?movie .
                ?actor_award ckmv:name ?award_name .
                BIND ("Best Actor" AS ?award_category)      
        }
      
          GRAPH <http://www.ckmvontology.com/hindi_movies>
            {
                ?movie rdf:type ckmv:Movie  .
                ?movie ckmv:title ?award_for_movie .  
        
          }
          
      }
   }
 
 
}

    """%(params,params,params,params,params,params,params,params,params,params)
  return q






