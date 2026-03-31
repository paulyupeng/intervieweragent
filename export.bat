@echo off
REM Export project to a zip file (Windows)

echo 📦 Packing Interviewer Agent for export...

REM Create exports directory
if not exist exports mkdir exports

REM Create zip file using PowerShell
powershell -Command "Compress-Archive -Path '.\backend', '.\frontend', '.\question_banks', '.\database', '.env.example', 'docker-compose.yml', 'docker-compose.yml.example', 'README.md', 'QUICKSTART.md', '.gitignore' -DestinationPath '.\exports\interviewer-agent-export.zip' -Force"

echo.
echo ✅ Export complete!
echo 📁 File location: exports\interviewer-agent-export.zip
echo.
echo To import on another computer:
echo 1. Copy the zip file to the target computer
echo 2. Extract to a folder
echo 3. Copy your .env file (with API keys) to the extracted folder
echo 4. Run docker-compose up -d

pause
