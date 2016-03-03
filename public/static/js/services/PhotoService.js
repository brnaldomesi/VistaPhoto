vistagrid.factory('PhotoService', ['$resource',
	function ($resource) {
		return {
			Uploads: $resource('/api/photos/:photo_id/', {photo_id: '@photo_id'}, {
				getAll: {
					method: 'GET',
					isArray: true
				},
				getOne: {
					method: 'GET',
					isArray: false
				}
			})
		}
}]);