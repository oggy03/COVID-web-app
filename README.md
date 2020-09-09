Corona Web Club:

Corona Web Club is a flask application that allows users to create an account and login, storing their data to a SQLite database using a hashing algorithm for the password.
They can then access the website which contains:
1. a homepage with a scrolling slide of pictures of coronavirus
2. an information page with links to government advice and NHS guidlines on the coronavirus
3. a news page that contains current headlines from the BBC website and links to the corresponding articles created using the BeautifulSoup library in python to scrape data from the BBC website.
4. an entertainment page that has an option of 2 views:
        1. text - 100 things to do in quarantine written as a long list
        2. video - embedded youtube videos with ideas for things to do during quarantine.
        Under each video there is a save button that allows the user to save up to 5 unique video URLs to a table in the SQLite database.
5. a saved videos page that allows users to see the videos that they have saved and remove videos from this page if they no longer want them saved.

The purpose of the Corona Web Club is to create an easy to use hub with all the information UK citizens need to help combat the coronavirus.
It also aims to show people how to keep active and entertained during this difficult period .
