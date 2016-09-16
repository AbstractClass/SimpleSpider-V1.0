Simple Spider - Version 1.0
===================

3 days ago, I (an intermediate Python user) decided to build... something.  I wanted a project, but nothing too crazy.  I wanted to dip into machine learning and pattern recognition in words, but that ended up being a little complex, so I built this instead.

What does it do?
-------------

The spider's main objective is to find all links withing a given page, then do the same with all of those links.  You are given the option to set 'max_pages', which will stop the search after a given number of pages.  If it is not given, the program will run infinitely, this is not recommended.

It also gives the ability to cache pages in their html form.  If a file is provided, they will be appended.  If no file is provided, files will be created for each url, with the url as the name, and the html as the content(and the special charactes in the url will be replaced with underscores).

Finally, I threw in the ability to stop on the finding of a given word or phrase (regex not supported at this time).  I honeslty did this so I could play 'six degrees of Kevin Bacon' with websites (like how long does it take to get from 'disney.com' to the first mention of 'Deadpool' just by clicking on links?)


How does it work?
---

It currently uses requests to get the page, BeautifulSoup4 to parse it (for links and the halt_phrase), urllib turn partial links into full links, and re to clean up the urls to be turned into filenames (if no output file is given)


Future Plans
---

Doing research on this, I discovered that there are a million and one ways to do this, and I plan to try a lot of them.  I want to experiment with the following packages:

- twisted
- ghost.py
- lxml (instead of bs4 using lxml)
- re (instead of bs4 for html parsing)
- threading (so it can process multiple urls at once)

I want to make this thing as fast as possible and offer lots of choice in crawling methods (optional threading? sure.  want the program to simulate clicking each link? sure. Want translation to Klingon? sure(if you can point me to the right module).)

Suggestions
---

If you have suggestions on speeding up performance, I want to hear them.  I promise I will not take offence to you talling me my code is bad (unless you suggested improvement is worse).  If there is a faster option, or a feature you want send me a message or leave a comment (also like, subscribe, retweet, favorite, and whatever else you kids do).

cheers, Connor MacLeod
