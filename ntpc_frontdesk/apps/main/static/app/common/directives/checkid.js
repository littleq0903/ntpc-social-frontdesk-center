angular.module('directives.checkid', [])

/* ROC ID Validation Directive */
.directive('checkid', function(){
    function checkID( id ) {
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
    
    return {
        require: 'ngModel',
        link: function(scope, elm, attrs, ctrl, ngModel) {
            ctrl.$validators["checkid"] = function (modelValue, viewValue){
                if (ctrl.$isEmpty(modelValue)) {
                    return true;
                }
                return checkID(viewValue);
            }
        }
    };
})