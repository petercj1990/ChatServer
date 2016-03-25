(function() {

	angular
	.module('eightBall')
	.service('eightBallService',  function($http){
		this.getFortune= function () {
			return $http({
				method: 'GET',
				url:'/fortune'

			}).then(function (response) {
				console.log(response);
				return response.data;
			})
		}
	})
})()