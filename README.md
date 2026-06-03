# LMS Agent

A generic Playwright + MCP powered Learning Management System automation framework.

The project is designed to work with multiple LMS platforms including Moodle, Canvas, Blackboard, TalentLMS, Thinkific, Teachable, Coursera Enterprise, and custom LMS implementations through configurable adapters.

## Features

- Automated LMS login
- Course discovery
- Learning content discovery
- Transcript extraction
- AI-ready content summarization
- Progress tracking
- SQLite persistence layer
- Playwright browser automation
- MCP (Model Context Protocol) integration
- Multi-LMS adapter architecture
- Configurable selectors and workflows

## Architecture

```text
lms_agent/
├── adapters/
├── agents/
├── config/
├── database/
├── mcp/
├── playwright/
├── data/
├── requirements.txt
├── .env.example
└── README.md
```

## Supported LMS Platforms

- Moodle
- Canvas
- Blackboard
- TalentLMS
- Thinkific
- Teachable
- Coursera Enterprise
- Custom LMS implementations

## System Requirements

| Component | Version |
|------------|----------|
| Python | 3.11+ |
| Playwright | Latest |
| SQLite | 3.x |
| MCP SDK | Latest |

## Installation

```bash
git clone https://github.com/MMBCoder/lms_agent.git
cd lms_agent
python -m venv venv
```

Activate environment:

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
playwright install
```

## Environment Variables

Create a `.env` file using `.env.example`.

```env
LMS_URL=https://your-lms.com
LMS_USERNAME=username
LMS_PASSWORD=password
HEADLESS=false
DATABASE_PATH=data/lms.db
```

## Configuration

LMS-specific selectors should be configured in:

```text
config/lms_config.yaml
```

Examples include login selectors, course selectors, content selectors, video player selectors, and transcript selectors.

## Running the Application

Initialize database:

```bash
python -c "from database.database import Database; Database().initialize()"
```

Start MCP server:

```bash
python mcp/server.py
```

## MCP Integration

Example MCP configuration:

```json
{
  "mcpServers": {
    "lms-agent": {
      "command": "python",
      "args": ["mcp/server.py"]
    }
  }
}
```

## Use Cases

- Corporate training automation
- Learning analytics
- Course auditing
- Transcript extraction
- Knowledge indexing
- AI-powered note generation
- Compliance training tracking
- Employee onboarding

## Security

- Never commit credentials
- Store secrets in `.env`
- Use encrypted secrets in production
- Rotate credentials regularly

## Roadmap

- Moodle adapter
- Canvas adapter
- Blackboard adapter
- Docker support
- CI/CD pipeline
- LLM-based summarization
- Advanced progress analytics

## Contributing

Contributions are welcome through pull requests and issues.

## License

MIT License
