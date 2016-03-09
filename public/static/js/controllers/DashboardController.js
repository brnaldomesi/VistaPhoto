vistagrid.controller('DashboardController',
	['$scope', 'PhotoService', '$timeout', 'Upload', function ($scope, PhotoService, $timeout, Upload) {
		var clickedPhotoID = null;
		var refreshThumbnails = function () {
			PhotoService.Thumbnails.getAll().$promise.then(
				function (response) {
					$scope.thumbnails = response;
				},
				function (error) {

				}
			);
		};

		var fetchUploads = function () {
			PhotoService.Uploads.getAll().$promise.then(
				function (response) {
					$scope.uploads = response;
				},
				function (error) {
					console.log(error);
				}
			);
		};

		fetchUploads();

		$scope.uploadClicked = function (photo_id, path) {
			var data = {
				photo_id: photo_id
			};
			clickedPhotoID = photo_id;

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
			PhotoService.Thumbnails.create(data).$promise.then(
				function (response) {
					refreshThumbnails();
				},
				function (error) {
					console.log(error);
				}
			);
		};

		$scope.uploadNewPhoto = function (file, errFiles) {
			if (file) {
				var data = {
					url: '/api/photos/',
					data: {
						path: file,
						filter_effects: 'BLUR'
					}
				}
				Upload.upload(data).then(
					function (response) {
						fetchUploads();
					},
					function (error) {
						console.log(error);
					}
				);
			}
		};

		$scope.effectPreview = function (effectID) {
			var data = {
				effect_id: effectID
			}
			PhotoService.Thumbnails.getOne(data).$promise.then(
				function (response) {
					$scope.clickedPhoto = response;
				},
				function (error) {

				}
			);
		};

		$scope.saveEdits = function () {
			if ($scope.clickedPhoto.effect_name) {
				swal(
					{
						title: "Are you sure?",
						text: "You cannot undo the changes you are about to make!",
						type: "warning",
						showCancelButton: true,
						confirmButtonColor: "#3b5998",
						confirmButtonText: "Yes, save!",
						closeOnConfirm: true
					},
					function () {
						effect_name = $scope.clickedPhoto.effect_name
						var data = {
							photo_id: clickedPhotoID,
							filter_effects: effect_name
						};
						PhotoService.Uploads.edit(data).$promise.then(
							function (response) {
								fetchUploads();
								Materialize.toast(effect_name + ' effect applied!', 5000);
								var $toastContent = $('<span style="font-weight: bold">' + effect_name + ' effect applied!</span>');
								Materialize.toast($toastContent, 5000);
							},
							function (error) {
								console.log(error);
							}
						);
					}
				);
			} else {
				var $toastContent = $('<span style="font-weight: bold">No effect selected!</span>');
				Materialize.toast($toastContent, 5000);
			}
		};

		$scope.deletePhoto = function () {
			swal(
				{
					title: "Are you sure?",
					text: "You will not be able to recover this photo!",
					type: "warning",
					showCancelButton: true,
					confirmButtonColor: "#f44336",
					confirmButtonText: "Yes, delete photo!",
					closeOnConfirm: true
				},
				function () {
					var data = {
						photo_id: clickedPhotoID
					};
					PhotoService.Uploads.delete(data).$promise.then(
						function (response) {
							fetchUploads();
							var $toastContent = $('<span style="font-weight: bold">Delete successful!</span>');
							Materialize.toast($toastContent, 5000);
						},
						function (error) {
							var $toastContent = $('<span style="font-weight: bold">An error occurred!</span>');
							Materialize.toast($toastContent, 5000);
						}
					);
				}
			);
		}
}]);