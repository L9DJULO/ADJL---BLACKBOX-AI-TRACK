// src/hooks/useVsCodeApi.ts
import { useMemo } from 'react'

type VsCodeApi = {
    postMessage: (message: any) => void
    getState: () => any
    setState: (state: any) => void
}

declare global {
    interface Window {
        acquireVsCodeApi?: () => VsCodeApi
    }
}

export function useVsCodeApi(): VsCodeApi | undefined {
    return useMemo(() => {
        if (typeof window !== 'undefined' && window.acquireVsCodeApi) {
            return window.acquireVsCodeApi()
        }
        return undefined
    }, [])
}
