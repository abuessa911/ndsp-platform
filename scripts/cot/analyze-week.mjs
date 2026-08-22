#!/usr/bin/env node

import { readFile } from 'node:fs/promises';

import {
  analyzeCotDirection,
  analyzeNamedCoalition,
  compareCanonicalCoalitions,
} from '../../backend/intelligence/cot-direction/index.js';

async function readInput(path) {
  if (path === '-') {
    const chunks = [];

    for await (const chunk of process.stdin) {
      chunks.push(chunk);
    }

    return Buffer.concat(chunks).toString('utf8');
  }

  return readFile(path, 'utf8');
}

async function main() {
  const inputPath = process.argv[2];

  if (!inputPath) {
    throw new Error(
      'حدد ملف JSON: node scripts/cot/analyze-week.mjs input.json',
    );
  }

  const payload = JSON.parse(await readInput(inputPath));

  let analysis;

  if (payload.compareCanonicalCoalitions === true) {
    analysis = compareCanonicalCoalitions(
      payload.participants,
    );
  } else if (payload.coalitionKey) {
    analysis = analyzeNamedCoalition(
      payload.coalitionKey,
      payload.participants,
    );
  } else {
    analysis = analyzeCotDirection(payload.participants);
  }

  process.stdout.write(
    `${JSON.stringify(
      {
        marketSymbol: payload.marketSymbol ?? null,
        reportDate: payload.reportDate ?? null,
        ...analysis,
      },
      null,
      2,
    )}\n`,
  );
}

main().catch((error) => {
  console.error(
    JSON.stringify(
      {
        error: error.name ?? 'Error',
        message: error.message,
        details: error.details ?? null,
      },
      null,
      2,
    ),
  );

  process.exitCode = 1;
});
