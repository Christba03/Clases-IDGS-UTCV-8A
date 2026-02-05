# SitioEstructura

This project was generated using [Angular CLI](https://github.com/angular/angular-cli) version 19.1.7.

## Development server

To start a local development server, run:

```bash
ng serve
```

Once the server is running, open your browser and navigate to `http://localhost:4200/`. The application will automatically reload whenever you modify any of the source files.

## Code scaffolding

Angular CLI includes powerful code scaffolding tools. To generate a new component, run:

```bash
ng generate component component-name
```

For a complete list of available schematics (such as `components`, `directives`, or `pipes`), run:

```bash
ng generate --help
```

## Building

To build the project run:

```bash
ng build
```

This will compile your project and store the build artifacts in the `dist/` directory. By default, the production build optimizes your application for performance and speed.

## Running unit tests

To execute unit tests with the [Karma](https://karma-runner.github.io) test runner, use the following command:

```bash
ng test
```

## Running end-to-end tests

For end-to-end (e2e) testing, run:

```bash
ng e2e
```

Angular CLI does not come with an end-to-end testing framework by default. You can choose one that suits your needs.

## Deployment to GitHub Pages

This project is configured for deployment to GitHub Pages.

### Prerequisites

1. Make sure your repository is initialized with git:
   ```bash
   git init
   git remote add origin https://github.com/christba03/your-repo-name.git
   ```

2. Ensure you have committed your changes:
   ```bash
   git add .
   git commit -m "Initial commit"
   ```

### Deploy to GitHub Pages

To deploy your application to GitHub Pages, run:

```bash
npm run deploy:gh-pages
```

This command will:
1. Build your application for production with the correct baseHref
2. Deploy the built files to the `gh-pages` branch of your repository

### First-time Deployment

On the first deployment, you may be prompted to:
- Enter your GitHub username
- Enter your GitHub password (or use a personal access token)

**Note:** If you're using two-factor authentication, you'll need to create a [Personal Access Token](https://github.com/settings/tokens) and use it instead of your password.

### After Deployment

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Pages**
3. Under "Source", select the `gh-pages` branch and `/ (root)` folder
4. Your site will be available at `https://christba03.github.io/your-repo-name/` (or `https://christba03.github.io/` if it's your main repository)

### Updating Your Site

To update your deployed site, simply run the deployment command again:

```bash
npm run deploy:gh-pages
```

### Custom Base Path

If you need to deploy to a subdirectory (e.g., `https://christba03.github.io/sitio-estructura-busqueda/`), update the `baseHref` in `angular.json`:

```json
"baseHref": "/sitio-estructura-busqueda/"
```

And update the deployment script in `package.json` accordingly.

## Additional Resources

For more information on using the Angular CLI, including detailed command references, visit the [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli) page.
