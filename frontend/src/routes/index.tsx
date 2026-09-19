import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { AppLayout } from '../components/layout/AppLayout';
import { LoginPage } from '../features/auth/LoginPage';
import { RegisterPage } from '../features/auth/RegisterPage';
import { StartupListPage } from '../features/auth/StartupListPage';
import { OverviewProfilePage } from '../features/profile/OverviewProfilePage';
import { ValuePropPage } from '../features/value-prop/ValuePropPage';
import { MarketPage } from '../features/market/MarketPage';
import { BusinessModelPage } from '../features/business-model/BusinessModelPage';
import { PitchDeckPage } from '../features/pitch/PitchDeckPage';
import { FeedbackPage } from '../features/feedback/FeedbackPage';
import { InvestorPracticePage } from '../features/investor/InvestorPracticePage';
import { ReadinessReportPage } from '../features/report/ReadinessReportPage';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const isMock = import.meta.env.VITE_USE_MOCKS === 'true';
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  // Auto-allow in mock mode
  if (isMock) {
    return <>{children}</>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

export const AppRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route
        path="/startups"
        element={
          <ProtectedRoute>
            <StartupListPage />
          </ProtectedRoute>
        }
      />

      <Route
        path="/"
        element={
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<OverviewProfilePage />} />
        <Route path="value-prop" element={<ValuePropPage />} />
        <Route path="market" element={<MarketPage />} />
        <Route path="business-model" element={<BusinessModelPage />} />
        <Route path="pitch-deck" element={<PitchDeckPage />} />
        <Route path="feedback" element={<FeedbackPage />} />
        <Route path="investor-practice" element={<InvestorPracticePage />} />
        <Route path="readiness-report" element={<ReadinessReportPage />} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};
