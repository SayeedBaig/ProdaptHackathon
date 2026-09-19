import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from './ui/Button';
import { AlertTriangle, ArrowLeft, Home } from 'lucide-react';

interface ErrorBoundaryState {
  error: Error | null;
}

export class ErrorBoundary extends React.Component<React.PropsWithChildren, ErrorBoundaryState> {
  state: ErrorBoundaryState = { error: null };

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { error };
  }

  componentDidCatch(error: Error): void {
    console.error('Route render failed:', error);
  }

  render() {
    if (!this.state.error) {
      return this.props.children;
    }

    return (
      <div className="min-h-[60vh] flex items-center justify-center p-6">
        <div className="w-full max-w-lg rounded-xl border border-amber-200 bg-white p-6 shadow-md">
          <div className="flex items-center gap-3 text-amber-800 mb-3">
            <div className="p-2 rounded-lg bg-amber-50">
              <AlertTriangle className="w-5 h-5" />
            </div>
            <h1 className="text-lg font-bold text-slate-900">This page hit a rendering error</h1>
          </div>
          <p className="text-sm text-slate-600 mb-4">
            The rest of the app is still available. You can go back, choose another startup, or retry after refreshing.
          </p>
          <pre className="max-h-28 overflow-auto rounded-lg bg-slate-50 p-3 text-xs text-slate-600 mb-4">
            {this.state.error.message}
          </pre>
          <div className="flex flex-wrap gap-2">
            <Button
              type="button"
              variant="outline"
              onClick={() => {
                this.setState({ error: null });
                window.history.back();
              }}
              leftIcon={<ArrowLeft className="w-4 h-4" />}
            >
              Go Back
            </Button>
            <Link to="/startups" onClick={() => this.setState({ error: null })}>
              <Button type="button" variant="primary" leftIcon={<Home className="w-4 h-4" />}>
                Startups
              </Button>
            </Link>
          </div>
        </div>
      </div>
    );
  }
}
