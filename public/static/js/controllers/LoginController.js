vistagrid.controller('LoginController', ['$scope', '$cookies', '$location', 'AuthService',
 function($scope, $cookies, $location, AuthService){
	$(".animation").typed({
		strings: ["Upload", "Access", "Edit", "Share"],
		typeSpeed: 70,
		backDelay: 70,
		loop: true,
		cursorChar: " | "
	 });
	 $('.slider').slider({height: 120, indicators: false, interval : 2000});

     // Redirect to dashboard if user is logged in
     AuthService.loginStatus.get().$promise.then(
        function (response) {
            $location.path('/dashboard');
        },
        function (error) {

        }
    );
}]);