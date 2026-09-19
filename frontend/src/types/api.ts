import { AiMode, ErrorCode } from './contracts';

export interface ResponseMeta {
  ai_mode: AiMode;
  model: string;
  degraded: boolean;
  warnings: string[];
  profile_version: number;
}

export interface SuccessEnvelope<T> {
  data: T;
  meta: ResponseMeta;
}

export interface ErrorDetails {
  code: ErrorCode;
  message: string;
  details: Record<string, unknown>;
  request_id: string;
}

export interface ErrorEnvelope {
  error: ErrorDetails;
}
