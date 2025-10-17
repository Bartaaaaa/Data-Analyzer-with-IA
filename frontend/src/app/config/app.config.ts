import {
  ApplicationConfig,
  provideBrowserGlobalErrorListeners,
  provideZoneChangeDetection,
} from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { routes } from '../app.routes';
import { APP_CONFIG, AppConfig } from './appConfigToken';
const appConfigValues: AppConfig = {
  apiBaseUrl: 'http://localhost:8000/api',
};
export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(), //loguer les erreurs dans la console
    provideZoneChangeDetection({ eventCoalescing: true }), //détection de changement
    provideRouter(routes), //active le service de routage
    provideHttpClient(), // permettre requete http
    { provide: APP_CONFIG, useValue: appConfigValues }, //Enregistrer apibaseUrl dans l'application
  ],
};
