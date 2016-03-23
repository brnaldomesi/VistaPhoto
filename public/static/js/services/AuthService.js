vistagrid.factory('AuthService', ['$resource',
    function ($resource) {
        return {
            loginStatus: $resource('/api/login/status/', {}, {
                get: {
                    method: 'GET',
                    isArray: false
                }
            })
        }
}]);