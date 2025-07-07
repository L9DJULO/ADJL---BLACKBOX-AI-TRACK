import { useState, useRef} from 'react';
import { Mic, MicOff, Code, Bug, TestTube, FileText, Zap, Settings, Upload, Download, RefreshCw, AlertTriangle, XCircle, Play } from 'lucide-react';

interface Suggestion {
  type: string;
  message: string;
  line: number;
}

interface BugReport {
  severity: string;
  message: string;
  line: number;
}

interface Panel {
  id: string;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
}

const AICodeVocalIDE = () => {
  const [isListening, setIsListening] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [code, setCode] = useState(`// Votre code ici - Powered by BLACKBOX.AI
function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

console.log(fibonacci(10));

// Commandez vocalement : "Analyser le code"
// ou "Optimiser cette fonction"
// ou "Générer des tests"`);
  
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const [bugs, setBugs] = useState<BugReport[]>([]);
  const [tests, setTests] = useState<string[]>([]);
  const [documentation, setDocumentation] = useState('');
  const [voiceCommand, setVoiceCommand] = useState('');
  const [activePanel, setActivePanel] = useState('suggestions');
  const [aiStatus, setAiStatus] = useState('idle');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Simulation des fonctionnalités AI avec BLACKBOX.AI
  const simulateAIAnalysis = () => {
    setIsProcessing(true);
    setAiStatus('analyzing');
    
    setTimeout(() => {
      setSuggestions([
        { type: 'performance', message: 'BLACKBOX.AI suggère: Utiliser la mémoisation pour optimiser fibonacci', line: 2 },
        { type: 'style', message: 'Llama 3.1 recommande: Utiliser const au lieu de function', line: 1 },
        { type: 'best-practice', message: 'Groq détecte: Ajouter une validation pour les nombres négatifs', line: 2 },
        { type: 'coral', message: 'Coral Protocol: Cette fonction peut être distribuée sur plusieurs agents', line: 3 },
        { type: 'fetch', message: 'Fetch.AI: Optimisation possible pour calculs décentralisés', line: 1 }
      ]);
      
      setBugs([
        { severity: 'error', message: 'Risque de stack overflow pour grandes valeurs', line: 3 },
        { severity: 'warning', message: 'Variable n non validée - peut causer des erreurs', line: 2 },
        { severity: 'info', message: 'Performance dégradée sans mémoisation', line: 1 }
      ]);
      
      setTests([
        'test("fibonacci(0) should return 0", () => { expect(fibonacci(0)).toBe(0); });',
        'test("fibonacci(1) should return 1", () => { expect(fibonacci(1)).toBe(1); });',
        'test("fibonacci(5) should return 5", () => { expect(fibonacci(5)).toBe(5); });',
        'test("fibonacci(10) should return 55", () => { expect(fibonacci(10)).toBe(55); });',
        'test("fibonacci(-1) should handle negative input", () => { expect(() => fibonacci(-1)).toThrow(); });'
      ]);
      
      setDocumentation(`/**
 * Calcule le nombre de Fibonacci - Optimisé par BLACKBOX.AI
 * @param {number} n - L'index du nombre de Fibonacci à calculer
 * @returns {number} Le nombre de Fibonacci correspondant
 * @throws {Error} Si n est négatif
 * @example
 * fibonacci(5) // returns 5
 * fibonacci(10) // returns 55
 * @complexity O(2^n) - Peut être optimisé avec mémoisation
 * @ai-suggestions Utiliser Map pour cache, validation d'entrée
 */`);
      
      setIsProcessing(false);
      setAiStatus('completed');
    }, 2500);
  };

  const toggleListening = () => {
    setIsListening(!isListening);
    if (!isListening) {
      setVoiceCommand('🎤 Écoute en cours... Dites votre commande');
      // Simulation commande vocale
      setTimeout(() => {
        const commands = [
          'Analyser le code et suggérer des améliorations',
          'Optimiser cette fonction fibonacci',
          'Générer des tests unitaires',
          'Créer la documentation',
          'Détecter les bugs potentiels'
        ];
        const randomCommand = commands[Math.floor(Math.random() * commands.length)];
        setVoiceCommand(`✅ Commande détectée: "${randomCommand}"`);
        setIsListening(false);
        setTimeout(() => {
          simulateAIAnalysis();
        }, 1000);
      }, 3000);
    } else {
      setVoiceCommand('');
    }
  };

  const StatusBadge = ({ status }: { status: string }) => {
    const statusConfig: Record<string, { color: string; text: string; pulse?: boolean }> = {
      idle: { color: 'status-idle', text: '🤖 Prêt' },
      analyzing: { color: 'status-analyzing', text: '🔄 Analyse IA...', pulse: true },
      completed: { color: 'status-completed', text: '✅ Terminé' }
    };
    
    const config = statusConfig[status];
    return (
      <div className={`status-badge ${config.color} ${config.pulse ? 'pulse-animation' : ''}`}>
        {config.text}
      </div>
    );
  };

  const panels: Panel[] = [
    { id: 'suggestions', label: 'Suggestions IA', icon: Zap },
    { id: 'bugs', label: 'Détection Bugs', icon: Bug },
    { id: 'tests', label: 'Tests Auto', icon: TestTube },
    { id: 'docs', label: 'Documentation', icon: FileText },
    { id: 'code', label: 'Code', icon: Code }
  ];

  return (
    <div className="aiv-container">
      {/* Header avec effet glassmorphism */}
      <header className="aiv-header">
        <div className="header-content">
          <div className="header-left">
            <div className="logo-container">
              <div className="logo-icon">
                <Code className="icon" />
              </div>
              <div>
                <h1 className="app-title">AI Code Vocal IDE</h1>
                <p className="app-subtitle">Hackathon BLACKBOX.AI Track</p>
              </div>
            </div>
            
            <div className="ai-providers">
              <div className="ai-provider">
                <div className="provider-indicator provider-indicator-blue"></div>
                <span className="provider-name">BLACKBOX.AI</span>
              </div>
              <div className="ai-provider">
                <div className="provider-indicator provider-indicator-green"></div>
                <span className="provider-name">Llama 3.1</span>
              </div>
              <div className="ai-provider">
                <div className="provider-indicator provider-indicator-orange"></div>
                <span className="provider-name">Groq</span>
              </div>
            </div>
          </div>
          
          <div className="header-right">
            <StatusBadge status={aiStatus} />
            <button className="icon-button">
              <Settings className="icon" />
            </button>
          </div>
        </div>
      </header>

      {/* Barre de commande vocale améliorée */}
      <div className="voice-command-bar">
        <div className="voice-command-content">
          <div className="voice-command-left">
            <button
              onClick={toggleListening}
              className={`voice-command-button ${isListening ? 'listening' : ''}`}
            >
              {isListening ? <MicOff className="icon" /> : <Mic className="icon" />}
              <span>
                {isListening ? 'Arrêter l\'écoute' : 'Commande vocale'}
              </span>
              {isListening && (
                <div className="audio-level-indicator">
                  <div className="audio-bar"></div>
                  <div className="audio-bar"></div>
                  <div className="audio-bar"></div>
                </div>
              )}
            </button>
            
            {voiceCommand && (
              <div className="voice-command-status">
                <div className="voice-command-indicator"></div>
                <span>{voiceCommand}</span>
              </div>
            )}
          </div>
          
          <div className="voice-command-right">
            <button
              onClick={simulateAIAnalysis}
              disabled={isProcessing}
              className={`analyze-button ${isProcessing ? 'processing' : ''}`}
            >
              {isProcessing ? <RefreshCw className="icon spin" /> : <Zap className="icon" />}
              <span>Analyser avec IA</span>
            </button>
          </div>
        </div>
      </div>

      {/* Contenu principal */}
      <div className="main-content">
        <div className="content-grid">
          
          {/* Éditeur de code */}
          <div className="editor-container">
            <div className="editor-card">
              <div className="editor-header">
                <h2>Éditeur de Code</h2>
                <div className="editor-actions">
                  <button className="icon-button">
                    <Upload className="icon" />
                  </button>
                  <button className="icon-button">
                    <Download className="icon" />
                  </button>
                  <button className="icon-button run-button">
                    <Play className="icon" />
                  </button>
                </div>
              </div>
              
              <div className="editor-body">
                <div className="code-editor-wrapper">
                  <textarea
                    ref={textareaRef}
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    className="code-editor"
                    placeholder="Tapez votre code ici ou utilisez une commande vocale..."
                  />
                  <div className="line-counter">
                    Lignes: {code.split('\n').length}
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Panneaux IA */}
          <div className="panels-container">
            {/* Navigation des panneaux */}
            <div className="panel-nav">
              {panels.map((panel) => (
                <button
                  key={panel.id}
                  onClick={() => setActivePanel(panel.id)}
                  className={`panel-nav-button ${activePanel === panel.id ? 'active' : ''}`}
                >
                  <panel.icon className="icon" />
                  <span>{panel.label}</span>
                </button>
              ))}
            </div>

            {/* Contenu du panneau actif */}
            <div className="panel-content-card">
              <div className="panel-header">
                <h3>
                  {panels.find(p => p.id === activePanel)?.label}
                </h3>
              </div>
              
              <div className="panel-body">
                {activePanel === 'suggestions' && (
                  <div className="suggestions-container">
                    {suggestions.length > 0 ? suggestions.map((suggestion, index) => (
                      <div key={index} className="suggestion-card">
                        <div className="suggestion-content">
                          <Zap className="icon suggestion-icon" />
                          <div>
                            <p className="suggestion-message">{suggestion.message}</p>
                            <span className="suggestion-line">
                              Ligne {suggestion.line}
                            </span>
                          </div>
                        </div>
                      </div>
                    )) : (
                      <div className="empty-panel">
                        <Zap className="empty-icon" />
                        <p className="empty-title">Aucune suggestion disponible.</p>
                        <p className="empty-subtitle">Lancez une analyse IA pour obtenir des suggestions.</p>
                      </div>
                    )}
                  </div>
                )}

                {activePanel === 'bugs' && (
                  <div className="bugs-container">
                    {bugs.length > 0 ? bugs.map((bug, index) => (
                      <div key={index} className={`bug-card bug-${bug.severity}`}>
                        <div className="bug-content">
                          {bug.severity === 'error' ? 
                            <XCircle className="icon bug-icon" /> :
                            bug.severity === 'warning' ?
                            <AlertTriangle className="icon bug-icon" /> :
                            <XCircle className="icon bug-icon" />
                          }
                          <div>
                            <p className="bug-message">{bug.message}</p>
                            <span className={`bug-severity bug-${bug.severity}`}>
                              {bug.severity.toUpperCase()} - Ligne {bug.line}
                            </span>
                          </div>
                        </div>
                      </div>
                    )) : (
                      <div className="empty-panel">
                        <Bug className="empty-icon" />
                        <p className="empty-title">Aucun bug détecté.</p>
                        <p className="empty-subtitle">Votre code semble propre !</p>
                      </div>
                    )}
                  </div>
                )}

                {activePanel === 'tests' && (
                  <div className="tests-container">
                    {tests.length > 0 ? tests.map((test, index) => (
                      <div key={index} className="test-card">
                        <div className="test-content">
                          <TestTube className="icon test-icon" />
                          <div className="test-details">
                            <code className="test-code">{test}</code>
                            <button className="test-run-button">
                              Exécuter
                            </button>
                          </div>
                        </div>
                      </div>
                    )) : (
                      <div className="empty-panel">
                        <TestTube className="empty-icon" />
                        <p className="empty-title">Aucun test généré.</p>
                        <p className="empty-subtitle">Lancez une analyse pour créer des tests.</p>
                      </div>
                    )}
                  </div>
                )}

                {activePanel === 'docs' && (
                  <div>
                    {documentation ? (
                      <div className="doc-card">
                        <div className="doc-content">
                          <FileText className="icon doc-icon" />
                          <div className="doc-details">
                            <pre className="doc-text">{documentation}</pre>
                            <button className="doc-copy-button">
                              Copier
                            </button>
                          </div>
                        </div>
                      </div>
                    ) : (
                      <div className="empty-panel">
                        <FileText className="empty-icon" />
                        <p className="empty-title">Aucune documentation générée.</p>
                        <p className="empty-subtitle">Analysez votre code pour créer la documentation.</p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer amélioré */}
      <footer className="aiv-footer">
        <div className="footer-content">
          <div className="footer-left">
            <span>© 2025 AI Code Vocal IDE</span>
            <span className="footer-divider">•</span>
            <span className="footer-highlight">Hackathon BLACKBOX.AI</span>
          </div>
          <div className="footer-right">
            <span>Intégré avec</span>
            <div className="integrations">
              <span className="integration-groq">Groq</span>
              <span className="integration-coral">Coral Protocol</span>
              <span className="integration-fetch">Fetch.AI</span>
            </div>
          </div>
        </div>
      </footer>

      <style>{`
        /* Variables de couleurs */
        :root {
          --primary-gradient: linear-gradient(135deg, #6e45e2, #88d3ce);
          --secondary-gradient: linear-gradient(135deg, #7e5bff, #ff7eb3);
          --dark-bg: #0f0f1b;
          --darker-bg: #0a0a12;
          --card-bg: rgba(25, 25, 45, 0.7);
          --card-border: rgba(255, 255, 255, 0.1);
          --text-primary: #ffffff;
          --text-secondary: #a0a0c0;
          --success: #4caf50;
          --warning: #ff9800;
          --error: #f44336;
          --info: #2196f3;
          --accent-purple: #9c27b0;
          --accent-blue: #03a9f4;
          --accent-pink: #e91e63;
          --glass-effect: rgba(30, 30, 50, 0.5);
          --glass-border: rgba(255, 255, 255, 0.1);
        }
        
        /* Styles globaux */
        .aiv-container * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .aiv-container {
          min-height: 100vh;
          display: flex;
          flex-direction: column;
          background: var(--dark-bg);
          background-image: 
            radial-gradient(circle at 10% 20%, rgba(110, 69, 226, 0.1) 0%, transparent 20%),
            radial-gradient(circle at 90% 80%, rgba(136, 211, 206, 0.1) 0%, transparent 20%);
        }
        
        .icon {
          width: 20px;
          height: 20px;
        }
        
        .spin {
          animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        
        /* Header */
        .aiv-header {
          background: var(--glass-effect);
          backdrop-filter: blur(12px);
          border-bottom: 1px solid var(--glass-border);
          padding: 1rem 0;
        }
        
        .header-content {
          max-width: 1200px;
          margin: 0 auto;
          padding: 0 1.5rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        
        .header-left {
          display: flex;
          align-items: center;
          gap: 2rem;
        }
        
        .logo-container {
          display: flex;
          align-items: center;
          gap: 0.75rem;
        }
        
        .logo-icon {
          width: 40px;
          height: 40px;
          border-radius: 12px;
          background: var(--secondary-gradient);
          display: flex;
          align-items: center;
          justify-content: center;
          box-shadow: 0 4px 15px rgba(156, 39, 176, 0.3);
        }
        
        .app-title {
          font-size: 1.5rem;
          font-weight: 700;
          background: var(--secondary-gradient);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }
        
        .app-subtitle {
          font-size: 0.85rem;
          color: var(--text-secondary);
        }
        
        .ai-providers {
          display: flex;
          gap: 1rem;
        }
        
        .ai-provider {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          background: rgba(0, 0, 0, 0.2);
          padding: 0.25rem 0.75rem;
          border-radius: 20px;
          font-size: 0.85rem;
        }
        
        .provider-indicator {
          width: 8px;
          height: 8px;
          border-radius: 50%;
        }
        
        .provider-indicator-blue {
          background: var(--accent-blue);
        }
        
        .provider-indicator-green {
          background: var(--success);
        }
        
        .provider-indicator-orange {
          background: var(--warning);
        }
        
        .provider-name {
          color: var(--text-secondary);
        }
        
        .header-right {
          display: flex;
          align-items: center;
          gap: 1rem;
        }
        
        .status-badge {
          padding: 0.5rem 1rem;
          border-radius: 20px;
          font-size: 0.9rem;
          font-weight: 500;
        }
        
        .status-idle {
          background: rgba(255, 255, 255, 0.1);
          color: var(--text-secondary);
        }
        
        .status-analyzing {
          background: rgba(33, 150, 243, 0.2);
          color: var(--accent-blue);
        }
        
        .status-completed {
          background: rgba(76, 175, 80, 0.2);
          color: var(--success);
        }
        
        .pulse-animation {
          animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
          0% { opacity: 1; }
          50% { opacity: 0.7; }
          100% { opacity: 1; }
        }
        
        .icon-button {
          width: 40px;
          height: 40px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: rgba(255, 255, 255, 0.1);
          border-radius: 10px;
          border: none;
          color: var(--text-primary);
          cursor: pointer;
          transition: all 0.3s ease;
        }
        
        .icon-button:hover {
          background: rgba(255, 255, 255, 0.2);
        }
        
        /* Barre de commande vocale */
        .voice-command-bar {
          background: rgba(0, 0, 0, 0.2);
          backdrop-filter: blur(12px);
          border-bottom: 1px solid var(--glass-border);
          padding: 1rem 0;
        }
        
        .voice-command-content {
          max-width: 1200px;
          margin: 0 auto;
          padding: 0 1.5rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        
        .voice-command-left {
          display: flex;
          align-items: center;
          gap: 1.5rem;
        }
        
        .voice-command-button {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          padding: 0.75rem 1.5rem;
          border-radius: 12px;
          font-weight: 500;
          border: none;
          color: white;
          cursor: pointer;
          transition: all 0.3s ease;
          background: var(--primary-gradient);
          box-shadow: 0 4px 20px rgba(110, 69, 226, 0.4);
        }
        
        .voice-command-button:hover {
          transform: translateY(-2px);
          box-shadow: 0 6px 25px rgba(110, 69, 226, 0.5);
        }
        
        .voice-command-button.listening {
          background: linear-gradient(to right, #ff416c, #ff4b2b);
          animation: pulse 1.5s infinite;
        }
        
        .audio-level-indicator {
          display: flex;
          align-items: center;
          gap: 4px;
          height: 24px;
        }
        
        .audio-bar {
          width: 3px;
          background: white;
          border-radius: 2px;
          animation: audioPulse 0.4s alternate infinite;
        }
        
        .audio-bar:nth-child(1) { height: 40%; animation-delay: 0s; }
        .audio-bar:nth-child(2) { height: 60%; animation-delay: 0.2s; }
        .audio-bar:nth-child(3) { height: 30%; animation-delay: 0.1s; }
        
        @keyframes audioPulse {
          from { height: 30%; }
          to { height: 90%; }
        }
        
        .voice-command-status {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          background: rgba(0, 0, 0, 0.3);
          padding: 0.5rem 1rem;
          border-radius: 8px;
          font-size: 0.9rem;
        }
        
        .voice-command-indicator {
          width: 10px;
          height: 10px;
          border-radius: 50%;
          background: var(--accent-purple);
          animation: pulse 1.5s infinite;
        }
        
        .voice-command-right {
          display: flex;
          gap: 1rem;
        }
        
        .analyze-button {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          padding: 0.75rem 1.5rem;
          border-radius: 12px;
          font-weight: 500;
          border: none;
          color: white;
          cursor: pointer;
          transition: all 0.3s ease;
          background: var(--secondary-gradient);
          box-shadow: 0 4px 20px rgba(156, 39, 176, 0.4);
        }
        
        .analyze-button:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 6px 25px rgba(156, 39, 176, 0.5);
        }
        
        .analyze-button:disabled {
          opacity: 0.7;
          cursor: not-allowed;
        }
        
        .analyze-button.processing {
          background: linear-gradient(to right, #2196f3, #21cbf3);
        }
        
        /* Contenu principal */
        .main-content {
          flex: 1;
          max-width: 1200px;
          margin: 0 auto;
          width: 100%;
          padding: 2rem 1.5rem;
        }
        
        .content-grid {
          display: grid;
          grid-template-columns: 1fr;
          gap: 2rem;
        }
        
        @media (min-width: 1024px) {
          .content-grid {
            grid-template-columns: 3fr 2fr;
          }
        }
        
        .editor-container, .panels-container {
          width: 100%;
        }
        
        .editor-card, .panel-content-card {
          background: var(--card-bg);
          backdrop-filter: blur(12px);
          border-radius: 16px;
          border: 1px solid var(--card-border);
          overflow: hidden;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }
        
        .editor-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 1rem 1.5rem;
          background: rgba(0, 0, 0, 0.2);
          border-bottom: 1px solid var(--card-border);
        }
        
        .editor-header h2 {
          font-size: 1.25rem;
          font-weight: 600;
        }
        
        .editor-actions {
          display: flex;
          gap: 0.75rem;
        }
        
        .run-button {
          background: rgba(76, 175, 80, 0.2);
          color: var(--success);
        }
        
        .editor-body {
          padding: 1.5rem;
        }
        
        .code-editor-wrapper {
          position: relative;
        }
        
        .code-editor {
          width: 100%;
          height: 400px;
          background: rgba(10, 10, 20, 0.7);
          color: #4af626; /* Couleur terminal vert */
          font-family: 'Fira Code', 'Consolas', monospace;
          font-size: 0.95rem;
          line-height: 1.5;
          padding: 1.5rem;
          border-radius: 12px;
          border: 1px solid rgba(74, 246, 38, 0.2);
          resize: none;
          outline: none;
          tab-size: 2;
        }
        
        .code-editor:focus {
          border-color: rgba(74, 246, 38, 0.4);
          box-shadow: 0 0 0 2px rgba(74, 246, 38, 0.1);
        }
        
        .line-counter {
          position: absolute;
          top: 1rem;
          right: 1rem;
          font-size: 0.8rem;
          color: var(--text-secondary);
          background: rgba(0, 0, 0, 0.3);
          padding: 0.25rem 0.5rem;
          border-radius: 4px;
        }
        
        /* Panneaux IA */
        .panel-nav {
          display: flex;
          flex-wrap: wrap;
          gap: 0.75rem;
          margin-bottom: 1.5rem;
        }
        
        .panel-nav-button {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.75rem 1.25rem;
          border-radius: 12px;
          font-size: 0.9rem;
          font-weight: 500;
          border: none;
          background: rgba(255, 255, 255, 0.1);
          color: var(--text-secondary);
          cursor: pointer;
          transition: all 0.3s ease;
        }
        
        .panel-nav-button:hover {
          background: rgba(255, 255, 255, 0.15);
        }
        
        .panel-nav-button.active {
          background: var(--secondary-gradient);
          color: white;
          box-shadow: 0 4px 15px rgba(156, 39, 176, 0.3);
        }
        
        .panel-header {
          padding: 1rem 1.5rem;
          background: rgba(0, 0, 0, 0.2);
          border-bottom: 1px solid var(--card-border);
        }
        
        .panel-header h3 {
          font-size: 1.1rem;
          font-weight: 600;
        }
        
        .panel-body {
          padding: 1.5rem;
          max-height: 400px;
          overflow-y: auto;
        }
        
        /* Cartes de contenu */
        .suggestion-card, .bug-card, .test-card, .doc-card {
          border-radius: 12px;
          padding: 1.25rem;
          margin-bottom: 1rem;
          transition: transform 0.3s ease;
        }
        
        .suggestion-card:hover, .bug-card:hover, .test-card:hover, .doc-card:hover {
          transform: translateY(-3px);
        }
        
        .suggestion-card {
          background: linear-gradient(135deg, rgba(33, 150, 243, 0.2), rgba(3, 169, 244, 0.2));
          border: 1px solid rgba(33, 150, 243, 0.3);
        }
        
        .bug-card {
          border: 1px solid;
        }
        
        .bug-error {
          background: linear-gradient(135deg, rgba(244, 67, 54, 0.2), rgba(229, 57, 53, 0.2));
          border-color: rgba(244, 67, 54, 0.3);
        }
        
        .bug-warning {
          background: linear-gradient(135deg, rgba(255, 152, 0, 0.2), rgba(245, 124, 0, 0.2));
          border-color: rgba(255, 152, 0, 0.3);
        }
        
        .bug-info {
          background: linear-gradient(135deg, rgba(33, 150, 243, 0.2), rgba(3, 169, 244, 0.2));
          border-color: rgba(33, 150, 243, 0.3);
        }
        
        .test-card {
          background: linear-gradient(135deg, rgba(76, 175, 80, 0.2), rgba(56, 142, 60, 0.2));
          border: 1px solid rgba(76, 175, 80, 0.3);
        }
        
        .doc-card {
          background: linear-gradient(135deg, rgba(156, 39, 176, 0.2), rgba(123, 31, 162, 0.2));
          border: 1px solid rgba(156, 39, 176, 0.3);
        }
        
        .suggestion-content, .bug-content, .test-content, .doc-content {
          display: flex;
          gap: 1rem;
        }
        
        .suggestion-icon, .bug-icon, .test-icon, .doc-icon {
          flex-shrink: 0;
        }
        
        .suggestion-icon {
          color: var(--accent-blue);
        }
        
        .bug-icon {
          color: var(--error);
        }
        
        .bug-warning .bug-icon {
          color: var(--warning);
        }
        
        .bug-info .bug-icon {
          color: var(--accent-blue);
        }
        
        .test-icon {
          color: var(--success);
        }
        
        .doc-icon {
          color: var(--accent-purple);
        }
        
        .suggestion-message, .bug-message {
          font-size: 0.95rem;
          margin-bottom: 0.5rem;
        }
        
        .suggestion-line {
          font-size: 0.8rem;
          background: rgba(33, 150, 243, 0.2);
          color: var(--accent-blue);
          padding: 0.25rem 0.75rem;
          border-radius: 20px;
          display: inline-block;
        }
        
        .bug-severity {
          font-size: 0.8rem;
          padding: 0.25rem 0.75rem;
          border-radius: 20px;
          display: inline-block;
        }
        
        .bug-error {
          background: rgba(244, 67, 54, 0.2);
          color: var(--error);
        }
        
        .bug-warning {
          background: rgba(255, 152, 0, 0.2);
          color: var(--warning);
        }
        
        .bug-info {
          background: rgba(33, 150, 243, 0.2);
          color: var(--accent-blue);
        }
        
        .test-details {
          flex: 1;
        }
        
        .test-code {
          display: block;
          font-family: 'Fira Code', 'Consolas', monospace;
          font-size: 0.85rem;
          background: rgba(0, 0, 0, 0.3);
          padding: 0.75rem;
          border-radius: 8px;
          margin-bottom: 0.75rem;
          white-space: pre-wrap;
          line-height: 1.4;
        }
        
        .test-run-button {
          font-size: 0.8rem;
          padding: 0.4rem 0.8rem;
          border-radius: 20px;
          background: rgba(76, 175, 80, 0.3);
          color: var(--success);
          border: none;
          cursor: pointer;
          transition: all 0.2s ease;
        }
        
        .test-run-button:hover {
          background: rgba(76, 175, 80, 0.4);
        }
        
        .doc-details {
          flex: 1;
        }
        
        .doc-text {
          font-family: 'Fira Code', 'Consolas', monospace;
          font-size: 0.9rem;
          background: rgba(0, 0, 0, 0.3);
          padding: 1rem;
          border-radius: 8px;
          margin-bottom: 1rem;
          white-space: pre-wrap;
          line-height: 1.5;
          color: var(--text-secondary);
        }
        
        .doc-copy-button {
          font-size: 0.8rem;
          padding: 0.4rem 0.8rem;
          border-radius: 20px;
          background: rgba(156, 39, 176, 0.3);
          color: var(--accent-purple);
          border: none;
          cursor: pointer;
          transition: all 0.2s ease;
        }
        
        .doc-copy-button:hover {
          background: rgba(156, 39, 176, 0.4);
        }
        
        /* Panneau vide */
        .empty-panel {
          text-align: center;
          padding: 2rem 0;
        }
        
        .empty-icon {
          width: 48px;
          height: 48px;
          margin: 0 auto 1rem;
          color: var(--text-secondary);
        }
        
        .empty-title {
          color: var(--text-secondary);
          margin-bottom: 0.5rem;
          font-size: 1.1rem;
        }
        
        .empty-subtitle {
          color: var(--text-secondary);
          font-size: 0.9rem;
          opacity: 0.8;
        }
        
        /* Footer */
        .aiv-footer {
          background: rgba(0, 0, 0, 0.3);
          backdrop-filter: blur(12px);
          border-top: 1px solid var(--glass-border);
          padding: 1.5rem 0;
          margin-top: auto;
        }
        
        .footer-content {
          max-width: 1200px;
          margin: 0 auto;
          padding: 0 1.5rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
          font-size: 0.9rem;
        }
        
        .footer-left {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          color: var(--text-secondary);
        }
        
        .footer-divider {
          color: var(--accent-purple);
        }
        
        .footer-highlight {
          color: var(--accent-purple);
          font-weight: 500;
        }
        
        .footer-right {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          color: var(--text-secondary);
        }
        
        .integrations {
          display: flex;
          gap: 0.75rem;
        }
        
        .integration-groq {
          color: var(--accent-blue);
        }
        
        .integration-coral {
          color: var(--success);
        }
        
        .integration-fetch {
          color: var(--warning);
        }
      `}</style>
    </div>
  );
};

export default AICodeVocalIDE;