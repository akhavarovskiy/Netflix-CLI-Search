# Import beautiful soup v4
import requests
import pickle
from bs4 import BeautifulSoup

#
# Object that is used to generate search queries to the Netflix webpage, can be used to scrape Netflix provided the user has a valid Netflix account
#
class NetflixCLI(object):
    #
    # constructor
    #
    def __init__ ( self ):
        self.session = requests.session()
    #
    # Destructor
    #
    def __exit__(self, exc_type, exc_value, traceback):
        if self.session is not None:
            self.session.close()

    #
    # Create a Netflix session using credentials, will return a list of profiles
    #
    def login( self, email : str, password : str ):
        # Create session
        s  = requests.session()
        
        # We need the login page to fetch the authURL 
        r  = s.get( 'https://www.netflix.com/login' )

        if r.status_code != 200:
            raise Exception( '[ Exception ] Failed to fetch login page' )

        # Parse the result to get the authURL
        bs = BeautifulSoup( r.text, 'html.parser' )
        k  = bs.find( 'input', { 'name' : 'authURL' } )[ 'value' ]

        # Create a POST request to the netflix login page
        r = s.post( "https://www.netflix.com/login", data = 
        { 
            'userLoginId'    : email,
            'password'       : password,
            'rememberMe'     : 'true',
            'flow'           : 'websiteSignUp',
            'mode'           : 'login',
            'action'         : 'loginAction',
            'withFields'     : 'rememberMe,nextPage,userLoginId,password,countryCode,countryIsoCode',
            'authURL'        : k,
            'nextPage'       : ' ',
            'showPassword'   : ' ',
            'countryCode'    : '+1',
            'countryIsoCode' : 'US'
        })

        # If the login fails
        if r.status_code != 200:
            raise Exception( '[ Exception ] Login POST request failed' )

        # Store the created session in a class variable
        self.session = s

        # Fetch the browse page
        r  = self.session.get( 'https://www.netflix.com/browse' )
        bs = BeautifulSoup( r.text, 'html.parser' )

        ret = list()

        # Get the profile options for the account
        p   = bs.find_all( 'a', { 'class' : 'profile-link' } ) 
        for i in p:
            ret.append( ( i.find( 'span', { 'class' : 'profile-name' } ).text, i[ 'href' ] ) )

        return ret

    #
    # Select the profile of the current session
    #
    def profile_select( self, profile : tuple ):
        self.session.get( 'https://www.netflix.com' + profile[1] )

    #
    # Save the login data to prevent additional signins
    #
    def cookies_save( self, dir : str ):
        if self.session is None:
            return False
        
        with open(dir, 'wb') as f:
            pickle.dump( self.session.cookies, f)

        return True

    #
    # Load the cookies of a previous session
    #
    def cookies_load( self, dir : str ):
        try:
            # If a cookie stored file exists we use pickle to load it
            f = open(dir, 'rb')
            # Load the cookies into the session
            self.session.cookies.update(pickle.load(f))
            # Close the file
            f.close()
            return True
        except FileNotFoundError:
            return False
    #
    # Use the Netflix Command Line Search
    #
    def search( self, query : str, results : int ):
        if self.session is None:
            return
        # Copy the amount of requested results in a local variable
        rc = results

        # Construct the Query URL
        r  = self.session.get( 'https://www.netflix.com/search?q=' + query )

        # If we fail to fetch the page we might no longer be authorized
        if r.status_code != 200:
            raise Exception( '[ Exception ] Cannot fetch search page. Cookies could be expired.' )

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
        if self.session is None:
            return
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

