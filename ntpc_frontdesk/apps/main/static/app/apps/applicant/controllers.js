angular.module('apps.applicant.controllers', [
    'resources.applicant',
])

.controller('ApplicantListCtrl', function($scope, applicantFactory) {
    $scope.applicant_r = applicantFactory.query(function(data){
        console.log(data);
    });
})