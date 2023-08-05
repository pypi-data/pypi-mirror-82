
![Normalize.css](https://necolas.github.io/normalize.css/logo.svg)

# Normalize.css

## A modern, HTML5-ready alternative to CSS resets

[Normalize.css](https://github.com/necolas/normalize.css/)  makes browsers render all elements more consistently and in line with modern standards. It precisely targets only the styles that need normalizing.

this is a pythonic package of normalize.css for [DicksonUI](https://github.com/Ksengine/DicksonUI)

Chrome, Edge, Firefox ESR+, IE 10+, Safari 8+, Opera

## install
```
pip install normalize.css
```
## usage
```python
import normalize
from dicksonui import Application, window
app = Application() # make Application
normalize.install(app) # install normalize.css
mywindow = window() # make window
app.add(mywindow) # add window to app
normalize.add(mywindow) # add normalize.css to window
mywindow.show() # show window
```

[Read more about original normalize.css »](http://nicolasgallagher.com/about-normalize-css/)


…as used by  [Twitter](https://twitter.com/),  [TweetDeck](https://tweetdeck.twitter.com/),  [GitHub](https://github.com/),  [Soundcloud](https://soundcloud.com/),  [Guardian](http://www.theguardian.com/uk?view=mobile),  [Medium](https://medium.com/),  [GOV.UK](https://www.gov.uk/),  [Bootstrap](http://getbootstrap.com/),  [HTML5 Boilerplate](http://html5boilerplate.com/), and many others.

[![GitHub](https://necolas.github.io/normalize.css/github-logo.png)](https://github.com/Ksengine/DicksonUI/extentions/normalize)
### Github repo
Source code available on GitHub:  [Ksengine/DicksonUI/extentions/normalize](https://github.com/Ksengine/DicksonUI/extentions/normalize).
