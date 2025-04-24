# Operations Dashboard Frontend

A modern web application for monitoring and managing system operations, built with Vue.js and Tailwind CSS.

## Features

- **Dashboard**: Monitor system performance and health with real-time metrics
- **Inventory**: Track and manage your server resources across different regions
- **Observability**: Deep insights into metrics, logs, and traces across your infrastructure

## Getting Started

### Prerequisites

- Node.js 16+ and npm

### Installation

```bash
# Install dependencies
npm install
```

### Development

```bash
# Start development server with hot-reload
npm run dev
```

The application will be available at http://localhost:3001

### Building for Production

```bash
# Build optimized files for production
npm run build
```

### Running in Docker

```bash
# Build Docker image
docker build -t operations-dashboard .

# Run container
docker run -p 8080:80 operations-dashboard
```

## Tech Stack

- Vue.js 3 with Composition API
- Vue Router for navigation
- Tailwind CSS for styling
- Chart.js for data visualization
- Axios for API requests 