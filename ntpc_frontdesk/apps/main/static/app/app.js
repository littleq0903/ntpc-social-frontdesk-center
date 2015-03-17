angular.module('RootApp', [
    'ngRoute',
    'ngMaterial',
])

/* Configuration */
.config(function($interpolateProvider) {
    // interpolate symbol settings
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');

})
.config(function($routeProvider){
    // routing
    $routeProvider.
        when('/cases', {
            templateUrl: '/static/app/partials/case-list.html',
            controller: 'CaseListCtrl'
        });

})
.config(function($mdThemingProvider){
    $mdThemingProvider.theme('toolbar-dark', 'default')
    .dark();
})

/* Controllers */
.controller('AppCtrl', function($scope, $mdSidenav){
    $scope.menuSections = [
        {
            "name": "案件管理",
            "items": [
                {
                    "name": "案件列表",
                    "href": "#/cases",
                    "clickAction": "closeSidenav()"
                },
            ]
        },
        {
            "name": "帳號管理",
            "items": [
                {
                    "name": "個人資訊頁面",
                    "href": "#/profile",
                    "clickAction": "closeSidenav()"
                }
            ]
        }
    ];
    $scope.openSidenav = function(){
        $mdSidenav('global-sidenav').open(); 
    };
    $scope.closeSidenav = function() {
        $mdSidenav('global-sidenav').close();
    };
})
.controller('CaseListCtrl', function(){
    


});
