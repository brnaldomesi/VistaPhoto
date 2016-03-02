vistagrid.controller('DashboardController',
	['$scope', 'PhotoService', function ($scope, PhotoService) {
		PhotoService.Uploads.getAll().$promise.then(
			function (response) {
				$scope.uploads = response;
				console.log($scope.uploads);
			},
			function (error) {
				console.log(error);
			}
		);
}]);