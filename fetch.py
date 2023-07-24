import requests

URL = "https://www.mcbbs.net/forum.php?mod=forumdisplay&fid=45&filter=sortall&sortall=1"
 

import os

os.system("curl \""+URL+"\" > ../mcbbs.html")