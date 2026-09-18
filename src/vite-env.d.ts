/// <reference types="vite/client" />

interface Window {
  geminiGenerateText: (promptText: string) => Promise<string>;
  geminiSearchText: (searchQuery: string) => Promise<string>;
  geminiImageCreation: (imagePrompt: string) => Promise<string>;
}