# Self-Hosted Open WebUI Stack

A complete self-hosted AI chat interface with integrated search capabilities and web scraping functionality.

![Project Screenshot](screenshot.png)

## What This Stack Includes

- **[Open WebUI](https://github.com/open-webui/open-webui)** <img src="https://raw.githubusercontent.com/open-webui/open-webui/main/static/favicon.png" width="20" height="20" alt="Open WebUI" style="vertical-align: middle;">: AI chat interface accessible at http://localhost:3000
- **[SearXNG](https://github.com/searxng/searxng)** <img src="https://raw.githubusercontent.com/searxng/searxng/master/searx/static/themes/simple/img/searxng.svg" width="20" height="20" alt="SearXNG" style="vertical-align: middle;">: Private search engine for web search functionality
- **[Firecrawl](https://github.com/mendableai/firecrawl)** <img src="https://avatars.githubusercontent.com/u/150964962?s=200&v=4" width="20" height="20" alt="Firecrawl" style="vertical-align: middle;">: Custom web scraping service for content extraction

## Required User Configuration

Before deploying this stack, you **MUST** update the following values:

### 🔑 Security Keys (REQUIRED)
```yaml
# In docker-compose.yml
WEBUI_SECRET_KEY: "your-secret-key-change-this"          # Change this to a strong random string
SEARXNG_SECRET: "your-searxng-secret-key-change-this"   # Change this to a strong random string
```

### 🤖 Ollama Configuration (REQUIRED)
```yaml
# In docker-compose.yml
OLLAMA_BASE_URL: "http://localhost:11434"              # Update to your Ollama server IP/hostname
```

### 🔧 Optional Configuration

#### Firecrawl API Key
```yaml
FIRECRAWL_API_KEY: ""                                    # Leave empty for local firecrawl service
```

#### Search Configuration
```yaml
RAG_WEB_SEARCH_DOMAIN_FILTER_ENABLED: false             # Set to true to enable domain filtering
DEFAULT_USER_ROLE: "user"                               # Change to "admin" if needed
```

## Quick Start

1. **Update Configuration**
   - Edit `docker-compose.yml` with your specific values (see above)
   - Ensure your Ollama server is running and accessible

2. **Deploy the Stack**
   ```bash
   docker-compose up -d
   ```

3. **Access Services**
   - Open WebUI: http://localhost:3000
   - SearXNG: http://localhost:8080
   - Firecrawl API: http://localhost:3002

4. **First Time Setup**
   - Open http://localhost:3000 in your browser
   - Create your admin account (first user becomes admin)
   - Configure your preferred AI models in the settings

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `WEBUI_SECRET_KEY` | `your-secret-key-change-this` | **REQUIRED**: Secret key for Open WebUI session encryption |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | **REQUIRED**: URL to your Ollama API server |
| `SEARXNG_SECRET` | `your-searxng-secret-key-change-this` | **REQUIRED**: Secret key for SearXNG |
| `SEARXNG_BASE_URL` | `http://searxng:8080` | Internal URL for SearXNG service |
| `FIRECRAWL_BASE_URL` | `http://firecrawl:3002` | Internal URL for Firecrawl service |
| `FIRECRAWL_API_KEY` | `""` | API key for Firecrawl (empty for local service) |
| `ENABLE_RAG_WEB_SEARCH` | `true` | Enable web search in RAG |
| `ENABLE_WEB_SEARCH` | `true` | Enable general web search |
| `WEB_SEARCH_ENGINE` | `searxng` | Search engine to use |
| `DEFAULT_USER_ROLE` | `user` | Default role for new users |

## Troubleshooting

### Common Issues

1. **Can't connect to Ollama**
   - Verify `OLLAMA_BASE_URL` points to your running Ollama instance
   - Ensure Ollama is accessible from Docker containers

2. **Search not working**
   - Check that SearXNG container is healthy: `docker-compose logs searxng`
   - Verify search is enabled in Open WebUI settings

3. **Web scraping not working**
   - Check Firecrawl container logs: `docker-compose logs firecrawl`
   - Ensure target websites allow scraping

### Reset Everything
```bash
./docker-reset.sh  # Stops containers and removes volumes
```

## Security Notes

- Change all default secret keys before deployment
- Consider using environment files (.env) for sensitive configuration
- Regularly update container images for security patches
- Monitor logs for unusual activity

## Next Steps

After deployment:
1. Log into Open WebUI at http://localhost:3000
2. Configure your AI models in Settings → Models
3. Test web search functionality
4. Explore RAG capabilities with document uploads