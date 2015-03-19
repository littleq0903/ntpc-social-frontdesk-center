angular.module('RootApp', [
    'ngRoute',
    'ngMaterial',
    'ngResource'
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

/* Factories */

.factory('userFactory', function($resource) {
    return $resource('/api/cases/:case_id', {
        case_id: '@id'
    });

})

/* Controllers */
.controller('AppCtrl', function($scope, $rootScope, $mdSidenav, $location, $timeout){
    $rootScope.$on('$locationChangeSuccess', closeSidenav);
                   
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
.controller('ProfileCtrl', function(){


});
