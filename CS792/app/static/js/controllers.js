'use strict';

app.controller('NavbarController', function($scope, $routeParams, $location) {
    if($routeParams.query < 2 | $routeParams > 50) {
        $location.path('/home');
        return;
    }

    $scope.$on('$routeChangeSuccess', function (event, current, previous) {
        $scope.query = current.pathParams.query;
     });

    $scope.go = function(query) {
        $location.path(query);
    };
});

app.controller('HomeController', function($rootScope, $scope, $location) {
    $scope.go = function(query) {
        $location.path(query);
    };

    $rootScope.is_homepage = function() {
        return true;
    }
});

app.controller('EmptyController', function($rootScope, $scope, $location) {
    $scope.go = function(query) {
        $location.path(query);
    };

    $rootScope.is_homepage = function() {
        return true;
    }
});

app.controller('SearchController', function($rootScope, $scope, $location, $routeParams, Healthcare) {
    if($routeParams.query < 2 | $routeParams > 50) {
        $location.path('/home');
        return;
    }

    // Execute query
    Healthcare.search($routeParams.query, $routeParams.page_num, function (data) {
            if (!data.page_count)
                $location.path('empty');
            $scope.query = data.query;
            $scope.page_count = data.page_count;
            $scope.page_size = data.page_size;
            $scope.page_num = data.page_num;
            $scope.page_next = data.page_next;
            $scope.page_prev = data.page_prev;

            //$scope.result = [].concat(typeof data.result);
            $scope.result = (typeof data.result === 'string') ? [ data.result ] : data.result;

            // Testing data
            /*
             $scope.result = [
             {"link": "http://www.google.com/aclk?sa=L&ai=C5tirvqXwVo3HG8fImAT4zZGABuvJqJhE5_zR6pEDhvCRBQgAEAFgya6ZjeykgBDIAQGqBB9P0OBepHEFM_dELxRZzDmieGipf1J4SaCtvSHblLQ4gAe_kNYzkAcBqAemvhvYBwE&sig=AOD64_2rta1DtQ887F9lqDtFND2JSAWWgA&clui=0&rct=j&q=&ved=0ahUKEwjzg7Pol9PLAhVFGx4KHcwfDmIQ0QwIGw&adurl=http://tracker.marinsm.com/rd%3Fcid%3D1870765e38482%26mkwid%3DseIEs444j-dc%26muid%3D%257Bm_uid%257D%26lp%3Dhttp://www.apple.com/us/shop/go/apple_com%253F%2526mnid%253DseIEs444j-dc_mtid_1870765e38482_pcrid_107648776087_%2526cid%253Daos-us-kwg-brand-slid-%2526mtid%253D1870765e38482%2526aosid%253Dp238", "domain": "www.google.com", "serp_id": "109", "id": "1020", "rank": "1", "snippet": "Shop iPhone, iPad, Mac, Apple TV & Apple Watch. Learn more & shop now.", "visible_link": "www.apple.com/", "link_type": "ads_main", "title": ""},
             {"link": "http://www.apple.com/", "domain": "www.apple.com", "serp_id": "109", "id": "1021", "rank": "5", "snippet": "Apple leads the world in innovation with iPhone, iPad, Mac, Apple Watch, iOS, OS X, watchOS and more. Visit the site to learn, buy, and get support.", "visible_link": "www.apple.com/", "link_type": "results", "title": "Apple"},
             {"link": "https://www.applefcu.org/", "domain": "www.applefcu.org", "serp_id": "109", "id": "1022", "rank": "6", "snippet": "Apple Federal Credit Union is a cooperative financial institution dedicated to fulfilling the dreams of its members.", "visible_link": "https://www.applefcu.org/", "link_type": "results", "title": "Apple Federal Credit Union"},
             {"link": "http://www.yellowpages.com/ashburn-va/the-apple-store", "domain": "www.yellowpages.com", "serp_id": "109", "id": "1023", "rank": "7", "snippet": "Results 1 - 30 of 148 - Find 148 listings related to The Apple Store in Ashburn on YP.com. See reviews, photos, directions, phone numbers and more for The Apple\u00a0...", "visible_link": "www.yellowpages.com \u203a Ashburn, VA", "link_type": "results", "title": "The Apple Store in Ashburn, Virginia with Reviews ..."},
             {"link": "http://apple-store.in/20147-ashburn/", "domain": "apple-store.in", "serp_id": "109", "id": "1024", "rank": "8", "snippet": "Apple Stores in Ashburn, VA \u00b7 List of Apple Stores nationwide .... Apple Store Reston. Apple Store Reston 11949 Market Street Reston, VA 20190. phone: (571)\u00a0...", "visible_link": "apple-store.in/20147-ashburn/", "link_type": "results", "title": "Apple Macintosh and iPhone Stores in Ashburn, VA"},
             {"link": "http://www.wired.com/2015/04/the-apple-watch/", "domain": "www.wired.com", "serp_id": "109", "id": "1025", "rank": "9", "snippet": "In early 2013, Kevin Lynch accepted a job offer from Apple. Funny thing about the offer: It didn't say what he would be doing. So intense is Apple's secrecy that\u00a0...", "visible_link": "www.wired.com/2015/04/the-apple-watch/", "link_type": "results", "title": "iPhone Killer: The Secret History of the Apple Watch | WIRED"},
             {"link": "http://www.newyorker.com/magazine/2015/02/23/shape-things-come", "domain": "www.newyorker.com", "serp_id": "109", "id": "1026", "rank": "10", "snippet": "Ian Parker visits the top-secret lab where the world's most powerful design team created the Apple Watch.", "visible_link": "www.newyorker.com/magazine/2015/02/23/shape-things-come", "link_type": "results", "title": "The Shape of Things to Come - The New Yorker"},
             {"link": "http://www.fastcodesign.com/3053406/how-apple-is-giving-design-a-bad-name", "domain": "www.fastcodesign.com", "serp_id": "109", "id": "1027", "rank": "11", "snippet": "Once upon a time, Apple was known for designing easy-to-use, easy-to-understand products. It was a champion of the graphical user interface,\u00a0...", "visible_link": "www.fastcodesign.com/3053406/how-apple-is-giving-design-a-bad-name", "link_type": "results", "title": "How Apple Is Giving Design A Bad Name | Co.Design ..."}
             ];
             */

            // Testing data
            /*
             $scope.result = [
             {
             "domain": "www.applefcu.org",
             "id": "429",
             "link": "https://www.applefcu.org/",
             "link_type": "results",
             "rank": "5",
             "serp_id": "51",
             "snippet": "Apple Federal Credit Union is a cooperative financial institution dedicated to fulfilling the dreams of its members.",
             "title": "Apple Federal Credit Union",
             "visible_link": "https://www.applefcu.org/"
             },
             {
             "domain": "www.yellowpages.com",
             "id": "430",
             "link": "http://www.yellowpages.com/ashburn-va/the-apple-store",
             "link_type": "results",
             "rank": "6",
             "serp_id": "51",
             "snippet": "Results 1 - 30 of 148 - Find 148 listings related to The Apple Store in Ashburn on YP.com. See reviews, photos, directions, phone numbers and more for The Apple\u00a0...",
             "title": "The Apple Store in Ashburn, Virginia with Reviews ...",
             "visible_link": "www.yellowpages.com \u203a Ashburn, VA"
             },
             {
             "domain": "apple-store.in",
             "id": "431",
             "link": "http://apple-store.in/20147-ashburn/",
             "link_type": "results",
             "rank": "7",
             "serp_id": "51",
             "snippet": "Apple Stores in Ashburn, VA \u00b7 List of Apple Stores nationwide .... Apple Store Reston. Apple Store Reston 11949 Market Street Reston, VA 20190. phone: (571)\u00a0...",
             "title": "Apple Macintosh and iPhone Stores in Ashburn, VA",
             "visible_link": "apple-store.in/20147-ashburn/"
             },
             {
             "domain": "en.wikipedia.org",
             "id": "432",
             "link": "https://en.wikipedia.org/wiki/Apple_Inc.",
             "link_type": "results",
             "rank": "8",
             "serp_id": "51",
             "snippet": "Apple Inc. is an American multinational technology company headquartered in Cupertino, California, that designs, develops, and sells consumer electronics,\u00a0...",
             "title": "Apple Inc. - Wikipedia, the free encyclopedia",
             "visible_link": "https://en.wikipedia.org/wiki/Apple_Inc."
             },
             {
             "domain": "arstechnica.com",
             "id": "433",
             "link": "http://arstechnica.com/apple/2016/03/liveblog-apples-march-21-iphone-and-ipad-event/",
             "link_type": "results",
             "rank": "9",
             "serp_id": "51",
             "snippet": "16 hours ago - Apple's next press event happens on Monday, March 21 at the company's campus in Cupertino, California. We're going to be in the audience to\u00a0...",
             "title": "Liveblog: Apple's March 21 iPhone and iPad event | Ars ...",
             "visible_link": "arstechnica.com/apple/.../liveblog-apples-march-21-iphone-..."
             }];*/
        });

    $rootScope.is_homepage = function() {
        return false;
    }

    $scope.orderByFunction = function(record){
        return parseInt(record.rank);
    };
});

app.controller('RssController', function($rootScope, $scope, $location, $routeParams, Healthcare) {
    // Get keyword
    var queryKeyWord = 'news';
    if($routeParams.query == undefined) {
        queryKeyWord = 'news';
    } else if($routeParams.query < 2 | $routeParams > 50) {
        queryKeyWord = 'news';
    } else {
        // Remove all spaces
        queryKeyWord = $routeParams.query.replace(/ /g,'');
    }
    // Execute query
    Healthcare.loadRSS(queryKeyWord, $routeParams.page_num, function (data) {
            if (!data.page_count) {
                if (queryKeyWord != 'news')
                    $location.path('rss');
                else
                    $location.path('empty');
            }
            $scope.query = data.query;
            $scope.page_count = data.page_count;
            $scope.page_size = data.page_size;
            $scope.page_num = data.page_num;
            $scope.page_next = data.page_next;
            $scope.page_prev = data.page_prev;

            $scope.result = (typeof data.result === 'string') ? [ data.result ] : data.result;
        });

    $rootScope.is_homepage = function() {
        return false;
    }
});

app.controller('LbsController', function($rootScope, $scope, $location, $routeParams, Healthcare) {
    // Get keyword
    var queryKeyWord = 'none';
    if($routeParams.query == undefined) {
        queryKeyWord = 'none';
    } else if($routeParams.query < 2 | $routeParams > 50) {
        queryKeyWord = 'none';
    } else {
        // Remove all spaces
        queryKeyWord = $routeParams.query.replace(/ /g,'');
    }
    // Execute query
    Healthcare.loadLBS(queryKeyWord, function (data) {
            $scope.query = data.query;
            $scope.poi_count = data.poi_count;
            $scope.result = (typeof data.result === 'string') ? [ data.result ] : data.result;
        });

    $rootScope.is_homepage = function() {
        return false;
    }
});
