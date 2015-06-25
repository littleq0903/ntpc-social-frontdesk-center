angular.module('resources.applicant', [
	'services.djangorestresource',
])

.factory('applicantFactory', [
    'DjangoRestResource',
    function($resource) {
        return $resource('/api/applicants/:applicant_id/', {
            applicant_id: "@id_no"
        },
        {
            query: {}
        });
    }
])