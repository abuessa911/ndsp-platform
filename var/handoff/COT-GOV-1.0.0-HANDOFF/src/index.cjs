'use strict';

const dominance = require('./shared/dominance.cjs');
const calendar = require('./timing/report-calendar.cjs');
const dayControl = require('./timing/day-control.cjs');
const investment = require('./investment/investment-engine.cjs');
const speculation = require('./speculation/speculation-engine.cjs');
const shadow = require('./shadow/perspective-runner.cjs');
const publicView = require('./public/public-view.cjs');

module.exports = {
  ...dominance,
  ...calendar,
  ...dayControl,
  ...investment,
  ...speculation,
  ...shadow,
  ...publicView
};
