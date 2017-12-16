var app = angular.module('CalcApp', ['ngMaterial', 'ngAnimate']);
app.controller('calcCtrl', function($scope, $timeout, $rootScope) {
  $scope.aclick = false;
  $scope.expr = '';
  $scope.result = '';
  $scope.getRes = function() {
    try {
      if ($scope.expr != '') {
        $scope.result = math.round(math.eval($scope.expr), 8);
      } else {
        $scope.result = '';
      }
    } catch (e) {
      $scope.result = 'Error';
    }
  };
  $scope.ac = function() {
    $timeout(function() {
      $scope.expr = '';
      $scope.result = '';
      $scope.aclick = false;
    }, 500);

  };
  $scope.clear = function() {
    if ($scope.expr.substr(-1) == ' ') {
      $scope.expr = $scope.expr.slice(0, -2);
    } else {
      $scope.expr = $scope.expr.slice(0, -1);
    }
  };
  $("#inp").keypress(function(e) {
    if (e.keyCode == 13) {
      $scope.getRes();
    }
  });
});