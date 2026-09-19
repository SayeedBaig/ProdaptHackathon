import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import { Button } from '../../components/ui/Button';
import { Card, CardContent } from '../../components/ui/Card';
import { Rocket, Sparkles } from 'lucide-react';
import { toast } from 'sonner';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const setAuth = useAuthStore((state) => state.setAuth);
  const [email, setEmail] = useState('founder@hyperscale.ai');
  const [password, setPassword] = useState('demo1234');
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    setTimeout(() => {
      setAuth('mock-token-demo', {
        id: '00000000-0000-0000-0000-000000000001',
        email,
        name: 'Alex Vance',
      });
      toast.success('Welcome back to PitchPilot!');
      navigate('/');
    }, 600);
  };

  const handleDemoBypass = () => {
    setAuth('mock-token-demo', {
      id: '00000000-0000-0000-0000-000000000001',
      email: 'founder@hyperscale.ai',
      name: 'Alex Vance',
    });
    toast.success('Logged in as Demo Founder');
    navigate('/');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 p-4">
      <Card className="w-full max-w-md shadow-xl border-slate-200">
        <CardContent className="p-8">
          <div className="text-center mb-8">
            <div className="inline-flex p-3 rounded-2xl bg-gradient-to-tr from-brand-700 to-indigo-500 text-white mb-3 shadow-md">
              <Rocket className="w-8 h-8" />
            </div>
            <h1 className="text-2xl font-bold text-slate-900 tracking-tight">
              Sign in to PitchPilot
            </h1>
            <p className="text-sm text-slate-500 mt-1">
              Your AI startup pitch coach & diligence simulator
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Email address
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full px-3.5 py-2 text-base border border-slate-300 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full px-3.5 py-2 text-base border border-slate-300 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none"
              />
            </div>

            <Button
              type="submit"
              variant="primary"
              className="w-full"
              isLoading={loading}
            >
              Sign in
            </Button>
          </form>

          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-slate-200" />
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-white px-2 text-slate-400 font-semibold">
                Or demo instantly
              </span>
            </div>
          </div>

          <Button
            type="button"
            variant="outline"
            onClick={handleDemoBypass}
            leftIcon={<Sparkles className="w-4 h-4 text-brand-600" />}
            className="w-full border-brand-200 bg-brand-50/60 text-brand-800 hover:bg-brand-100/70 font-semibold"
          >
            Auto-Login Demo Founder
          </Button>

          <div className="mt-6 text-center text-xs text-slate-500">
            Don&apos;t have an account?{' '}
            <Link to="/register" className="text-brand-600 font-medium hover:underline">
              Create an account
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
