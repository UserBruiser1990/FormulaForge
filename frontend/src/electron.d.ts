export {};

declare global {
  interface ImportMetaEnv {
    readonly VITE_API_URL?: string;
  }

  interface ImportMeta {
    readonly env: ImportMetaEnv;
  }

  interface Window {
    formulaForge?: {
      checkForUpdates: () => Promise<UpdateStatus>;
      downloadUpdate: () => Promise<UpdateStatus>;
      installUpdate: () => Promise<void>;
      onUpdateStatus: (callback: (status: UpdateStatus) => void) => () => void;
    };
  }
}

type UpdateStatus = {
  state: "available" | "checking" | "current" | "downloading" | "downloaded" | "unavailable" | "error";
  version?: string;
  percent?: number;
  message?: string;
};
