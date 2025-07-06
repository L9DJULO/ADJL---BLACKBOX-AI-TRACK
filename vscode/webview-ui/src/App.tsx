import { useVsCodeApi } from './vscode/use-vscode-api.ts'

export default function App() {
    const vscode = useVsCodeApi()

    const sendMessage = () => {
        vscode?.postMessage({ type: 'hello', payload: 'from webview' })
    }

    return (
        <div>
            <h1>Hello from Vite + React</h1>
            <h1>{ vscode === undefined ? 'NOOON' : 'YESSS'}</h1>
            <button onClick={sendMessage}>Send Message to VS Code</button>
        </div>
    )
}
