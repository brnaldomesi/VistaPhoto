vistagrid.controller('DashboardController',
	['$scope', 'PhotoService', '$timeout', 'Upload', function ($scope, PhotoService, $timeout, Upload) {
		$scope.uploader = {};
		var refreshThumbnails = function () {
			PhotoService.Thumbnails.getAll().$promise.then(
				function (response) {
					$scope.thumbnails = response;
				},
				function (error) {

				}
			);
		}

		var fetchUploads = function () {
			PhotoService.Uploads.getAll().$promise.then(
				function (response) {
					$scope.uploads = response;
				},
				function (error) {
					console.log(error);
				}
			);
		}

		fetchUploads();

		$scope.uploadClicked = function (photo_id, path) {
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
			data = {
				path: path
			};
			console.log(data);
			PhotoService.Thumbnails.create(data).$promise.then(
				function (response) {
					console.log(response);
					refreshThumbnails();
				},
				function (error) {
					console.log(error);
				}
			);
		};

		$scope.uploadNewPhoto = function (file, errFiles) {
			if (file) {
				console.log(file);
				var data = {
					url: '/api/photos/',
					data: {
						path: file,
						filter_effects: 'BLUR'
					}
				}
				Upload.upload(data).then(
					function (response) {
						console.log('Successful upload!!');
						fetchUploads();
					},
					function (error) {
						console.log(error);
					}
				);
			}
		}
}]);