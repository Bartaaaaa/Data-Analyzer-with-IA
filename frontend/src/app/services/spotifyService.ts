import { inject, Injectable, signal } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, map, Observable, tap, throwError } from 'rxjs';
import { API_BASE_URL } from '../config/apiBaseUrlToken';
import { API_ROUTES } from '../utils/apiRoutes';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { topArtistsResponse } from '../models/spotify/topArtistsResponse';
@Injectable({ providedIn: 'root' })
export class SpotifyService {
  private http = inject(HttpClient);
  private apiBase = inject(API_BASE_URL);

  login() {
    const token = localStorage.getItem('access_token');
    window.location.href = `${this.apiBase}${API_ROUTES.connections.spotifyConnection}?jwt=${token}`;
  }

  checkToken() {
    return this.http.get<boolean>(
      `${this.apiBase}${API_ROUTES.connections.checkSpotifyConnection}`
    );
  }

  private getHeaders(token: string) {
    return new HttpHeaders({
      Authorization: `Bearer ${token}`,
    });
  }

  // DATA API

  getTopArtists(): Observable<topArtistsResponse> {
    return this.http.get<topArtistsResponse>(`${this.apiBase}${API_ROUTES.spotify.topArtists}`, {});
  }
}
