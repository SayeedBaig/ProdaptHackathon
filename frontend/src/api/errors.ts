import { ErrorCode } from '../types/contracts';
import { ErrorEnvelope } from '../types/api';

export class ApiError extends Error {
  public readonly code: ErrorCode;
  public readonly details: Record<string, unknown>;
  public readonly request_id: string;
  public readonly status: number;

  constructor(
    code: ErrorCode,
    message: string,
    details: Record<string, unknown> = {},
    request_id = `req-${Math.random().toString(36).substring(2, 9)}`,
    status = 500
  ) {
    super(message);
    this.name = 'ApiError';
    this.code = code;
    this.details = details;
    this.request_id = request_id;
    this.status = status;
    Object.setPrototypeOf(this, ApiError.prototype);
  }

  static fromEnvelope(envelope: ErrorEnvelope, status: number): ApiError {
    return new ApiError(
      envelope.error.code,
      envelope.error.message,
      envelope.error.details,
      envelope.error.request_id,
      status
    );
  }
}
