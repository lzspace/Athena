#!/usr/bin/env bash
# Category: Environment Setup
# Description: Start Athena Assistant Environment
# Details:
# 1. Starts the Docker container for LLaMA.
# 2. Activates the Python virtual environment.
# 3. Pulls the LLaMA2 model if not already downloaded.
# 4. Initializes the appointments database if needed.
# 5. Starts the Athena Assistant backend.

from pathlib import Path

# Define the start_all.sh content

echo "🚀 Starting Athena Assistant Environment..."

# 1. Start Docker Compose (LLaMA server)
echo "🐳 Starting LLaMA Docker container..."
docker-compose up -d llama

# 2. Activate virtual environment
echo "🐍 Activating virtual environment..."
source venv/bin/activate

# 3. Pull model if it's not already downloaded (optional)
if ! docker exec ollama ollama list | grep -q "llama2"; then
  echo "⬇️  Pulling LLaMA2 model into Docker container..."
  docker exec -it ollama ollama pull llama2
fi


# 4. Initialize the appointments database if needed
echo "🗃️  Initializing appointments database (if missing)..."
python3 -c 'from assistant_core.modules.appointments.domain import init_db; init_db()'


# 5. Confirm ready
echo "✅ Athena environment is ready to go!"
#python3 -i -c 'from assistant_core.modules.nlu.nlu_pipeline import process_user_input; print("✅ Assistant is ready!")'
#python run_assistant.py

echo "🧠 Launching Athena Assistant Backend..."
python3 -c "from assistant_core.modules.nlu.nlu_pipeline import process_user_input; print('✅ Assistant backend ready!')"

echo "🖥️ Starting Athena UI..."

UI_DIR="./ui"
if [ -d "$UI_DIR" ]; then
  cd "$UI_DIR"
  echo "▶ Starting Vite dev server in background..."
  npm run dev &
  sleep 3
  echo "▶ Launching Electron app..."
  npx electron electron/main.ts
else
  echo "❌ UI directory not found: $UI_DIR"
  exit 1
fi

# Write the script to scripts/start_all.sh
#script_path = Path("scripts/start_all.sh")
#script_path.parent.mkdir(parents=True, exist_ok=True)
#script_path.write_text(script_content)

# Make it executable
#script_path.chmod(0o755)

#script_path

