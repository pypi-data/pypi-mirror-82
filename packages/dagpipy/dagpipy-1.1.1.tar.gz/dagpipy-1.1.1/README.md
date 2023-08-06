# dagpipy
A Python API Wrapper for https://dagpi.xyz/, the fast and free image API.<br>
[`dagpipy docs`](https://github.com/niztg/dagpipy/blob/master/DOCUMENTATION.md) • [`dagpi docs`](https://dagpi.docs.apiary.io/#reference) • [`examples`](https://github.com/niztg/dagpipy/blob/master/examples.py)

### Getting a token
- Go to https://dagpi.xyz/dashboard
- Sign up
- Create an app
- Wait for a few days/weeks
- Check back to see if you have your token. If so, you're free to continue!

### Instantiate a Client
```py
import dagpipy

client = dagpipy.Client(TOKEN)
```

## Image API

#### Where `url` is equal to:
<img src=https://www.gettyimages.ca/gi-resources/images/500px/983794168.jpg height=500></img>

```py
from PIL import Image

bad = client.get_image(
    option=dagpipy.ImageOptions.bad,
    url=url
)

bad_image = Image.open(bad)
bad_image.show()
```
##### Returns:<br>
<img src=https://i.imgur.com/9RILo9W.png height=500></img>

<hr>

```py
from PIL import Image

tweet = client.get_image(
    option=dagpipy.ImageOptions.tweet,
    url=url,
    username="dagpipy",
    text="amazing"
)

tweet_image = Image.open(tweet)
tweet_image.show()
```
##### Returns:<br>
<img src=https://i.imgur.com/37qSqod.png height=500></img>

<hr>

```py
from PIL import Image

whyareyougay = client.get_image(
    option=dagpipy.ImageOptions.whyareyougay,
    url=url,
    url2=url
)

whyareyougay_image = Image.open(whyareyougay)
whyareyougay_image.show()
```
##### Returns:<br>
<img src=https://i.imgur.com/NgfdJnT.png height=500></img>

<hr>

## Data/Games API

```py
wtp = client.get_game(
    option=dagpipy.Games.whos_that_pokemon
)
print(wtp.name)
print(wtp.question)
print(wtp.answer)
print(wtp.types)
print(wtp.abilities)
print(wtp.ascii)
```

##### Returns:<br>
```py
Kecleon
https://logoassetsgame.s3.us-east-2.amazonaws.com/wtp/pokemon/281q.png
https://logoassetsgame.s3.us-east-2.amazonaws.com/wtp/pokemon/281a.png
['normal']
['color change', 'protean']
@@@@@@@@@@@@@@@@@@@@@@@@,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@:.?@@@+.%@,,:@@@@%:@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@.*+@@....?....,,:,:,:::%@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@:.........**,,,**%::::#+:,%@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@.*.....****,,,******,:::::@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@,,,...*.S:.,,:*******S:::.%?S@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@,,S,:::*#,,S*********:::::,@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@,,,:%,,,,,,,,,,::.****:::::,@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@S,@,,,,,%,.,+:::::.:,****:::::,@@@@@@@@@@@@@@@@@@@@@@
@@@@@@%,,,,,:::::%,S::S?::*:,***S::,.@@@@@@@@@@@@@@@@@@@@@@@
@@@@@S,,,#:::::::.,:**#??**#:***.@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@*,,,::::::::::*:.**.***%:***,@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@.::*:,,,,:S%:***?::+.***:S***,@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@+****:..:::S+::::S?+*****@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@,#:********%*::******%@,.@@@.@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@:.:*************?******,@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@.......*:****.***%.@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@#::*%****::******+.%,,@@@@@@@@@@@@@@@@@@@@@@@
@@@@:?%.:,,:::::***:*.:::***?..*#:,,@@@@@@,#:::**:::?@@@@@@@
@,%*******+?*::::::::::****+.**SSSS+@@@@::*.***...*******@@@
@@.@@@..#****************:*.SSSSS#+SS*@%:**.#*******+***.%@@
@@@@@@@@@@@@@@:#+******:+S#SSSSS%***+*?********...***..***%@
@@@@@@@@@@@@@@@@@@@*.+SSSSSSS**+:#*****?**.**.****.***.****@
@@@@@@@@@@@@@@@@@@@?...+**.+***:,#:::*****?****S**..**..***+
@@@@@@@@@@@@@@@@@@@:**S**********::::%**%**.*****.****.****@
@@@@@@@@@@@@@@@@@@@::%*************?.****************%****#@
@@@@@@@@@@@@@@@@@@@?::::%*************?.....*****...*****#@@
@@@@@@@@@@@@@@@@@@@@*::::*****+,@,?......**************:@@@@
@@@@@@@@@@@@@@@@@@@@@@+*******.@@@@@@.:**************.@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@:****#@@@@@@@@@@@@@@..S,,@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@#?,*??@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
```

<hr>

```py
joke = client.get_game(
    option=dagpipy.Games.joke
)
print(joke.id)
print(joke.joke)
```

##### Returns:<br>
```py
41914
What do you call a midget physic that has escaped from prison?? A small medium at large
```

Consult the docs for more information on how to use this module!
