Leetcode Problem Opener

Program that helps you browse and open problems in leetcode.com.
Problems are indexed from easiest to hardest with respect to elo rating calulated by @zerotrac in https://github.com/zerotrac/leetcode_problem_rating 

To use "Show accomplished" feature, paste your cookie header to /data/cookie.txt.
  Tutorial:
  1) Go to https://leetcode.com/api/problems/algorithms/ while being logged in.
  2) Click combination of: "Ctrl + Shift + C" (works for both Opera and Chrome),
     or right click anywhere on the text filled page and choose "Inspect element".
  3) Go to "Network" tab.
  4) Reload the page (e.g. by clicking F5).
  5) You will see number (for me is 3) of requests call made to API, left click on "algorithms/"
  6) Go to "Headers" tab.
  7) Look for "Request Headers".
  8) Copy contents of "Cookie" under "Request Headers" to /data/cookie.txt.
     !!! Be extra mindful of the trailing endline while copying - remove it. !!!
     Your cookie should look something like (mine look like this):
     "_gcl_au=<some_numbers>
     _ga_(...)=(...)
     _ga_(...)=(...)
     (...)"
     legend: (...) - any amount of characters
  9) Run "api_leet.py" after copying your cookie to "/data/cookie.txt".

In future commits I will explore possibility to scrap it out without making this call to API (I have idea).


Libraries in use: 
- pandas

Methods and libraries included in python:
- tkinter
- webbrowser
- os.getcwd()
- json
