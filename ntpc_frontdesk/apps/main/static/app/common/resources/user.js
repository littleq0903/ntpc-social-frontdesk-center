angular.module('resources.user', [
	'services.djangorestresource',
])

.factory('userFactory', [
    'DjangoRestResource',
    function($resource) {
        return $resource('/api/users/:username/', {
            username: "@username",
        });
    }
])