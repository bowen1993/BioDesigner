var ProController = angular.module('ProController', ['ngMaterial']);

ProController.controller('MainCtrl',function($scope, $http, $location, $mdDialog, $mdMedia, $mdToast){
	$scope.project_info = [];
	$scope.isEdit = false
	$scope.isChosen = false;
	$scope.toggle_device = function(index){
		$scope.getDevices(index, $scope.project_info[index].id);

		$scope.project_info[index].isDeviceShowed = !$scope.project_info[index].isDeviceShowed;
	}
	$scope.devcie_img_src ="/static/img/logo_design.png"
	$scope.update = function(){
		$scope.project_info = [];
		$scope.init();
	}
	$scope.init = function(){
		$http.get("/home/getUserProject").success(function(data){
			if( data.isSuccessful ){
				var projects = data.projects;
				for(var i = 0; i < projects.length; i++){
					$scope.project_info.push({
						id:projects[i].id,
						name:projects[i].name,
						devices:[],
						isDeviceShowed:true,
						track:projects[i].track,
						function:projects[i].function,
						creator:projects[i].creator
					});
				}
			}
		});
	}
	$scope.getDevices = function(index, id){
		$http.get("/home/getChainList?id="+id).success(function(data){
			$scope.project_info[index].devices = data;
		});
	}
	$scope.device_clicked = function(device_id){
		$scope.isChosen = true;
		$http.get('/home/getResultImage?id='+device_id).success(function(data){
			if(data.isSuccessful){
				console.log(data);
				$scope.devcie_img_src = data.filepath;
			}else{
				console.log(data);
			}
		});
	}
	$scope.toggle_edit = function(){
		$scope.isEdit = !$scope.isEdit;

	}
	$scope.delete_device = function(device_id){

	}
	$scope.showNewDeviceDialog = function(ev, project_id){
		var useFullScreen = ($mdMedia('sm') || $mdMedia('xs')) && $scope.customFullscreen;
		$mdDialog.show({
			controller:NewDeviceCtrl,
			templateUrl:'/static/html/new_device.tmp.html',
			parent:angular.element(document.body.div),
			targetEvent:ev,
			clickOutsideToClose:true,
			fullscreen: useFullScreen,
			locals:{$http:$http, $mdToast,$mdToast, project_id: project_id}
		}).then(function(answer){
			$scope.update();
		}, function(){
			$scope.update();
		});
		$scope.$watch(function(){
			return $mdMedia('xs') || $mdMedia('sm');
		}, function(wantsFullScreen){
			$scope.customFullscreen = (wantsFullScreen === true);
		});
	}
	$scope.showNewProjectDialog = function(ev){
		var useFullScreen = ($mdMedia('sm') || $mdMedia('xs')) && $scope.customFullscreen;
		$mdDialog.show({
			controller: NewProjectCtrl,
			templateUrl:'/static/html/new_project.tmp.html',
			parent:angular.element(document.body.div),
			targetEvent: ev,
			clickOutsideToClose:true,
			fullscreen: useFullScreen,
			locals: {$http: $http, $mdToast:$mdToast}
		}).then(function(answer){
			$scope.update();
		}, function(){
			$scope.update();
		});
		$scope.$watch(function(){
			return $mdMedia('xs') || $mdMedia('sm');
		}, function(wantsFullScreen){
			$scope.customFullscreen = (wantsFullScreen === true);
		});
	}
	$scope.delete_project = function(index, id){
		var opt = {
			url: '/home/deleteProject',
			method: 'POST',
			data:JSON.stringify({
				id:id
			}),
			headers: { 'Content-Type': 'application/json' }
		};
		$http(opt).success(function(data){
			if( data.isSuccessful ){
				$scope.project_info.splice(index, 1);
				showToast($mdToast, "Project deleted successfully");
			}else{
				showToast($mdToast, "Project deleted FAILED")
			}
		});
	}

	$scope.init();

});

function NewDeviceCtrl($scope, $mdDialog, $http, $mdToast, project_id){
	$scope.new_device_name = "";
	$scope.project_id = project_id;
	$scope.hide = function() {
		$mdDialog.hide();
	}
	$scope.cancel = function() {
		$mdDialog.cancel();
	}
	$scope.create_device = function(){
		var opt = {
			url: "/home/newDevice",
			method:'POST',
			data:JSON.stringify({
				name:$scope.new_device_name,
				id:project_id
			}),
			headers: {'Content-Type': 'application/json'}
		}
		$http(opt).success(function(data){
			if( $scope.new_device_name.length == 0 ){
				return;
			}else{
				if( data.isSuccessful ){
					showToast($mdToast, "Device created SUCCESS");
					$mdDialog.hide();
				}else{
					showToast($mdToast, "Device created FAILED");
					$mdDialog.hide();
				}
			}
		})
	}

}

function NewProjectCtrl($scope, $mdDialog, $http, $mdToast){
	$scope.tracks = [];
	$scope.new_project_track = "";
	$scope.new_project_name = "";
	$scope.init = function(){
		$http.get('/home/tracks').success(function(data){
			if( data.isSuccessful ){
				$scope.tracks = data.tracks;
				console.log($scope.tracks);
			}
		});
	}
	$scope.init();
	$scope.hide = function() {
		$mdDialog.hide();
	};
	$scope.cancel = function() {
		$mdDialog.cancel();
	};
	$scope.create_project = function(){
		if( $scope.new_project_track.length == 0 || $scope.new_project_name.length == 0){
			return;
		}else{
			var opt = {
				url: '/home/newProject',
				method: 'POST',
				data:JSON.stringify({
					name:$scope.new_project_name,
					track:$scope.new_project_track
				}),
				headers: { 'Content-Type': 'application/json' }
			};
			$http(opt).success(function(data){
				if( data.isSuccessful ){
					$mdDialog.hide();
					showToast($mdToast, "Project created successfully");
				}else{
					showToast($mdToast, "Project created FAILED")
				}
			});
		}
	}
}

var last = {
    bottom: false,
    top: true,
    left: false,
    right: true
};

var toastPosition = angular.extend({},last);

function sanitizePosition() {
	var current = toastPosition;
	if ( current.bottom && last.top ) current.top = false;
	if ( current.top && last.bottom ) current.bottom = false;
	if ( current.right && last.left ) current.left = false;
	if ( current.left && last.right ) current.right = false;
	last = angular.extend({},current);
}

var getToastPosition = function() {
    sanitizePosition();
    return Object.keys(toastPosition)
      .filter(function(pos) { return toastPosition[pos]; })
      .join(' ');
};

function showToast($mdToast, msg){
	var pinTo = getToastPosition();
    var toast = $mdToast.simple()
      .textContent(msg)
      .highlightAction(true)
      .position(pinTo);
    $mdToast.show(toast).then(function(response) {
      if ( response == 'ok' ) {
      }
    });
}