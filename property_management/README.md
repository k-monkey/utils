diff_properties.py is used to compare properties between two environments.

before using the script, make sure you have the following software installed:

1. Python 2.7.x or higher version (do not install Python 3!)
2. the BeautifulSoup4 python library

In order to install the BeautifulSoup, run the following command in your terminal:

easy_install BeautifulSoup4

or 

sudo easy_install BeautifulSoup4

======================================
usage:

diff_properties.py src_env dst_env [--print_all] 

e.g. the following commands prints (only) the difference between jcia6700 and localhost

diff_properties.py jcia6700 localhost 

'--print_all' option force it to print all properties. The printout is a union of the two environments.

diff_properties.py jcia6700 localhost --print_all 

Use '-h' to find out more options
