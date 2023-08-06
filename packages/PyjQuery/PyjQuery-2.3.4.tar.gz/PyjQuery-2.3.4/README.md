# [jQuery](https://jquery.com/ "jQuery")
> jQuery for DicksonUI

##Features

### Lightweight Footprint

Only sent around 87kb (minified).
python wheel is around 65kb
python package is around 35kb(Tar archive - gzip compressed)

### CSS3 Compliant

Supports CSS3 selectors to find elements as well as in style property manipulation

### Cross-Browser

[Chrome, Edge, Firefox, IE, Safari, Android, iOS, and more](https://jquery.com/browser-support/)

## What is jQuery?

jQuery is a fast, small, and feature-rich JavaScript library. It makes things like HTML document traversal and manipulation, event handling, animation, and Ajax much simpler with an easy-to-use API that works across a multitude of browsers. With a combination of versatility and extensibility, jQuery has changed the way that millions of people write JavaScript.
thia is python package of jQuery for DicksonUI

## Other Related Projects

> Coming soon(python packages)

[jQueryUI](https://jqueryui.com/)
[jQuery Mobile](https://jquerymobile.com/)
[QUnit](https://qunitjs.com/)
[Sizzle](https://sizzlejs.com/)

### Resources

-   [jQuery Core API Documentation](https://api.jquery.com/)
-   [jQuery Learning Center](https://learn.jquery.com/)
-   [jQuery Blog](https://blog.jquery.com/)
-   [Contribute to jQuery](https://contribute.jquery.com/)
-   [About the jQuery Foundation](https://jquery.org/)
-   [Browse or Submit jQuery Bugs](https://github.com/jquery/jquery/issues)

## A Brief Look

### Import
```python
import jquery
from dicksonui import Application, window

app = Application() # make Application

jquery.install(app) # install jquery

mywindow = window() # make window

app.add(mywindow) # add window to app

# $ is invalid name for python so S used
S=jquery.jQuery(mywindow) # add jquery to window

mywindow.show() # show window

# think S as $ n jquery
```

### DOM Traversal and Manipulation

Get the  `<button>`  element with the class 'continue' and change its HTML to 'Next Step...'

```python
S( "button.continue" ).html( "Next Step..." )
```

### Event Handling

Show the  `#banner-message`  element that is hidden with  `display:none`  in its CSS when any button in  `#button-container`  is clicked.
```python
from dicksonui.builtins import setCall, function
hiddenBox = S( "#banner-message" )

S( "#button-container button" ).on( "click", function("event")  (

 setCall(hiddenBox.show)

))
```
### Ajax

Call a local script on the server  `/api/getWeather`  with the query parameter  `zipcode=97201`  and replace the element  `#weather-temp`'s html with the returned text.
```python
from dicksonui.builtins import setCall, function, code
S.ajax({
    
     "url": "/api/getWeather",
    
     "data": {
    
     "zipcode": 97201
    
     },
    
     success: function( "result" ) (
    
     setCall(S( "#weather-temp" ).html)(
     
             code('"<strong>" + result + "</strong> degrees"')
        )
         
      )
    
    });


-   [Learning Center](https://learn.jquery.com/)
-   [Forum](https://forum.jquery.com/)
-   [API](https://api.jquery.com/)
-   [Twitter](https://twitter.com/jquery)
-   [IRC](https://irc.jquery.org/)
-   [GitHub](https://github.com/jquery)

Copyright 2020  [The jQuery Foundation](https://jquery.org/team/).  [jQuery License](https://jquery.org/license/)[Web hosting by Digital Ocean](https://www.digitalocean.com/)  |  [CDN by StackPath](https://www.stackpath.com/)
