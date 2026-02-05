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

This project is configured for automatic deployment to GitHub Pages using GitHub Actions.

### Automatic Deployment (Recommended)

The project includes a GitHub Actions workflow (`.github/workflows/deploy-angular-gh-pages.yml`) that automatically builds and deploys your site whenever you push to the `main` branch.

**Setup:**
1. Go to your repository on GitHub
2. Navigate to **Settings** → **Pages**
3. Under "Source", select **GitHub Actions** (not "Deploy from a branch")
4. Save the settings

**How it works:**
- Every time you push changes to the `main` branch in the `sitio-estructura-busqueda` folder, the workflow will:
  1. Install dependencies
  2. Build your Angular app for production
  3. Deploy it to GitHub Pages automatically

**View deployments:**
- Go to the **Actions** tab in your repository to see deployment status
- Your site will be available at `https://christba03.github.io/Clases-IDGS-UTCV-8A/`

### Manual Deployment (Alternative)

If you prefer to deploy manually, you can use:

```bash
npm run deploy:gh-pages
```

This command will:
1. Build your application for production with the correct baseHref
2. Deploy the built files to the `gh-pages` branch of your repository

**Note:** For manual deployment, you'll need to configure GitHub Pages to use the `gh-pages` branch in Settings → Pages.

### Custom Base Path

If you need to deploy to a different subdirectory, update the `baseHref` in `angular.json`:

```json
"baseHref": "/your-custom-path/"
```

And update the deployment script in `package.json` accordingly.

## Additional Resources

For more information on using the Angular CLI, including detailed command references, visit the [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli) page.
