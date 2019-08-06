import sys
import getpass
from NetflixCLI import NetflixCLI

netflixCLI = NetflixCLI();

if __name__ == "__main__":
    email     = input( 'Email:' )
    password  = getpass.getpass( 'Password:' )

    accounts = netflixCLI.login( email, password )

    print( '----------------------------------------------------' )
    print( ' Select User' )
    print( '----------------------------------------------------' )

    i = 0
    for a in accounts:
        print( '[ %d ] (%s : %s)' % ( i, a[0], a[1] ) )
        i += 1

    print( '----------------------------------------------------' )
    sa = -1;
    while sa not in range( 0, len( accounts ) ):
        sa = int(input())

    print( 'Selecting Profile' )
    netflixCLI.profile_select( accounts[ sa ] )

    print( 'Saving Cookies' )
    netflixCLI.cookies_save( 'cookies' )

    print( 'Done' )
    print( '----------------------------------------------------' )
