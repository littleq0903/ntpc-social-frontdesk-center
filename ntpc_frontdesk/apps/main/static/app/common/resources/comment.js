angular.module('resources.comment', [
	'services.djangorestresource',
])

.factory('commentFactory', [
    'DjangoRestResource',
    function($resource) {
        return $resource('/api/comments/:comment_id/', {
            comment_id: "@id"
        });
    }
])