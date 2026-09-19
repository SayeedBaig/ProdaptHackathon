import { create } from 'zustand';
import { AiMode } from '../types/contracts';

interface UiState {
  currentStartupId: string | null;
  activeSlideIndex: number;
  isDegradedBannerDismissed: boolean;
  sidebarOpen: boolean;
  aiMode: AiMode;
  profileVersion: number;
  setCurrentStartupId: (id: string | null) => void;
  setActiveSlideIndex: (index: number) => void;
  setDegradedBannerDismissed: (dismissed: boolean) => void;
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
  setAiMode: (mode: AiMode) => void;
  setProfileVersion: (version: number) => void;
}

const isMockMode = import.meta.env.VITE_USE_MOCKS === 'true';

export const useUiStore = create<UiState>((set) => ({
  currentStartupId: isMockMode ? 'hyperscale-ai-001' : null,
  activeSlideIndex: 0,
  isDegradedBannerDismissed: false,
  sidebarOpen: true,
  aiMode: (isMockMode ? 'mock' : 'live') as AiMode,
  profileVersion: 1,

  setCurrentStartupId: (id) => set({ currentStartupId: id }),
  setActiveSlideIndex: (index) => set({ activeSlideIndex: index }),
  setDegradedBannerDismissed: (dismissed) => set({ isDegradedBannerDismissed: dismissed }),
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
  setAiMode: (mode) => set({ aiMode: mode }),
  setProfileVersion: (version) => set({ profileVersion: version }),
}));
