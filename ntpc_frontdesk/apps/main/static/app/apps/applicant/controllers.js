angular.module('apps.applicant.controllers', [
    'resources.applicant',
])

.controller('ApplicantListCtrl', function($scope, applicantFactory) {
    $scope.applicant_r = applicantFactory.query(function(data){
        console.log(data);
    });
})
.controller('ApplicantDetailCtrl', function($scope, applicantFactory, $routeParams, $mdToast){
	$scope.applicant = applicantFactory.get({applicant_id: $routeParams.id_no}, function (data) {
		console.log('got applicant instance:');
		console.log(data);
	});

	$scope.commitModification = function(){
		$scope.applicant.$update().then(function(data){
            console.log('updated:');
            console.log(data);
            var successToast = $mdToast
                .simple()
                .content("申請人資料修改完成。");
            $mdToast.show(successToast);

            if (after_function) { after_function(); }

        }, function(data) {
            var errorText = data.status + " " + data.statusText;
            var errorToast = $mdToast
                .simple()
                .content("申請人資料儲存發生錯誤：" + errorText + "，請稍候再試。");
            $mdToast.show(errorToast);

		})
	};
})