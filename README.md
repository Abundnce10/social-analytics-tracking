# [Social Analytics Tracking](http://stattracker.me/socialanalytics/)

This is a JSON API that provides insight into how a specific URL performs across a variety of social networks.  Utilizing the [Flask](http://flask.pocoo.org/) microframework and a [Python package](https://pypi.python.org/pypi/socialanalytics) I created, I've created API endpoints for Facebook, Pinterest, Twitter, and Google+.

I've created a static webpage that uses [Angular.js](https://angularjs.org/) to hit the API and present the results.  It can be found [here](http://stattracker.me/socialanalytics/).

## Documentation

#### Facebook

```
/api/v1/facebook?url=
```

#### Pinterest

```
/api/v1/pinterest?url=
```

#### Twitter

```
/api/v1/twitter?url=
```

#### Google+

```
/api/v1/google?url=
```