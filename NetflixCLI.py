# Import beautiful soup v4
import requests
import pickle
from bs4 import BeautifulSoup

#
# Cookie data with corresponding names, populate these fields manually and a cookies file will be generated.
# Once a cookie file is made, these fields may be cleared as the object will reuse the cookie file if one exists.
#
NetflixId = ' '

SecureNetflixId = ' '

ProfileId = ''

#
# Object that is used to generate search queries to the Netflix webpage, can be used to scrape Netflix provided the user has a valid Netflix account
#
class NetflixCLI(object):
    #
    # constructor
    #
    def __init__ ( self ):
        # Create a connection session
        self.session = requests.session()

        try:
            # If a cookie stored file exists we use pickle to load it
            f = open('cookies', 'rb')
            # Load the cookies into the session
            self.session.cookies.update(pickle.load(f))
            # Close the file
            f.close()
        except FileNotFoundError:
            # If no file exists we manually create cookies use
            self.session.cookies.set_cookie( requests.cookies.create_cookie(domain='www.netflix.com',name='NetflixId',value=NetflixId) )
            self.session.cookies.set_cookie( requests.cookies.create_cookie(domain='www.netflix.com',name='SecureNetflixId',value=SecureNetflixId) )
            r = self.session.get( 'https://www.netflix.com/SwitchProfile?tkn=' + ProfileId )

            # If netflix did not return a 200(SUCCESS) we throw an exception
            if r.status_code != 200:
                raise Exception( '[ Exception ] Netflix did not return 200 status code' )
            
            # If we are able to successfully choose a profile store the cookies into a local file
            with open('cookies', 'wb') as f:
                pickle.dump( self.session.cookies, f)

        return
    #
    # Destructor
    #
    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()

    #
    # Use the Netflix Command Line Search
    #
    def search( self, query : str, results : int ):
        # Copy the amount of requested results in a local variable
        rc = results

        # Construct the Query URL
        r  = self.session.get( 'https://www.netflix.com/search?q=' + query )
        bs = BeautifulSoup( r.text, 'html.parser' )

        # Initialize return list
        ret = list()

        # Fetch all the card information in the Netflix search page
        cards = bs.find_all("div", {"class": "title-card-container"}) 

        # Iterate through cards and scrape information
        for c in cards:
            # If we hit the query maximum were done
            if rc <= 0: return ret
                
            # Counting down on the amount of results fetched
            rc -= 1

            # Get the Movie ID from the Netflix video link
            movie_id     = c.find( 'a', href=True )[ 'href' ].split( '?' )[0].split( '/' )[2] 
            # Get the movie name form the fallback text that is shown if image fails to load.
            movie_name   = c.find( 'div', { "class" : "fallback-text" } ).text
            # Get the Netflix promotional Image
            card_url     = c.find( 'a', href=True ).find( 'img' )[ 'src' ]
            # Construct the URL for the movie link
            movie_url     = 'https://www.netflix.com/watch/' + movie_id
            # Store the data as a list of tuples
            ret.append( ( movie_id, movie_name, card_url, movie_url) )

        # If we have no more results to return were done
        return ret

    #
    # Lookup secondary movie data, note this will significantly slowdown scraping as it requires a secondary page fetch per film
    #
    def movie_info( self, movie_id : int ):
        # Construct the URL for the tittle page, this page contains secondary information about the film
        tittle_url    = 'https://www.netflix.com/title/' + movie_id

        # Fetch the secondary page information
        r  = requests.get( tittle_url, cookies=self.session.cookies)
        # Parse the page via Beautiful Soup
        bs = BeautifulSoup( r.text, 'html.parser' )

        # Scrape Secondary data from the /title/id subroutine
        year     = bs.find( 'span', {'class': 'year'}  )
        year     = year.text     if year != None     else None
    
        maturity = bs.find( 'span', {'class': 'maturity-number' } )
        maturity = maturity.text if maturity != None else None
        
        duration = bs.find( 'span', {'class': 'duration'}  ) 
        duration = duration.text if duration != None else None
        
        synopsis = bs.find( 'div',  {'class': 'synopsis'} ) 
        synopsis = synopsis.text if synopsis != None else None

        # Store the data as a tuple
        return ( duration, synopsis, year, maturity )

