#!/usr/bin/env pwsh
# Backpropagation Museum Project Setup Script
# PowerShell script for Windows environment setup

Write-Host "🚀 Setting up Backpropagation Museum Environment..." -ForegroundColor Green

# Check if Python is installed
try {
    $pythonVersion = python --version 2>$null
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+ first." -ForegroundColor Red
    exit 1
}

# Check if pip is available
try {
    pip --version | Out-Null
    Write-Host "✓ pip is available" -ForegroundColor Green
} catch {
    Write-Host "❌ pip not found. Please ensure pip is installed." -ForegroundColor Red
    exit 1
}

Write-Host "`n📦 Installing Python dependencies..." -ForegroundColor Yellow

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
if ($IsWindows -or $env:OS -eq "Windows_NT") {
    & ".\venv\Scripts\Activate.ps1"
} else {
    & ".\venv\bin\Activate.ps1"
}

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install requirements
Write-Host "Installing requirements..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "`n🔧 Setting up configuration..." -ForegroundColor Yellow

# Copy config template if it doesn't exist
if (-not (Test-Path ".env")) {
    if (Test-Path "config.env") {
        Copy-Item "config.env" ".env"
        Write-Host "✓ Configuration template copied to .env" -ForegroundColor Green
        Write-Host "⚠️  Please edit .env with your API keys" -ForegroundColor Yellow
    }
}

Write-Host "`n🧠 Creating Backpropagation implementation directories..." -ForegroundColor Yellow

# Create project directories
$directories = @("src", "notebooks", "tests", "docs", "examples")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
        Write-Host "✓ Created directory: $dir" -ForegroundColor Green
    }
}

Write-Host "`n🔍 Checking LaTeX files..." -ForegroundColor Yellow

# Check for existing LaTeX files
$latexFiles = @("BP.tex", "BP_review.md")
foreach ($file in $latexFiles) {
    if (Test-Path $file) {
        Write-Host "✓ Found: $file" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Missing: $file" -ForegroundColor Yellow
    }
}

Write-Host "`n🌐 Testing internet connectivity..." -ForegroundColor Yellow

# Test internet access
try {
    $response = Invoke-WebRequest -Uri "https://httpbin.org/get" -TimeoutSec 10 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ Internet access confirmed" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  Internet access test failed" -ForegroundColor Yellow
}

Write-Host "`n🚀 Starting MCP Server..." -ForegroundColor Yellow

# Check if MCP server can start
try {
    Write-Host "Testing MCP server startup..." -ForegroundColor Yellow
    
    # Start server in background and test
    $serverJob = Start-Job -ScriptBlock {
        cd $using:PWD
        & ".\venv\Scripts\python.exe" mcp_server.py
    }
    
    # Wait a moment for server to start
    Start-Sleep 3
    
    # Test health endpoint
    try {
        $healthCheck = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5 -UseBasicParsing
        if ($healthCheck.StatusCode -eq 200) {
            Write-Host "✓ MCP Server is running successfully" -ForegroundColor Green
            
            # Test capabilities endpoint
            $capabilities = Invoke-WebRequest -Uri "http://localhost:8000/capabilities" -TimeoutSec 5 -UseBasicParsing
            $capData = $capabilities.Content | ConvertFrom-Json
            Write-Host "✓ Server capabilities loaded" -ForegroundColor Green
            Write-Host "  - Internet Access: $($capData.internet_access)" -ForegroundColor Cyan
            Write-Host "  - Backprop Tools: $($capData.backpropagation_tools)" -ForegroundColor Cyan
            Write-Host "  - LaTeX Processing: $($capData.latex_processing)" -ForegroundColor Cyan
        }
    } catch {
        Write-Host "⚠️  MCP Server health check failed" -ForegroundColor Yellow
    }
    
    # Stop the test server
    Stop-Job $serverJob
    Remove-Job $serverJob
    
} catch {
    Write-Host "⚠️  MCP Server test failed: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host "`n📚 Setting up Jupyter environment..." -ForegroundColor Yellow

# Create Jupyter kernel for the project
try {
    python -m ipykernel install --user --name backprop --display-name "Backpropagation Museum"
    Write-Host "✓ Jupyter kernel installed" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Jupyter kernel installation failed" -ForegroundColor Yellow
}

Write-Host "`n✨ Setup Complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Edit .env file with your API keys" -ForegroundColor White
Write-Host "2. Run 'python mcp_server.py' to start the MCP server" -ForegroundColor White
Write-Host "3. Run 'jupyter lab' to start Jupyter for development" -ForegroundColor White
Write-Host "4. Open the Backpropagation notebook to begin implementation" -ForegroundColor White

Write-Host "`n🔗 Available endpoints once server is running:" -ForegroundColor Cyan
Write-Host "  - Health: http://localhost:8000/health" -ForegroundColor White
Write-Host "  - Capabilities: http://localhost:8000/capabilities" -ForegroundColor White
Write-Host "  - MCP Protocol: http://localhost:8000/mcp" -ForegroundColor White

Write-Host "`n🎯 Ready to build the Backpropagation Museum! 🧠✨" -ForegroundColor Magenta 