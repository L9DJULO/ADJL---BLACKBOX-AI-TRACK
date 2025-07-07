import * as vscode from 'vscode';
import * as fs from 'fs';

export function activate(context: vscode.ExtensionContext) {
    
    // Commande Hello World qui ouvre le React 
    const helloWorldCommand = vscode.commands.registerCommand('adj.helloWorld', () => {
        const panel = vscode.window.createWebviewPanel(
            'myWebview',
            'My React Panel',
            vscode.ViewColumn.One,
            {
                enableScripts: true,
                localResourceRoots: [vscode.Uri.joinPath(context.extensionUri, 'media')],
            }
        );

        const scriptPath = vscode.Uri.joinPath(context.extensionUri, 'media', 'index.html');
        const html = fs.readFileSync(scriptPath.fsPath, 'utf8');

        panel.webview.html = html;

        panel.webview.onDidReceiveMessage(async msg => {
            vscode.window.showInformationMessage(JSON.stringify(msg));
        });
    });

    context.subscriptions.push(helloWorldCommand);
}
