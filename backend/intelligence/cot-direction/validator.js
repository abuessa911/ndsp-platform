export class CotValidationError extends Error {
  constructor(message, details = {}) {
    super(message);
    this.name = 'CotValidationError';
    this.details = details;
  }
}

function normalizeParticipant(value) {
  if (typeof value !== 'string' || value.trim() === '') {
    throw new CotValidationError('اسم الفئة مطلوب.');
  }

  return value
    .trim()
    .toUpperCase()
    .replaceAll('-', '_')
    .replaceAll(' ', '_');
}

function requireNumber(value, field, participant) {
  if (typeof value !== 'number' || !Number.isFinite(value)) {
    throw new CotValidationError(
      `${field} يجب أن يكون رقمًا صالحًا للفئة ${participant}.`,
    );
  }

  return value;
}

export function validateParticipants(participants) {
  if (!Array.isArray(participants) || participants.length === 0) {
    throw new CotValidationError(
      'يجب إدخال فئة واحدة على الأقل.',
    );
  }

  const normalized = participants.map((row, index) => {
    if (!row || typeof row !== 'object' || Array.isArray(row)) {
      throw new CotValidationError(
        `المدخل رقم ${index} غير صالح.`,
      );
    }

    const participant = normalizeParticipant(row.participant);

    return Object.freeze({
      participant,
      longChange: requireNumber(
        row.longChange,
        'longChange',
        participant,
      ),
      shortChange: requireNumber(
        row.shortChange,
        'shortChange',
        participant,
      ),
    });
  });

  const names = normalized.map((row) => row.participant);
  const duplicates = names.filter(
    (name, index) => names.indexOf(name) !== index,
  );

  if (duplicates.length > 0) {
    throw new CotValidationError(
      `الفئة مكررة: ${[...new Set(duplicates)].join(', ')}`,
    );
  }

  return Object.freeze(normalized);
}
