angular.module('resources.applicationcase', [
	'services.djangorestresource',
])

.factory('applicationCaseFactory', [
    'DjangoRestResource',
    function($resource){
        return $resource('/api/applicationcase/:case_id/',{
            case_id: "@id"
        },{
            query: {}
        });
    }
])