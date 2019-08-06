# Netflix CLI Search

The following is a python project uses data from the Netflix web search to allow for search functionality through the command line. The project requires a valid Netflix account for functionality. This project can be easily adapted for thorough scraping applications, although Netflix might frown upon that behaviour. 

# How To
The search.py is an example of the CLI interface and can be used to perform basic searches.

The login.py will log you into Netflix and cache to cookies for later reuse.

NetflixCLI.py has a login feature that will generate a cookie for authentication. You can save the cookie to the file of your choice then load it for later authentication. This script will use an existing Netflix account as an entry point into the Netflix webpage. 
<span style="color:red"> **If you login more than 25 times in a single day. Netflix will block your access to the login page. From witch point you will no longer be able to login to Netflix, for a period of 24 hours. So please cache your cookies and reuse them.** </span>

# Disclaimer
Do not use this code for any kind of enterprize/heavy bandwidth applications. This could lead to your Netflix account getting banned. Furthermore, Netflix could pursuit trespass to chattels lawsuit for unlawful use of their servers.

# Example
Bash Command
```bash
python3 example.py 'Blade Runner' 5
```
Results
```
---------------------------------------------------------
Cloud Atlas : (70248183)
https://*.nflxso.net/dnm/api/v6/*.jpg
https://www.netflix.com/watch/70248183
2h 51m
From ancient killer to hero in a primal future. When time shapes the soul, yesterday's gesture is tomorrow's revolution.
2012
R
---------------------------------------------------------
---------------------------------------------------------
Solo: A Star Wars Story : (80220814)
https://*.nflxso.net/dnm/api/v6/*.jpg
https://www.netflix.com/watch/80220814
2h 14m
A young Han Solo tries to settle an old score with the help of his new buddy Chewbacca, a crew of space smugglers and a cunning old friend.
2018
PG-13
---------------------------------------------------------
---------------------------------------------------------
Black Mirror : (70264888)
https://*.nflxso.net/dnm/api/v6/*.jpg
https://www.netflix.com/watch/70264888
5 Seasons
When old college friends Danny and Karl reconnect in a VR version of their favorite video game, the late-night sessions yield an unexpected discovery.
2019
TV-MA
---------------------------------------------------------
---------------------------------------------------------
Altered Carbon : (80097140)
https://*.nflxso.net/dnm/api/v6/*.jpg
https://www.netflix.com/watch/80097140
1 Season
After 250 years on ice, a prisoner returns to life in a new body with one chance to win his freedom: by solving a mind-bending murder.
2018
TV-MA
---------------------------------------------------------
---------------------------------------------------------
Ex Machina : (80023689)
https://*.nflxso.net/dnm/api/v6/*.jpg
https://www.netflix.com/watch/80023689
1h 48m
He was chosen to meet his company's reclusive founder, one of the world's greatest minds. And one of the most dangerous.
2015
R
---------------------------------------------------------
```
Corresponding Web Results
![alt text]( /images/ss.png )

# Todo
- [ x ] Add a script to allow for generation of authentication cookies.