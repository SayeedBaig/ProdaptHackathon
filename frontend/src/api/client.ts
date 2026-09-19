import { useAuthStore } from '../store/authStore';
import { useUiStore } from '../store/uiStore';
import { ErrorEnvelope, SuccessEnvelope } from '../types/api';
import { ApiError } from './errors';
import { handleMockRequest } from '../mocks/mockClient';
import { toast } from 'sonner';

interface RequestOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  body?: unknown;
  headers?: Record<string, string>;
  signal?: AbortSignal;
  timeoutMs?: number;
  profileVersion?: number;
  skipGlobalErrorToast?: boolean;
}

// Global active in-flight map to prevent accidental double-submits on mutating requests
const inFlightMutations = new Set<string>();

export async function apiClient<T>(
  url: string,
  options: RequestOptions = {}
): Promise<SuccessEnvelope<T>> {
  const {
    method = 'GET',
    body,
    headers = {},
    signal,
    timeoutMs = 60000, // 60s timeout for AI operations
    profileVersion,
    skipGlobalErrorToast = false,
  } = options;

  const isMutation = method !== 'GET';
  const mutationKey = isMutation ? `${method}:${url}:${JSON.stringify(body || {})}` : null;

  if (mutationKey && inFlightMutations.has(mutationKey)) {
    throw new ApiError(
      'RATE_LIMITED',
      'Request already in flight. Preventing duplicate submit.',
      {},
      `req-dup-${Date.now()}`,
      429
    );
  }

  if (mutationKey) {
    inFlightMutations.add(mutationKey);
  }

  try {
    const isMock = import.meta.env.VITE_USE_MOCKS === 'true';

    // 1. Mock Mode Bypass
    if (isMock) {
      const result = await handleMockRequest<T>(url, method, body, profileVersion);
      // Sync meta with UiStore
      useUiStore.getState().setAiMode(result.meta.ai_mode);
      if (result.meta.profile_version) {
        useUiStore.getState().setProfileVersion(result.meta.profile_version);
      }
      return result;
    }

    // 2. Real Backend Call
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

    const onExternalAbort = () => controller.abort();
    if (signal) {
      signal.addEventListener('abort', onExternalAbort);
    }

    const token = useAuthStore.getState().token;
    const requestHeaders: Record<string, string> = {
      'Content-Type': 'application/json',
      ...headers,
    };

    if (token) {
      requestHeaders['Authorization'] = `Bearer ${token}`;
    }

    let response: Response;
    try {
      response = await fetch(url, {
        method,
        headers: requestHeaders,
        body: body ? JSON.stringify(body) : undefined,
        signal: controller.signal,
      });
    } catch (err: any) {
      if (err.name === 'AbortError') {
        throw new ApiError(
          'LLM_UNAVAILABLE',
          'The AI request timed out after 60 seconds.',
          {},
          `req-timeout-${Date.now()}`,
          503
        );
      }
      throw new ApiError(
        'LLM_UNAVAILABLE',
        'Network error or backend unreachable.',
        { original: String(err) },
        `req-net-${Date.now()}`,
        503
      );
    } finally {
      clearTimeout(timeoutId);
      if (signal) {
        signal.removeEventListener('abort', onExternalAbort);
      }
    }

    // Parse response
    const json = await response.json();

    if (!response.ok) {
      const errorEnvelope = json as ErrorEnvelope;
      const apiErr = ApiError.fromEnvelope(errorEnvelope, response.status);

      // Global error handling behaviors
      handleGlobalError(apiErr, skipGlobalErrorToast);
      throw apiErr;
    }

    const successEnvelope = json as SuccessEnvelope<T>;

    // Keep meta in sync with UiStore
    if (successEnvelope.meta) {
      useUiStore.getState().setAiMode(successEnvelope.meta.ai_mode);
      if (successEnvelope.meta.profile_version) {
        useUiStore.getState().setProfileVersion(successEnvelope.meta.profile_version);
      }
    }

    return successEnvelope;
  } finally {
    if (mutationKey) {
      inFlightMutations.delete(mutationKey);
    }
  }
}

function handleGlobalError(error: ApiError, skipToast: boolean): void {
  switch (error.status) {
    case 401:
      useAuthStore.getState().logout();
      if (!skipToast) toast.error('Session expired. Please log in again.');
      break;

    case 409:
      if (error.code === 'VERSION_CONFLICT') {
        if (!skipToast) {
          toast.warning('Your profile was updated in another session. Refreshed.', {
            description: 'Please retry your latest changes.',
          });
        }
      } else if (error.code === 'SESSION_CLOSED') {
        if (!skipToast) {
          toast.info('This investor session has concluded and is closed.');
        }
      }
      break;

    case 429:
      if (!skipToast) {
        toast.error('Too many requests. Please wait a moment before trying again.');
      }
      break;

    case 502:
      // LLM_INVALID_OUTPUT
      if (!skipToast) {
        toast.error('AI Output Error: The model produced an invalid response.', {
          description: `Request ID: ${error.request_id}`,
        });
      }
      break;

    case 503:
      // LLM_UNAVAILABLE
      if (!skipToast) {
        toast.error('AI Service Unavailable. Fallback provider might be offline.', {
          description: `Request ID: ${error.request_id}`,
        });
      }
      break;

    case 422:
      // Validation error mapped to details
      if (!skipToast) {
        toast.error('Validation Error: Please check the highlighted inputs.');
      }
      break;

    default:
      if (!skipToast) {
        toast.error(error.message || 'An unexpected error occurred.');
      }
  }
}
