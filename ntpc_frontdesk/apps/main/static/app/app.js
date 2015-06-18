angular.module('RootApp', [
    'ngRoute',
    'ngMaterial',
    'ngResource',
    'ngCookies',
    'ngMessages',
])


/* Directive */
.directive('checkid', function(){
    function checkID( id ) {
        tab = "ABCDEFGHJKLMNPQRSTUVXYWZIO"                     
        A1 = new Array (1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3);
        A2 = new Array (0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5);
        Mx = new Array (9,8,7,6,5,4,3,2,1,1);

        if ( id.length != 10 ) return false;
        i = tab.indexOf( id.charAt(0) );
        if ( i == -1 ) return false;
        sum = A1[i] + A2[i]*9;

        for ( i=1; i<10; i++ ) {
            v = parseInt( id.charAt(i) );
            if ( isNaN(v) ) return false;
            sum = sum + v * Mx[i];
        }
        if ( sum % 10 != 0 ) return false;
        return true;
    }
    
    return {
        require: 'ngModel',
        link: function(scope, elm, attrs, ctrl, ngModel) {
            ctrl.$validators["checkid"] = function (modelValue, viewValue){
                if (ctrl.$isEmpty(modelValue)) {
                    return true;
                }
                return checkID(viewValue);
            }
        }
    };
})

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
        .when('/new-case', {
            templateUrl: '/static/app/partials/case-new.html',
            controller: 'CaseAddCtrl'
        })
        .when('/cases/:id', {
            templateUrl: '/static/app/partials/case-detail.html',
            controller: 'CaseDetailCtrl'
        })
        .when('/cases', {
            templateUrl: '/static/app/partials/case-list.html',
            controller: 'CaseListCtrl'
        })
        // profile page
        .when('/profile', {
            templateUrl: '/static/app/partials/profile.html',
            controller: 'ProfileCtrl'
        })
        .when('/applicants', {
            templateUrl: '/static/app/partials/applicant-list.html',
            controller: 'ApplicantListCtrl'
        })
        .otherwise('/cases');
})
.config(function($mdThemingProvider){
    $mdThemingProvider.theme('profile-dark', 'default')
        .dark();
    $mdThemingProvider.theme('case-detail-form', 'default')
        .backgroundPalette('indigo');
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

.factory('RestResource', function($resource, $http) {
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
        
        resource.prototype.$iter = function(cb) {
            /*
             * pagination method for Django Rest Framework
             */
            var _this_resource = this;
            console.log(_this_resource);

            if (_this_resource.next) {
                $http.get(_this_resource.next).success(function(data){
                    // reset the next and previous page api url.
                    _this_resource.next = data.next;
                    _this_resource.previous = data.previous;

                    // append newly fetched results to exsiting results
                    for ( i in data.results ) {
                        _this_resource.results.push(data.results[i]);
                    }

                    // callback
                    if (cb) cb(data);
                });
            }
        };

        resource.prototype.$loadall = function (cb) {
            var _this = this;
            if (this.results.length < this.count) {
                this.$iter(function(){
                    _this.$loadall();
                });
            } else {
                return;
            }
            if (cb) cb(this.results.length);
        }

        return resource;
    };

})
.factory('userFactory', [
    'RestResource',
    function($resource) {
        return $resource('/api/users/:username/', {
            username: "@username",
        });
    }
])
.factory('applicationCaseFactory', [
    'RestResource',
    function($resource){
        return $resource('/api/applicationcase/:case_id/',{
            case_id: "@id"
        },{
            query: {}
        });
    }
])
.factory('applicationFactory', [
    'RestResource',
    function($resource) {
        return $resource('/api/applications/:application_id/', {
            application_id: "@id"
        },
        {
            query: {}
        });
    }
])
.factory('commentFactory', [
    'RestResource',
    function($resource) {
        return $resource('/api/comments/:comment_id/', {
            comment_id: "@id"
        });
    }
])
.factory('applicantFactory', [
    'RestResource',
    function($resource) {
        return $resource('/api/applicants/:applicant_id/', {
            applicant_id: "@id"
        },
        {
            query: {}
        });
    }
])

/* Controllers */
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
.controller('CaseListCtrl', function(applicationFactory, $scope){
    applicationFactory.query(function(data){
        console.log('get case list');
        console.log($scope.cases);
        $scope.cases = data.results;
    });
})
.controller('CaseDetailCtrl', function($mdToast, applicationFactory, commentFactory, $rootScope, $scope, $routeParams, $mdToast){
    $rootScope.checkingListTable = {};
    $scope.case = applicationFactory.get({application_id: $routeParams.id}, function(data) {
        console.log('get case instance:');
        console.log(data);
        console.log($scope.case);
        $scope.comments = $scope.case.comments;
        $scope.syncCheckingList();
    });

    $scope.printNotifyForm = function(){
        $scope.commitModification(function(){
            var app_id = $scope.case.id;

            ifrm = document.createElement("iframe");
            ifrm.setAttribute("src", "http://" + document.location.host + "/app/case-printing/" + app_id + "/");
            ifrm.setAttribute("style", "display: None;");
            document.body.appendChild(ifrm);
            ifrm.contentWindow.print();
            
        });
    }

    $scope.syncCheckingList = function () {
        var data_src = $scope.case.handovered_forms;
        var true_ids = _.map(data_src, function(doc) {
            return doc.form_type;
        });

        for ( id in true_ids ) {
            $rootScope.checkingListTable[true_ids[id]] = true;
        }

        $scope.updateHandovered();
    }

    $scope.updateHandovered = function () {
        $scope.case.handovered_forms_string = _.map($rootScope.checkingListTable, function(v, k) { if (v) return parseInt(k); });
        $scope.case.handovered_forms_string = _.filter($scope.case.handovered_forms_string, function (v) { return v; });
    }

    $scope.commitModification = function(after_function){
        var caseModel_toUpdate = _.extend({}, $scope.case);

        caseModel_toUpdate.application_case = caseModel_toUpdate.application_case.id;
        caseModel_toUpdate.author_username = $rootScope.current_user.username;

        caseModel_toUpdate.$update().then(function(data){
            console.log('updated:');
            console.log(data);
            var successToast = $mdToast
                .simple()
                .content("案件修改完成。");
            $mdToast.show(successToast);

            if (after_function) { after_function(); }

        }, function(data) {
            var errorText = data.status + " " + data.statusText;
            var errorToast = $mdToast
                .simple()
                .content("案件儲存發生錯誤：" + errorText + "，請稍候再試。");
            $mdToast.show(errorToast);
        });
    }

    $scope.submitComment = function() {
        var comment = new commentFactory({
            content: $scope.comment_content,
            target: $scope.case.id,
            author: $rootScope.current_user.pk
        });
        comment.$save().then(function(data){
            var successToast = $mdToast
                .simple()
                .content("Comment sent.");

            $scope.comment_content = "";
            $scope.comments.push(comment);

        });
    }
    
})
.controller('CaseAddCtrl', function($mdToast, applicationCaseFactory, applicationFactory, $rootScope, $scope, $location){
    $rootScope.handoveredDocumentTemp = {};
    
    $scope.applicationCase_r = applicationCaseFactory.query(function(data){
        console.log($scope.caseOptions);
        $scope.applicationCase_r.$loadall();
    });

    $scope.caseModel = new applicationFactory();

    $scope.clearHandovered = function () {
        $rootScope.handoveredDocumentTemp = {};
    }
    $scope.updateHandovered = function() {
        
        $scope.caseModel.handovered_forms_string = _.map($rootScope.handoveredDocumentTemp, function (v, k) { if (v) return parseInt(k); });
        $scope.caseModel.handovered_forms_string = _.filter($scope.caseModel.handovered_forms_string, function(v) {return v;});

    }

    $scope.saveCase = function(){
        var caseModel_toSubmit = _.extend({}, $scope.caseModel);
        
        // injection to data for submitting
        caseModel_toSubmit.application_case = caseModel_toSubmit.application_case.id;
        caseModel_toSubmit.author_username = $rootScope.current_user.username;

        caseModel_toSubmit.$save().then(function(data){
            var new_application_id = data.id;
            $location.path('/cases/' + new_application_id.toString());

            var successToast = $mdToast
                .simple()
                .content("案件新增完成。");
            $mdToast.show(successToast);

        }, function(data) {
            var errorText = data.status + " " + data.statusText;
            var errorToast = $mdToast
                .simple()
                .content("案件新增發生錯誤：" + errorText + "，請稍候再試。");
            $mdToast.show(errorToast);
        });
    }

})
.controller('ProfileCtrl', function($scope, $http, userFactory, $mdToast, $cookies){
    $scope.SAVE_TIMEOUT = 2000;
    $scope.user = userFactory.get({username: 'me'}, function(data) {

        // set watcher after the data has been loaded.
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
})
.controller('ApplicantListCtrl', function($scope, applicantFactory) {
    $scope.applicant_r = applicantFactory.query(function(data){
        console.log(data);
    });
})
;

