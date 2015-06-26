angular.module('RootApp', [
    // libraries
    'ngMaterial',
    'ngCookies',
    'ngMessages',
    'infinite-scroll',

    // global modules
    'config',
    
    // resources
    'resources.user',

    // controllers
    'apps.profile.controllers',
    'apps.application.controllers',
    'apps.applicant.controllers',

])

/* pre-run */
.run(function($rootScope){
    // for more button loading status
    $rootScope.moreLoadingStatus_stop = "更多";
    $rootScope.moreLoadingStatus_pending = "讀取中...";
    $rootScope.moreLoadingStatus = $rootScope.moreLoadingStatus_stop;
})

/* Controllers */
.controller('LoginCtrl', function(){})
.controller('AppCtrl', function($scope, $rootScope, $mdSidenav, $window, $location, $timeout, $cookies, userFactory){
    $rootScope.$on('$locationChangeSuccess', closeSidenav);
    $rootScope.getCSRFToken = function (){
        return $cookies.get('csrftoken');
    }
                   
    function openSidenav(){
        $timeout(function(){
            $mdSidenav('global-sidenav').open(); 
        });
    }
    function closeSidenav() {
        $timeout(function(){
            $mdSidenav('global-sidenav').close();
        });
    }
    function navTo(url) {
        $window.location.href = url;
    }


    $scope.openSidenav = openSidenav;
    $scope.closeSidenav = closeSidenav;
    $scope.navTo = navTo;

    $scope.menuSections = [
        {
            "name": "案件管理",
            "items": [
                {
                    "name": "案件列表",
                    "href": "#/cases",
                    "icon": "/static/material-design-icons/editor/svg/production/ic_insert_drive_file_24px.svg"
                },
                {
                    "name": "案件統計",
                    "href": "#/dashboard",
                    "icon": "/static/material-design-icons/action/svg/production/ic_assessment_24px.svg",
                }
            ]
        },
        {
            "name": "申請人管理",
            "items": [
                {
                    "name": "申請人列表",
                    "href": "#/applicants",
                    "icon": "/static/material-design-icons/editor/svg/production/ic_insert_drive_file_24px.svg"
                }
            ]
        },
        {
            "name": "帳號管理",
            "items": [
                {
                    "name": "個人資訊頁面",
                    "href": "#/profile",
                    "icon": "/static/material-design-icons/action/svg/production/ic_account_circle_24px.svg"
                },
                {
                    "name": "登出",
                    "href": "/logout",
                    "icon": "/static/material-design-icons/navigation/svg/production/ic_close_24px.svg"
                }
            ]
        }
    ];

    $rootScope.current_user = userFactory.get({username: "me"});
})

