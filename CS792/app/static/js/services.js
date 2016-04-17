'use strict';

app.factory('Healthcare', function($http) {

    var api = '/apis';

    return {
        search: function(query, page_num, callback) {
            var uri = api + '/search/' + query;
            if(page_num == undefined) uri += '/1';
            else uri += '/' + page_num;
            return $http.get(uri).success(callback);
        },

        loadRSS: function(query, page_num, callback) {
            var uri = api + '/loadRSS/' + query;
            if(page_num == undefined) uri += '/1';
            else uri += '/' + page_num;
            return $http.get(uri).success(callback);
        },

        loadLBS: function(query, callback) {
            var uri = api + '/loadLBS/' + query;
            return $http.get(uri).success(callback);
        }
    };
});
