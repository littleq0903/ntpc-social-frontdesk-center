angular.module('services.djangorestresource', ['ngResource'])

/* Factories */
.factory('DjangoRestResource', function($resource, $http, $rootScope) {
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
                $rootScope.moreLoadingStatus = $rootScope.moreLoadingStatus_pending;
                $http.get(_this_resource.next).success(function(data){
                    // reset the next and previous page api url.
                    _this_resource.next = data.next;
                    _this_resource.previous = data.previous;

                    // append newly fetched results to exsiting results
                    for ( i in data.results ) {
                        _this_resource.results.push(data.results[i]);
                    }

                    $rootScope.moreLoadingStatus = $rootScope.moreLoadingStatus_stop;
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