var bio_project = angular.module('bio_project', ['ngRoute', 'ProController','ngMaterial','ngAnimate']);

bio_project.config(['$routeProvider', function($routeProvider){
	$routeProvider.when('/', {
		templateUrl:'/static/html/project_main.html',
		controller: 'MainCtrl'
	}).otherwise({
		redirectTo:'/'
	});
}]);



