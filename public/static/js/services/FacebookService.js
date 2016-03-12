vistagrid.factory('FacebookService', ['$q', '$rootScope', '$window', function ($q, $rootScope, $window) {

	var checkLoginStatus = function () {
		var deferred = $q.defer();
		window.fbAsyncInit = function() {
			FB.init({
				appId      : '1578038259153196',
				xfbml      : true,
				version    : 'v2.5'
			});

			FB.getLoginStatus(function (response) {
				if (response.status === 'connected') {
					deferred.resolve(response);
				} else {
					deferred.reject(response);
				}
			});
		};
		(function(d, s, id){
			var js, fjs = d.getElementsByTagName(s)[0];
			if (d.getElementById(id)) {return;}
				js = d.createElement(s); js.id = id;
				js.src = "//connect.facebook.net/en_US/sdk.js";
				fjs.parentNode.insertBefore(js, fjs);
		}(document, 'script', 'facebook-jssdk'));
		return deferred.promise;
	};

	return {
		loginStatus: checkLoginStatus
	};
}]);