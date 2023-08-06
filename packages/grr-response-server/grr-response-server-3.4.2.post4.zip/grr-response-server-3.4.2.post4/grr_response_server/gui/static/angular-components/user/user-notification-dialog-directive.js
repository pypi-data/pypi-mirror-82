goog.module('grrUi.user.userNotificationDialogDirective');
goog.module.declareLegacyNamespace();



/**
 * Controller for UserNotificationDialogDirective.
 * @unrestricted
 */
const UserNotificationDialogController = class {
  /**
   * @param {!angular.Scope} $scope
   * @ngInject
   */
  constructor($scope) {
    /** @private {!angular.Scope} */
    this.scope_ = $scope;

    /** @type {string} */
    this.notificationUrl = 'users/me/notifications';
  }
};



/**
 * Directive for showing the notification dialog.
 *
 * @return {!angular.Directive} Directive definition object.
 * @ngInject
 * @export
 */
exports.UserNotificationDialogDirective = function() {
  return {
    scope: {close: '&'},
    restrict: 'E',
    templateUrl:
        '/static/angular-components/user/user-notification-dialog.html',
    controller: UserNotificationDialogController,
    controllerAs: 'controller'
  };
};


/**
 * Directive's name in Angular.
 *
 * @const
 * @export
 */
exports.UserNotificationDialogDirective.directive_name =
    'grrUserNotificationDialog';
