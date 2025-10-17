import { Component, signal, inject } from '@angular/core';
import { Router, RouterOutlet, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';
import { AppHeader } from './pages/header/header';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, AppHeader, CommonModule],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  private router = inject(Router);

  // Afficher le header en fonction des routes
  currentUrl = signal<string>('');
  hiddenRoutes = ['/login', '/register'];
  constructor() {
    this.router.events
      .pipe(filter((e): e is NavigationEnd => e instanceof NavigationEnd))
      .subscribe((event) => {
        this.currentUrl.set(event.urlAfterRedirects.replace(/\/$/, ''));
      });
  }
  showHeader(): boolean {
    return !this.hiddenRoutes.includes(this.currentUrl());
  }
}
