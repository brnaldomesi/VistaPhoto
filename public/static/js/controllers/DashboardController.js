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

		$scope.uploadClicked = function (photo_id) {
			var data = {
				photo_id: photo_id
			};
			PhotoService.Uploads.getOne(data).$promise.then(
				function (response) {
					$scope.showMain = true;
					$scope.clickedPhoto = response;
				},
				function (error) {

				}
			);
		};
}]);