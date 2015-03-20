angular.module('RootApp', [
    'ngRoute',
    'ngMaterial',
    'ngResource',
    'ngCookies',
])

/* Configuration */
.config(function($interpolateProvider) {
    // interpolate symbol settings
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
})
.config(function($routeProvider){
    // routing
    $routeProvider
        // case list page
        .when('/cases', {
            templateUrl: '/static/app/partials/case-list.html',
            controller: 'CaseListCtrl'
        })
        // profile page
        .when('/profile', {
            templateUrl: '/static/app/partials/profile.html',
            controller: 'ProfileCtrl'
        }) ;

})
.config(function($mdThemingProvider){
    $mdThemingProvider.theme('profile-dark', 'default')
    .primaryPalette('light-green')
    .dark();
})
.config(['$resourceProvider', function($resourceProvider) {
  // Don't strip trailing slashes from calculated URLs
  $resourceProvider.defaults.stripTrailingSlashes = false;
}])
.config(function($httpProvider){
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
})

/* Factories */

.factory('RestResource', function($resource) {
    /*
     * Extending the full-restful feature to $save
     */
    return function( url, params, methods ) {
        var defaults = {
            update: { method: 'put', isArray: false },
            create: { method: 'post' }
        };

        methods = angular.extend( defaults, methods );

        var resource = $resource( url, params, methods );

        resource.prototype.$save = function() {
            if ( !this.id ) {
                return this.$create();
            }
            else {
                return this.$update();
            }
        };

        return resource;
    };

})
.factory('userFactory', [
    'RestResource',
    '$rootScope',
    '$cookies',
    function($resource, $rootScope, $cookies) {
        return $resource('/api/users/:username/', {
            username: "@username",
        });
    }
])


/* Controllers */
.controller('AppCtrl', function($scope, $rootScope, $mdSidenav, $location, $timeout, $cookies){
    $rootScope.$on('$locationChangeSuccess', closeSidenav);
    $rootScope.getCSRFToken = function (){
        return $cookies.get('csrftoken');
    }
                   
    function openSidenav(){
        $timeout(function(){
            $mdSidenav('global-sidenav').open(); 
        });
    };
    function closeSidenav() {
        $timeout(function(){
            $mdSidenav('global-sidenav').close();
        });
    };

    $scope.openSidenav = openSidenav;
    $scope.closeSidenav = closeSidenav;

    $scope.menuSections = [
        {
            "name": "案件管理",
            "items": [
                {
                    "name": "案件列表",
                    "href": "#/cases"
                },
            ]
        },
        {
            "name": "帳號管理",
            "items": [
                {
                    "name": "個人資訊頁面",
                    "href": "#/profile"
                }
            ]
        }
    ];
})
.controller('CaseListCtrl', function(){
    


})
.controller('ProfileCtrl', function($scope, $http, userFactory, $mdToast, $cookies){
    $scope.SAVE_TIMEOUT = 2000;
    $scope.user = userFactory.get({username: 'me'}, function(data) {
        console.log(data);
    });

    $scope.$watchCollection('user', function(){
        $scope.user.$save().then(function(){
            var successToast = $mdToast
                .simple()
                .content("個人資料修改完成。");
            $mdToast.show(successToast);
        }, function(data){
            var errorText = data.status + " " + data.statusText;
            var errorToast = $mdToast
                .simple()
                .content("個人資料儲存發生錯誤：" + errorText);
            $mdToast.show(errorToast);
        });
    });
    
});
