vistagrid.controller('LoginController', ['$scope', '$cookies', '$location',
 function($scope, $cookies, $location){
	$(".animation").typed({
		strings: ["Upload", "Access", "Edit", "Share"],
		typeSpeed: 70,
		backDelay: 70,
		loop: true,
		cursorChar: " | "
	 });
	 $('.slider').slider({height: 120, indicators: false, interval : 2000});

     if ($cookies.get('isLoggedIn')) {
        $location.path('/dashboard');
     }
}]);