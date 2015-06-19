angular.module('resources.application', [
	'services.djangorestresource',
])

.factory('applicationFactory', [
    'DjangoRestResource',
    function($resource) {
        return $resource('/api/applications/:application_id/', {
            application_id: "@id"
        },
        {
            query: {}
        });
    }
])