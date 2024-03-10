# mastrbot

--------------------------------------------------
A ~~Twitter~~ Mastodon bot that tweets words from a dictionary, with optional prefix and postfix pre/ap-pended.

Based on https://github.com/theodric/assaultbot (formerly live at - inter alia - https://twitter.com/assaultwords (RIP)).

You will need to edit the script and insert your Mastodon instance and API details, or it will not work! Fill out the form at https://[your-mastodon-instance]/settings/applications and populate the generated details in the indicated locations within the script. I hear https://botsin.space/auth/edit is a potentially bot-friendly instance.

Also, be sure to install the required libraries using the provided requirements file after the usual fashion.

```bash
pip install -r requirements.txt
```

To use the script, pass it an argument pointing to a text file containing one word per line. A sample dictionary.txt file is included.

```bash
./mastrbot.py dictionary.txt
```

There are a couple other things you can configure, such as tweet frequency, and tweet prefix/postfix. Read the script comments for more info.

The latest version of this script makes use of the Wordfilter Python module. (The original version is still there, tagged with -NOFILTER.) Whatever your personal opinons on MUH FREE SPEECH may be, Mastodon has an even higher percentage population of hyper-sensitive left-leaning language police than Twitter ever did. Feel however you like about that, but as it's a common space, and we are asking to play in their playground, we need to conduct ourselves according to the prevailing standards of the community and ensure that our bots do not use racist, sexist, ableist, -phobic, or targeting language-- or else we may inadvertently be an asshole to someone, or even find ourselves permabanned, mobbed, doxxed, gangstalked, or abducted by aliens. Inside the script, I add a couple of words to the default filter list that I don't want my particular bot tweeting; feel free to revise according to your needs by reviewing the manpage at https://pypi.python.org/pypi/wordfilter.
