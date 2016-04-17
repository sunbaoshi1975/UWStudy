'use strict';

var app = angular.module('uiApp', []);

app.config(function ($routeProvider) {
    $routeProvider
        .when('/home',
            {
                controller: 'HomeController',
                templateUrl: '/static/partials/home.html'
            })
        .when('/search/:query',
            {
                controller: 'SearchController',
                templateUrl: '/static/partials/search.html'
            })
        .when('/search/:query/:page_num',
            {
                controller: 'SearchController',
                templateUrl: '/static/partials/search.html'
            })
        .when('/empty',
            {
                controller: 'EmptyController',
                templateUrl: '/static/partials/empty.html' 
            })
        .when('/donate',
            {
                templateUrl: '/static/partials/donate.html' 
            })
        .when('/statistic',
            {
                templateUrl: '/static/partials/statistic.html' 
            })
        .when('/rss',
            {
                controller: 'RssController',
                templateUrl: '/static/partials/rss.html'
            })
        .when('/rss/:query',
            {
                controller: 'RssController',
                templateUrl: '/static/partials/rss.html'
            })
        .when('/rss/:query/:page_num',
            {
                controller: 'RssController',
                templateUrl: '/static/partials/rss.html'
            })
        .when('/lbs',
            {
                controller: 'LbsController',
                templateUrl: '/static/partials/lbs.html'
            })
        .when('/lbs/:query',
            {
                controller: 'LbsController',
                templateUrl: '/static/partials/lbs.html'
            })
        .when('/forum',
            {
                templateUrl: '/static/partials/forum.html'
            })
        .otherwise(
            { 
                redirectTo: '/home'
            });
});

app.filter('escape', function($window) {
    return $window.encodeURIComponent;
});

app.filter('startFrom', function() {
    return function(input, start) {
        start = +start; //parse to int
        return input.slice(start);
    }
});

// Handle error image
app.directive('errSrc', function() {
    return {
        link: function(scope, element, attrs) {
            element.bind('error', function() {
                if (attrs.src != attrs.errSrc) {
                    attrs.$set('src', attrs.errSrc);
                }
            });
        }
    }
});
