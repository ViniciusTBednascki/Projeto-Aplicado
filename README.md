# Real Estate Data Engineering

A Python-based data enginnering project that collects real estate property listings from Brazilian websites and stores them in a database.

## Overview

This project scrapes property listings (apartments and houses) from popular Brazilian real estate websites, specifically targeting properties in Curitiba, Paraná. The scraped data includes property details such as price, location, size, number of rooms, and descriptions.

## Features

- **Multi-source scraping**: Collects data from Viva Real and Imovel Web
- **Property types**: Supports apartments and houses
- **Location focus**: Currently configured for Curitiba, Paraná, Brazil
- **Database storage**: MongoDB integration with PostgreSQL support (placeholder)
- **Browser automation**: Uses Pyppeteer for headless Chrome automation
- **Data export**: Can save scraped data to JSON files
- **Docker support**: Database containers for easy setup

## Project Structure

```
├── main.py                 # Main entry point for scraping
├── teste.py               # Test script for data insertion
├── imoveis.json           # Sample scraped data (JSON format)
├── Scrapers/              # Web scraping modules
│   ├── main.py           # Orchestrates scraping from multiple sources
│   ├── viva_real.py      # Viva Real scraper
│   ├── imovel_web.py     # Imovel Web scraper
│   └── browser.py        # Browser automation setup
└── databases/            # Database controllers and configurations
    ├── mongodb/
    │   ├── controller.py     # MongoDB operations
    │   └── docker-compose.yaml
    └── postgresql/
        ├── controller.py     # PostgreSQL operations (placeholder)
        └── docker-compose.yaml
```

## Prerequisites

- Python 3.8+
- Google Chrome browser
- Docker (for database containers)
- MongoDB (via Docker or local installation)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Install Python dependencies**:
   ```bash
   pip install pymongo pyppeteer
   ```

3. **Set up databases** (optional, for full functionality):
   ```bash
   # MongoDB
   cd databases/mongodb
   docker-compose up -d

   # PostgreSQL (if implementing)
   cd ../postgresql
   docker-compose up -d
   ```

## Usage

### Running the Scraper

Execute the main scraping script:

```bash
python main.py
```

This will:
1. Launch a headless Chrome browser
2. Scrape property listings from configured websites
3. Store the data in MongoDB
4. Display scraping progress and results

### Data Structure

Each scraped property contains:

```json
{
  "link": "https://...",
  "tipo": "Apartamento",
  "estado": "PR",
  "cidade": "Curitiba",
  "bairro": "Centro",
  "rua": "Rua Example",
  "area": "55",
  "quartos": "2",
  "banheiros": "1",
  "vagas": "1",
  "preco": "R$ 340.000",
  "descricao": "Property description..."
}
```

### Alternative Data Export

To save data to JSON instead of MongoDB, modify `main.py`:

```python
# Comment out MongoDB save
# save_in_mongodb(data)

# Uncomment JSON save
save_in_json(data)
```

## Configuration

### Scraping Parameters

Edit the scraper files to modify:

- **Cities**: Update `CIDADES` list in scraper files
- **Property types**: Modify `TIPOS` and corresponding URLs
- **Max pages**: Change `MAX_PAGES` for pagination limits
- **Browser settings**: Adjust `browser.py` for different Chrome configurations

### Database Configuration

- **MongoDB**: Default connection is `mongodb://localhost:27017/`
- **Database name**: Default is `"bronze"`
- **Collection**: Configured as `"imoveis"`

Set environment variable for custom MongoDB URI:
```bash
export MONGO_URI="your-connection-string"
```

## Dependencies

- **pymongo**: MongoDB driver for Python
- **pyppeteer**: Python port of Puppeteer for browser automation

## Browser Setup

The project uses Pyppeteer with a local Chrome installation. Update `CHROME_PATH` in `browser.py` if your Chrome executable is in a different location.

## Database Operations

### MongoDB Controller Features

- Bulk insert operations for large datasets
- Single document insertion
- Query operations with optional limits
- Connection management

### PostgreSQL

PostgreSQL controller is prepared but not implemented. The structure is ready for SQL-based storage if needed.

## Docker Support

Database containers are configured for easy setup:

```bash
# Start MongoDB
docker-compose -f databases/mongodb/docker-compose.yaml up -d

# Start PostgreSQL
docker-compose -f databases/postgresql/docker-compose.yaml up -d
```

## Error Handling

The scraper includes error handling for:
- Network issues during scraping
- Database connection problems
- Browser automation failures
- Data parsing errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Disclaimer

This project is for educational purposes. Ensure compliance with website terms of service and robots.txt files when scraping. Respect rate limits and implement appropriate delays between requests.
