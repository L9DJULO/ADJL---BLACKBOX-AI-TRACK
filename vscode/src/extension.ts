import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import { create } from 'domain';

export function activate(context: vscode.ExtensionContext) {
    


    // Commande : Afficher panneau React (helloWorld)
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
    const fonctionGlobal = vscode.commands.registerCommand('adj.fonctionGLobal', () => {
        vscode.commands.executeCommand('adj.helloWorld');
       
    })

    // Enregistre les commandes dans les subscriptions
    context.subscriptions.push(helloWorldCommand, fonctionGlobal);
}

export function deactivate() {}
