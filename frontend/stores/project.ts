"use client";

import { create } from "zustand";

interface ProjectState {
  currentProject: any | null;
  setCurrentProject: (project: any) => void;
}

export const useProjectStore = create<ProjectState>((set) => ({
  currentProject: null,
  setCurrentProject: (project) => set({ currentProject: project }),
}));
