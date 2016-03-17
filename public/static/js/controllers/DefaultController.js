vistagrid.controller('DefaultController',
	['$rootScope', '$scope', '$cookies', function($rootScope, $scope, $cookies) {
        $scope.logout = function () {
            $rootScope.showLogoutButton = false;
            $cookies.remove('isLoggedIn');
        }
}]);