angular.module('directives.checkid', [])

/* ROC ID Validation Directive */
.directive('checkid', function(){

    var checking_config = {
        'national': {
            'pattern': /^[A-Z][0-9]{9}$/,
            'validator': checkNationalID
        },
        'foreign': {
            'pattern': /^[A-Z]{2}[0-9]{8}$/,
            'validator': checkForeignID
        }
    }

    function checkEntryPoint ( id ) {
        /*
        This is the entry point of whole id checking mechanism, it will proceed id checking depends on
        whether it is or is not a national ID.

        format of national ID: [A-Z][0-9]{9} -> this will be checked
        format of foreign ID: [A-Z]{2}[0-9]{8} -> this will be allowed directly
        */

        for ( config_i in checking_config ) {
            var config = checking_config[config_i];

            if (id.match(config.pattern)) {
                return config.validator(id);
            }
        }

        return false;
    }

    /*
     * Validators
     */
    function checkNationalID( id ) {
        tab = "ABCDEFGHJKLMNPQRSTUVXYWZIO"
        A1 = new Array (1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3);
        A2 = new Array (0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5);
        Mx = new Array (9,8,7,6,5,4,3,2,1,1);

        if ( id.length != 10 ) return false;
        i = tab.indexOf( id.charAt(0) );
        if ( i == -1 ) return false;
        sum = A1[i] + A2[i]*9;

        for ( i=1; i<10; i++ ) {
            v = parseInt( id.charAt(i) );
            if ( isNaN(v) ) return false;
            sum = sum + v * Mx[i];
        }
        if ( sum % 10 != 0 ) return false;
        return true;
    }
    function checkForeignID( id ) {
        return true; // always returning true
    }

    return {
        require: 'ngModel',
        link: function(scope, elm, attrs, ctrl, ngModel) {
            ctrl.$validators["checkid"] = function (modelValue, viewValue){
                if (ctrl.$isEmpty(modelValue)) {
                    return true;
                }
                return checkEntryPoint(viewValue);
            }
        }
    };
})