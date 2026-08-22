'use strict';

const CONTROLLER = Object.freeze({
  LONG_TERM: 'LONG_TERM',
  SHORT_TERM: 'SHORT_TERM'
});

const DAY_NAMES = Object.freeze([
  'SUNDAY',
  'MONDAY',
  'TUESDAY',
  'WEDNESDAY',
  'THURSDAY',
  'FRIDAY',
  'SATURDAY'
]);

const PERSPECTIVES = Object.freeze({
  D1: Object.freeze({
    MONDAY: CONTROLLER.LONG_TERM,
    TUESDAY: CONTROLLER.SHORT_TERM,
    WEDNESDAY: CONTROLLER.SHORT_TERM,
    THURSDAY: CONTROLLER.SHORT_TERM,
    FRIDAY: CONTROLLER.LONG_TERM,
    SATURDAY: CONTROLLER.SHORT_TERM,
    SUNDAY: CONTROLLER.SHORT_TERM
  }),
  D2: Object.freeze({
    MONDAY: CONTROLLER.SHORT_TERM,
    TUESDAY: CONTROLLER.SHORT_TERM,
    WEDNESDAY: CONTROLLER.SHORT_TERM,
    THURSDAY: CONTROLLER.LONG_TERM,
    FRIDAY: CONTROLLER.LONG_TERM,
    SATURDAY: CONTROLLER.SHORT_TERM,
    SUNDAY: CONTROLLER.SHORT_TERM
  })
});

function controllerForTimestamp(timestamp, perspectiveName) {
  const perspective = PERSPECTIVES[perspectiveName];

  if (!perspective) {
    throw new Error(`Unknown day-control perspective: ${perspectiveName}`);
  }

  const date = new Date(timestamp);

  if (Number.isNaN(date.getTime())) {
    throw new TypeError('Invalid UTC timestamp');
  }

  const dayName = DAY_NAMES[date.getUTCDay()];

  return {
    canonicalTimezone: 'UTC',
    dayName,
    controller: perspective[dayName],
    perspective: perspectiveName
  };
}

module.exports = {
  CONTROLLER,
  PERSPECTIVES,
  controllerForTimestamp
};
