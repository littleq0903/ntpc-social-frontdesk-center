angular.module('apps.profile.controllers', [
    'ngCookies',
    'ngMaterial',

    'resources.user',
])

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