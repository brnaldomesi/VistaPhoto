var vistagrid = angular.module('vistagrid', ['ngRoute', 'ngResource', 'ngFileUpload']);

vistagrid.config(function ($interpolateProvider) {
	$interpolateProvider.startSymbol('[[');
	$interpolateProvider.endSymbol(']]');
});

vistagrid.config(['$resourceProvider', function ($resourceProvider) {
	$resourceProvider.defaults.stripTrailingSlashes = false;
}]);

vistagrid.config(function ($routeProvider) {
	$routeProvider
	.when('/', {
		templateUrl: 'static/views/login.html',
		controller: 'LoginController'
	})
	.when('/dashboard', {
		templateUrl: 'static/views/dashboard.html',
		controller: 'DashboardController'
	})
	.otherwise({
		redirectTo: '/'
	});
});

vistagrid.config(function ($httpProvider) {
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});