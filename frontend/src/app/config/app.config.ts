import {
  ApplicationConfig,
  provideBrowserGlobalErrorListeners,
  provideZoneChangeDetection,
} from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { routes } from '../app.routes';
import { APP_CONFIG, AppConfig } from './appConfigToken';
import { AuthInterceptor } from '../pages/auth/httpInterceptor';
const appConfigValues: AppConfig = {
  apiBaseUrl: 'http://localhost:8000/api',
};
export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(), //loguer les erreurs dans la console
    provideZoneChangeDetection({ eventCoalescing: true }), //détection de changement
    provideRouter(routes), //active le service de routage
    provideHttpClient(withInterceptors([AuthInterceptor])), // permettre requete http
    { provide: APP_CONFIG, useValue: appConfigValues }, //Enregistrer apibaseUrl dans l'application
  ],
};
