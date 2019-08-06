import sys
from NetflixCLI import NetflixCLI

netflixCLI = NetflixCLI();

if __name__ == "__main__":
    if len( sys.argv ) < 3:
        print( '[ Error ] Not enough arguments.' )
        exit()

    netflixCLI.cookies_load( 'cookies' )

    for x in netflixCLI.search( sys.argv[1], int(sys.argv[2]) ):
        print( '---------------------------------------------------------' )
        print( x[1] + ' : (' + x[0] + ')' )
        print( x[2] )
        print( x[3] )
        movieInfo = netflixCLI.movie_info( x[0] )
        print( movieInfo[0] )
        print( movieInfo[1] )
        print( movieInfo[2] )
        print( movieInfo[3] )
        print( '---------------------------------------------------------' )
