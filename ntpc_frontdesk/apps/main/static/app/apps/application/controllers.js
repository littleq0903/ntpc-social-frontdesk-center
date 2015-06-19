angular.module('apps.application.controllers', [
    'ngMaterial',

    // directives
    'directives.checkid',

    'resources.application',
    'resources.applicationcase',
    'resources.comment'
])

.controller('CaseListCtrl', function(applicationFactory, $scope){
    $scope.case_r = applicationFactory.query(function(data){
        console.log(data);
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