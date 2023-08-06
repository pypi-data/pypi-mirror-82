# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redditsfinder']

package_data = \
{'': ['*']}

install_requires = \
['redditcleaner>=1.1.2,<2.0.0', 'requests>=2.24.0,<3.0.0', 'rich>=7.0.0,<8.0.0']

entry_points = \
{'console_scripts': ['redditsfinder = redditsfinder:main']}

setup_kwargs = {
    'name': 'redditsfinder',
    'version': '1.3.0',
    'description': "Archive a reddit user's post history. Formatted overview of a profile, JSON containing every post, and picture downloads.",
    'long_description': "# redditsfinder --- reddit user info\n**`pip3 install redditsfinder`**\n\n**A command line program to easily download reddit users' post histories.**\n\nGet any reddit user's entire post history with one command while avoiding the reddit API's 1000 post limit. \\\nThe main meat of this program is making the requests to pushshift and manipulating pushshift's JSON for a more readable all_posts.json file. \\\nThere is also a handly image downloader I made that avoids a lot of the problems of trying to grab multiple images from different sites at once. Things like file types being not what the file is encoded as, and changed URLs. Or a URL that ends with .png that returns ASCII text. It gets imgur albums along with images, because at least for a while imgur was essentially reddit's non-official image hosting service.\n\nThe colored terminal features and markup are from https://github.com/willmcgugan/rich \\\n`pip3 install rich` which is one the coolest python packages I've seen. It's very easy to pick up, but as is shown with the animated example in its README, still has a lot of depth.  \n\nhttps://github.com/LoLei/redditcleaner `pip3 install redditcleaner` was also a massive help for dealing with reddit's strange markup. \\\nComments and self-posts can be unreadable when put in another format like JSON if they have a fair amount of formatting. \\\nTo deal with it, I gave up and looked online for an alternative. Luckily there was a good one readily available.\n\n# Installation\n`pip3 install redditsfinder`\n\n# Running redditsfinder\n\n***Test it on yourself to make sure it works.***\n\n`redditsfinder yourusername`\n\n***Basic usage***\n\n**Returns every post to a different JSON file for each user and formats a table in the terminal for a quick view.\\\nTakes an arbitrary number of user names, such that there is at least one user name.**\\\n\\\n`redditsfinder username`\\\n`redditsfinder [options] username_0 username_1 username_2 ...`\n\n\n\n***Newline separated file***\n\n**Uses user names from a file.**\\\n\\\n`-f` or `--file`\\\n`redditsfinder [options] -f line_separated_text_file.txt`\n\n\n\n\n***Optional args***\n\n`-pics` returns URLs of image uploads.\\\n`-pics -d` or `-pics --download` downloads them.\\\n`-q` or `--quiet` turns off non log related print statements.\n\n# Example Pushshift request log\n![Imgur Image](https://imgur.com/VJDzFAh.png)\n\n# Example terminal table\n![Imgur Image](https://imgur.com/ZncrWFX.png)\n\n# Example JSON object\n![Imgur Image](https://imgur.com/SfoDXHQ.png)\n",
    'author': 'fitzy1293',
    'author_email': 'berkshiremind@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Fitzy1293/redditsfinder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
