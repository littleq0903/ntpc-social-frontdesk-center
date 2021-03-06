angular.module('config', [
    'ngResource',
    'ngRoute'
])

/* Configuration */
.config(function($interpolateProvider) {
    // interpolate symbol settings
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
})

// Routing
.config(function($routeProvider){
    // routing
    $routeProvider
        // case list page
        .when('/new-case', {
            templateUrl: '/static/app/apps/application/new.tpl.html',
            controller: 'CaseAddCtrl'
        })
        .when('/cases/:id', {
            templateUrl: '/static/app/apps/application/detail.tpl.html',
            controller: 'CaseDetailCtrl'
        })
        .when('/cases', {
            templateUrl: '/static/app/apps/application/list.tpl.html',
            controller: 'CaseListCtrl'
        })

        // profile page
        .when('/profile', {
            templateUrl: '/static/app/apps/profile/profile.tpl.html',
            controller: 'ProfileCtrl'
        })

        // applicant page
        .when('/applicants', {
            templateUrl: '/static/app/apps/applicant/list.tpl.html',
            controller: 'ApplicantListCtrl'
        })
        .when('/applicants/:id_no', {
            templateUrl: '/static/app/apps/applicant/detail.tpl.html',
            controller: 'ApplicantDetailCtrl'
        })
        .otherwise('/cases');
})


.config(function($mdThemingProvider){
    // default palette config
    $mdThemingProvider.theme('default')
        .primaryPalette('blue')
        ;

    // emphasis theme config
    $mdThemingProvider.theme('emphasis', 'default')
        .backgroundPalette('blue')
        .dark()
        ;
})
.config(function($resourceProvider) {
    // Don't strip trailing slashes from calculated URLs
    $resourceProvider.defaults.stripTrailingSlashes = false;
})
.config(function($httpProvider){
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
})