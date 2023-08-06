/**
 * @param {string} module
 * @return {Function}
 */
var minErr = function(module) {
  return function() {};
};


/**
 * @param {!angular.JQLite} element
 * @return {string} Returns the string representation of the element.
 */
var startingTag = function(element) {
  return '';
};


/**
 * @type {Object}
 * @const
 */
var grr = {};


/**
 * @param {string=} opt_hash
 */
grr.loadFromHash = function(opt_hash) {};


/**
 * @param {string} renderer
 * @param {string} domId
 * @param {Object=} opt_state
 *     the AJAX request (as query parameters).
 * @param {Function=} opt_onSuccess
 *     completion.
 */
grr.layout = function(renderer, domId, opt_state, opt_onSuccess) {};


/**
 * @type {Object}
 */
grr.labels_completer = {};


/**
 * @param {(jQuerySelector|Element|jQuery|string)} element
 * @param {Array<string>} completions
 * @param {RegExp} regex
 */
grr.labels_completer.Completer = function(element, completions, regex) {};


/**
 * @type {Object}
 */
grr.glob_completer = {};


/**
 * @param {(jQuerySelector|Element|jQuery|string)} element
 * @param {Array<string>} completions
 */
grr.glob_completer.Completer = function(element, completions) {};


/**
 * @type {Object<string, string>}
 */
grr.hash;


/**
 * @type {Object<string, string>}
 */
grr.state;


/**
 * @param {string} hash
 * @return {Object}
 */
grr.parseHashState = function(hash) {};


/**
 * @param {string} name
 * @param {string} value
 * @param {Object=} opt_event
 * @param {Object=} opt_data
 */
grr.publish = function(name, value, opt_event, opt_data) {};


/**
 * A jQuery object that has been extended with Angular's extra methods.
 * @typedef {(jQuery|angular.JQLite)}
 */
angular.jQuery;


/**
 * Angular UI definitions.
 */


/**
 * @type {Object}
 * @const
 */
var angularUi = {};


/**
 * @typedef {{
 *   close: function(string=),
 *   dismiss: function(string=),
 *   result: angular.$q.Promise
 *   }}
 */
angularUi.$uibModalInstance;


/**
 * @typedef {{
 *   open: function(Object): angularUi.$uibModalInstance
 *   }}
 */
angularUi.$uibModal;


/**
 * @param {(jQuerySelector|Element|jQuery|string)} placeholder
 * @param {Array} data
 * @param {Object=} opt_options
 */
$.plot = function(placeholder, data, opt_options) {};


/**
 * @param {Object} data
 */
jQuery.prototype.jstree = function(data) {};


/**
 * @typedef {{
 *   as: function(string):number,
 *   asSeconds: function():number,
 *   humanize: function(boolean=):string
 * }}
 */
moment.Duration;


/**
 * Angular UI definitions.
 */


/**
 * Suppresses the compiler warning when multiple externs files declare the
 * ui namespace.
 * @suppress {duplicate}
 */
var ui = {};


/**
 * @type {Object}
 * @const
 */
ui.router = {};


/**
 * @typedef {{
 *   params: Object,
 *   current: !ui.router.State,
 *   transition: ?angular.$q.Promise,
 *   get: function(...),
 *   go: function(...),
 *   href: function(...),
 *   includes: function(...),
 *   is: function(...),
 *   reload: function(...),
 *   transitionTo: function(...)
 * }}
 */
ui.router.$state;


/**
 * @type {ui.router.State}
 */
ui.router.$state.current;


/**
 * @type {Object}
 */
ui.router.$state.params;


/**
 * @type {?angular.$q.Promise}
 */
ui.router.$state.transition;


/**
 * @param {?string|Object=} opt_stateOrName
 * @param {?string|Object=} opt_context
 * @return {Object|Array}
 */
ui.router.$state.get = function(opt_stateOrName, opt_context) {};

/**
 * @typedef {{
 *   location: (boolean|string|undefined),
 *   inherit: (boolean|undefined),
 *   relative: (Object|undefined),
 *   notify: (boolean|undefined),
 *   reload: (boolean|undefined)
 * }}
 */
ui.router.$state.GoOptions_;

/**
 * @param {string} to
 * @param {Object=} opt_params
 * @param {(ui.router.$state.GoOptions_|Object)=} opt_options
 * @return {angular.$q.Promise}
 */
ui.router.$state.go = function(to, opt_params, opt_options) {};


/**
 * @param {?string|Object} stateOrName
 * @param {Object=} opt_params
 * @param {Object=} opt_options
 * @return {string} compiled state url
 */
ui.router.$state.href = function(stateOrName, opt_params, opt_options) {};


/**
 * @param {?string} stateOrName
 * @param {Object=} opt_params
 * @param {Object=} opt_options
 */
ui.router.$state.includes = function(stateOrName, opt_params, opt_options) {};


/**
 * @param {?string|Object} stateOrName
 * @param {Object=} opt_params
 * @param {Object=} opt_options
 * @return {boolean}
 */
ui.router.$state.is = function(stateOrName, opt_params, opt_options) {};


/**
 * @return {angular.$q.Promise}
 */
ui.router.$state.reload = function() {};


/**
 * @param {string} to
 * @param {Object=} opt_toParams
 * @param {Object=} opt_options
 */
ui.router.$state.transitionTo = function(to, opt_toParams, opt_options) {};


/**
 * @typedef {Object.<string, string>}
 */
ui.router.$stateParams;


/**
 * This is the object that the ui-router passes to callback functions listening
 * on ui router events such as `$stateChangeStart` or
 * `$stateChangeError` as the `toState` and `fromState`.
 * Example:
 * $rootScope.$on('$stateChangeStart', function(
 *     event, toState, toParams, fromState, fromParams){ ... });
 *
 * @typedef {{
 *     'abstract': (boolean|undefined),
 *     controller: (string|Function|undefined),
 *     controllerAs: (string|undefined),
 *     controllerProvider: (Function|undefined),
 *     data: (Object|undefined),
 *     name: string,
 *     onEnter: (Object|undefined),
 *     onExit: (Object|undefined),
 *     params: (Object|undefined),
 *     reloadOnSearch: (boolean|undefined),
 *     resolve: (Object.<string, !Function>|undefined),
 *     template: (string|Function|undefined),
 *     templateUrl: (string|Function|undefined),
 *     templateProvider: (Function|undefined),
 *     url: (string|undefined),
 *     views: (Object|undefined)
 * }}
 */
ui.router.State;



/** @unrestricted */
ui.router.$urlMatcherFactory = class {
  constructor() {}
};



/** @unrestricted */
ui.router.$urlRouterProvider = class {
  /**
   * @param {!ui.router.$urlMatcherFactory} $urlMatcherFactory
   */
  constructor($urlMatcherFactory) {}

  /**
   * @param {string|RegExp} url
   * @param {string|function(...)|Array.<!Object>} route
   */
  when(url, route) {}

  /**
   * @param {string|function(...)} path
   */
  otherwise(path) {}

  /**
   * @param {function(...)} rule
   */
  rule(rule) {}

  /**
   * Defers URL interception.
   */
  deferIntercept() {}

  /**
   * Syncs the $urlRouterProvider with the URL.
   */
  sync() {}

  /**
   * Re-attaches the $urlRouterProvider to listen for changes in the URL.
   */
  listen() {}
};



/** @unrestricted */
ui.router.$stateProvider = class {
  /**
   * @param {!ui.router.$urlRouterProvider} $urlRouterProvider
   * @param {!ui.router.$urlMatcherFactory} $urlMatcherFactory
   * @param {!angular.$locationProvider} $locationProvider
   */
  constructor($urlRouterProvider, $urlMatcherFactory, $locationProvider) {}

  /**
   * @param {!string} name
   * @param {Object} definition
   * @return {!ui.router.$stateProvider}
   */
  state(name, definition) {}
};



/**
 * @param {!string} source
 * @return {!string}
 */
var marked = function(source) {};

/**
 * @param {Array<HTMLElement|string>} elements
 * @param {Object=} options
 * @return {Object}
 */
var Split = function(elements, options) {};
