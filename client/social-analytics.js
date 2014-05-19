angular.module('socialAnalytics', ['pinterestModule', 'facebookModule', 'twitterModule', 'googleModule', 'urlModule']);
      
  
  var urlModule = angular.module('urlModule', []);
  
  urlModule.factory('URLFactory', [function() {
    var URLs = [
      'http://allrecipes.com/recipe/worlds-best-lasagna/detail.aspx',
      'http://allrecipes.com/recipe/crispy-edamame/detail.aspx',
      'http://allrecipes.com/Recipe/Chicken-Pot-Pie-IX/Detail.aspx',
      'http://espn.go.com/nfl/playoffs/2013/story/_/id/10395131/super-bowl-xlviii-seattle-seahawks-michael-bennett-doug-baldwin-talk-win'
    ]
    
    return {
      getURL : function() {
        // return random URL
        return URLs[Math.floor(Math.random()*URLs.length)];
      }
    }  
  }]);
  
    
      
      
  /////////////// Pinterest //////////////////
  var pinterestModule = angular.module('pinterestModule', []);
  
  pinterestModule.controller('PinterestCtrl', ['$scope', 'PinterestFactory', 'URLFactory',
    function($scope, PinterestFactory, URLFactory) {
      
      $scope.reveal = false;
      $scope.revealResults = false;
      $scope.fetchedURL = "";
      
      $scope.fetch = function(e) {
        if (e.keyCode != 13) return;
        
        $scope.reveal = true;
        $scope.fetchedURL = $scope.url;
        
        PinterestFactory.getPinterestData($scope.url).then(function(res) {
          if (!res.data.error) {
            $scope.pinterest = res.data;
            $scope.revealResults = true;
            $scope.revealError = false;
          } else {
            $scope.pinterest = {};
            $scope.error = res.data.error;
            $scope.revealError = true;
            $scope.revealResults = false;
          }
        });
        
        $scope.url = "";
      };
      
      $scope.runExample = function() {
        $scope.url = URLFactory.getURL();
        setTimeout(function() { $scope.fetch({ 'keyCode': 13 }) }, 800);
      };
      
    }
  ]);
  
  
  pinterestModule.factory('PinterestFactory', ['$http', 
    function($http){
      return {
        /*
        getPinterestData : function(url) {
          return {
            "cached": false, 
            "pin_count": "21,968", 
            "timestamp": "2014-05-04 03:30:24", 
            "url": url
          }
        }*/
        getPinterestData : function(url) {
          return $http({method: 'GET', url: 'http://mysterious-falls-4554.herokuapp.com/api/v1/pinterest?url=' + url}).
            success(function(data, status, headers, config) {

            }).
            error(function(data, status, headers, config) {

            });
        }
      };
    }
  ]);
  
  pinterestModule.directive('pinterestResults', function() {
    return {
      templateUrl: 'pinterest-results.html'
    };
  });
  
  
  
  ///////////////// Facebook //////////////////
  var facebookModule = angular.module('facebookModule', []);
  
  facebookModule.controller('FacebookCtrl', ['$scope', 'FacebookFactory', 'URLFactory', 
    function($scope, FacebookFactory, URLFactory) {
      
      $scope.reveal = false;
      $scope.revealResults = false;
      $scope.fetchedURL = "";
      
      $scope.fetch = function(e) {
        if (e.keyCode != 13) return;
        
        $scope.reveal = true;
        $scope.fetchedURL = $scope.url
        
        FacebookFactory.getFacebookData($scope.url).then(function(res){
          if (!res.data.error) {
            $scope.facebook = res.data;
            $scope.revealResults = true;
            $scope.revealError = false;
          } else {
            $scope.facebook = {};
            $scope.error = res.data.error;
            $scope.revealError = true;
            $scope.revealResults = false;
            
            console.log(res);
          }
          
          
        });
        
        $scope.url = "";
      };
      
      $scope.runExample = function() {
        $scope.url = URLFactory.getURL();
        setTimeout(function() { $scope.fetch({ 'keyCode': 13 }) }, 800);
      };
      
    }
  ]);
  
  facebookModule.factory('FacebookFactory', ['$http', 
    function($http) {
      return {
        // static url
        getFacebookData : function(url) {
          return $http({method: 'GET', url: 'http://mysterious-falls-4554.herokuapp.com/api/v1/facebook?url=' + url}).
            success(function(data, status, headers, config) {

            }).
            error(function(data, status, headers, config) {

            });
        }
      };
    }
  ]); 
  
  facebookModule.directive('facebookResults', function() {
    return {
      templateUrl: 'facebook-results.html'
    };
  });
  
  
    /////////////// Twitter //////////////////
  var twitterModule = angular.module('twitterModule', []);
  
  twitterModule.controller('TwitterCtrl', ['$scope', 'TwitterFactory', 'URLFactory',
    function($scope, TwitterFactory, URLFactory) {
      
      $scope.reveal = false;
      $scope.revealResults = false;
      $scope.fetchedURL = "";
      
      $scope.fetch = function(e) {
        if (e.keyCode != 13) return;
        
        $scope.reveal = true;
        $scope.fetchedURL = $scope.url
        
        TwitterFactory.getTwitterData($scope.url).then(function(res) {
          if (!res.data.error) {
            $scope.twitter = res.data;
            $scope.revealResults = true;
            $scope.revealError = false;
          } else {
            $scope.twitter = {};
            $scope.error = res.data.error;
            $scope.revealError = true;
            $scope.revealResults = false;
          }
        });
        
        $scope.url = "";
      };
      
      $scope.runExample = function() {
        $scope.url = URLFactory.getURL();
        setTimeout(function() { $scope.fetch({ 'keyCode': 13 }) }, 800);
      };
      
    }
  ]);
  
  
  twitterModule.factory('TwitterFactory', ['$http', 
    function($http){
      return {
        getTwitterData : function(url) {
          return $http({method: 'GET', url: 'http://mysterious-falls-4554.herokuapp.com/api/v1/twitter?url=' + url}).
            success(function(data, status, headers, config) {

            }).
            error(function(data, status, headers, config) {

            });
        }
      };
    }
  ]);
  
  twitterModule.directive('twitterResults', function() {
    return {
      templateUrl: 'twitter-results.html'
    };
  });
  
  
  
    /////////////// Google+ //////////////////
  var googleModule = angular.module('googleModule', []);
  
  googleModule.controller('GoogleCtrl', ['$scope', 'GoogleFactory', 'URLFactory',
    function($scope, GoogleFactory, URLFactory) {
      
      $scope.reveal = false;
      $scope.revealResults = false;
      $scope.fetchedURL = "";
      
      $scope.fetch = function(e) {
        if (e.keyCode != 13) return;
        
        $scope.reveal = true;
        $scope.fetchedURL = $scope.url
        
        GoogleFactory.getGoogleData($scope.url).then(function(res) {
          if (!res.data.error) {
            $scope.google = res.data;
            $scope.revealResults = true;
            $scope.revealError = false;
          } else {
            $scope.google = {};
            $scope.error = res.data.error;
            $scope.revealError = true;
            $scope.revealResults = false;
          }
        });
        
        $scope.url = "";
      };
      
      $scope.runExample = function() {
        $scope.url = URLFactory.getURL();
        setTimeout(function() { $scope.fetch({ 'keyCode': 13 }) }, 800);
      };
      
    }
  ]);
  
  
  googleModule.factory('GoogleFactory', ['$http', 
    function($http){
      return {
        getGoogleData : function(url) {
          return $http({method: 'GET', url: 'http://mysterious-falls-4554.herokuapp.com/api/v1/google-plus?url=' + url}).
            success(function(data, status, headers, config) {

            }).
            error(function(data, status, headers, config) {

            });
        }
      };
    }
  ]);
  
  googleModule.directive('googleResults', function() {
    return {
      templateUrl: 'google-results.html'
    };
  });
  
  
  
  
  
      