vistagrid.factory('AuthService', ['$resource',
    function ($resource) {
        return {
            loginStatus: $resource('/api/loginstatus/', {}, {
                get: {
                    method: 'GET',
                    isArray: false
                }
            })
        }
}]);