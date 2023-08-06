/**
 * Copyright 2016 IBM Corp.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */

(function() {
  'use strict';

  angular
    .module('horizon.dashboard.project.queues')
    .controller('horizon.dashboard.project.queues.steps.QueueDetailsController', controller);

  controller.$inject = [
    '$scope'
  ];

  /**
   * @ngdoc controller
   * @name horizon.dashboard.project.queues.steps.QueueDetailsController
   * @param {Object} $scope
   * @returns {undefined} Returns nothing
   * @description This controller is use for creating a queue.
   */
  function controller($scope) {

    var ctrl = this;
    ctrl.queue = $scope.queue ? $scope.queue : {};
    ctrl.update = $scope.queue;

    $scope.stepModels.queueDetailsForm = ctrl.queue;
  } // end of controller
})();
