#!/usr/bin/env node

/**
 * Maya MCP Node.js wrapper
 * This script launches the Python MCP server
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Get project root directory
const projectRoot = path.resolve(__dirname, '..');

// Check if Python is available
function checkPython() {
    const pythonCommands = ['python3', 'python'];
    
    for (const cmd of pythonCommands) {
        try {
            const result = spawn(cmd, ['--version'], { stdio: 'pipe' });
            result.on('close', (code) => {
                if (code === 0) {
                    return cmd;
                }
            });
        } catch (e) {
            continue;
        }
    }
    
    console.error('Error: Python is not installed or not in PATH');
    console.error('Please install Python 3.10 or higher from https://www.python.org/');
    process.exit(1);
}

// Main function
function main() {
    console.log('Starting Maya MCP Server...');
    
    // Environment variables
    const env = {
        ...process.env,
        PYTHONPATH: path.join(projectRoot, 'src'),
        MAYA_HOST: process.env.MAYA_HOST || 'localhost',
        MAYA_PORT: process.env.MAYA_PORT || '9877'
    };
    
    // Check if src directory exists
    if (!fs.existsSync(path.join(projectRoot, 'src'))) {
        console.error('Error: src directory not found');
        console.error('Make sure you are running this from the maya-mcp-server directory');
        process.exit(1);
    }
    
    // Determine Python command
    const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';
    
    console.log(`Project root: ${projectRoot}`);
    console.log(`PYTHONPATH: ${env.PYTHONPATH}`);
    console.log(`Maya connection: ${env.MAYA_HOST}:${env.MAYA_PORT}`);
    console.log('');
    
    // Spawn Python process
    const pythonProcess = spawn(pythonCmd, ['-m', 'maya_mcp.server'], {
        env: env,
        stdio: 'inherit',
        cwd: projectRoot
    });
    
    // Handle process events
    pythonProcess.on('error', (error) => {
        console.error('Failed to start Maya MCP Server:', error.message);
        process.exit(1);
    });
    
    pythonProcess.on('close', (code) => {
        if (code !== 0) {
            console.error(`Maya MCP Server exited with code ${code}`);
            process.exit(code);
        }
    });
    
    // Handle termination signals
    process.on('SIGINT', () => {
        console.log('\nShutting down Maya MCP Server...');
        pythonProcess.kill('SIGINT');
        process.exit(0);
    });
    
    process.on('SIGTERM', () => {
        pythonProcess.kill('SIGTERM');
        process.exit(0);
    });
}

// Run
main();