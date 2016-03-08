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
				},
				upload: {
					method: 'POST'
				}
			}),
			Thumbnails: $resource('/api/effects/:effect_id/', {effect_id: '@effect_id'}, {
				getAll: {
					method: 'GET',
					isArray: true
				},
				create: {
					method: 'POST'
				}
			})
		}
}]);