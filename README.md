# Social Analytics Tracking

demo: [http://abundnce10.github.io/social-analytics-tracking/](http://abundnce10.github.io/social-analytics-tracking/)

This is a JSON API that provides insight into how a specific URL performs across a variety of social networks.  Utilizing the [Flask](http://flask.pocoo.org/) microframework and a [Python package](https://pypi.python.org/pypi/socialanalytics) I wrote, I created API endpoints for Facebook, Pinterest, Twitter, and Google+.

I've created a static webpage that uses [Angular.js](https://angularjs.org/) to hit the API and present the results.

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
