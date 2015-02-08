var clientApp = angular.module('clientApp', ['ngSanitize']);


//Do dynamic angular stuff
clientApp.controller('ClientController', ['$scope', '$http', '$q', function($scope, $http, $q){
    $scope.clicked = false;
    $scope.politician_array = [];

    $scope.getData = function(){
        console.log('requesting new politician');

        promise = $http.get('/api/get_statement')
            .success(function(data, status, headers, config){
                // $scope.politicians = data;
                console.log(data);
                $('#test').lettering('words').children('span').lettering();
                $scope.politician_array.push(data);
                $scope.politicians = $scope.politician_array[0];
                //this is bad code, but this will infinitely increase the cache of politicians
                $scope.getData();
            });

        return promise;
    }

    $scope.showNewQuote = function(){
        var myPromise;
        if ($scope.politician_array.length <= 1){
            myPromise = $scope.getData();
            console.log('oldpoli', $scope.politicians);
            myPromise.then(function(){
                $scope.showNewQuote();
            });

            console.log('newpoli', $scope.politicians);
            return;
        }

        $scope.politicians = $scope.politician_array[0];
        $scope.politician_array.shift();
        $scope.clicked = false;
        $('#test').lettering();
    }

    $scope.showPolitician = function()
    {
        $scope.clicked = true;
        var box = document.getElementById("box");

        var facetop = $scope.politicians.text_offset.top;
        var faceleft = $scope.politicians.text_offset.left + 150;
        var faceheight = $scope.politicians.text_offset.height;
        var facewidth = $scope.politicians.text_offset.width;

        $(box).css({top: facetop, left: faceleft, height: faceheight, width: facewidth});

        var bubble = document.getElementById("bubble");
        var leftoffset = $scope.politicians.text_offset.offset[0] + 150;
        var bottomoffset = $scope.politicians.text_offset.offset[1] + 120;
        $(bubble).css({bottom: bottomoffset, left: leftoffset});
    }

    $http.get('/api/get_party_array')
        .success(function(data, status, headers, config){
            $scope.party = data.party;
            // console.log(p)
        });

    $scope.reloadPage = function(){
        window.location.reload();
    }

}]);


clientApp.filter('capitalize', function() {
    return function(input, scope) {
        if (input!=undefined)
        {
            input = input.toLowerCase();
            return input.substring(0,1).toUpperCase()+input.substring(1);
        }else {
            return "";
        }
    }
});

clientApp.directive("jqTable", function() {
    console.log("kk");
    // return function(scope, element, attrs) {
    //     scope.$watch("assignments", function() {
    //         $('#test').lettering();
    //         console.log("fllflf");
    //     });
    // };
});
