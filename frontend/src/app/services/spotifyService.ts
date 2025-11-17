import { inject, Injectable, signal } from '@angular/core';
import { Observable } from 'rxjs';
import { API_BASE_URL } from '../config/apiBaseUrlToken';
import { API_ROUTES } from '../utils/apiRoutes';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { topArtistsResponse } from '../models/spotify/topArtistsResponse';
import { topTracksResponse } from '../models/spotify/topTracksResponse';
import { currentTrackResponse } from '../models/spotify/currentTrackResponse';
import { checkTokenResponse } from '../models/spotify/checkTokenResponse';
@Injectable({ providedIn: 'root' })
export class SpotifyService {
  private http = inject(HttpClient);
  private apiBase = inject(API_BASE_URL);

  login() {
    const token = localStorage.getItem('access_token');
    window.location.href = `${this.apiBase}${API_ROUTES.connections.spotifyConnection}?jwt=${token}`;
  }

  checkToken(): Observable<checkTokenResponse> {
    return this.http.get<checkTokenResponse>(
      `${this.apiBase}${API_ROUTES.connections.checkSpotifyConnection}`
    );
  }

  private getHeaders(token: string) {
    return new HttpHeaders({
      Authorization: `Bearer ${token}`,
    });
  }

  // DATA API

  getTopArtists(timeRange = 'short_term', limit = 10): Observable<topArtistsResponse> {
    return this.http.get<topArtistsResponse>(
      `${this.apiBase}${API_ROUTES.spotify.topArtists}?limit=${limit}&time_range=${timeRange}`,
      {}
    );
  }
  getTopTracks(timeRange = 'short_term', limit = 10, offset = 0): Observable<topTracksResponse> {
    return this.http.get<topTracksResponse>(
      `${this.apiBase}${API_ROUTES.spotify.topTracks}?limit=${limit}&time_range=${timeRange}&offset=${offset}`,
      {}
    );
  }

  getCurrentTrack(): Observable<currentTrackResponse> {
    return this.http.get<currentTrackResponse>(`${this.apiBase}${API_ROUTES.spotify.currentTrack}`);
  }

  skipNextTrack(): Observable<void> {
    return this.http.post<void>(`${this.apiBase}${API_ROUTES.spotify.nextTrack}`, null);
  }
  skipPreviousTrack(): Observable<void> {
    return this.http.post<void>(`${this.apiBase}${API_ROUTES.spotify.previousTrack}`, null);
  }
}
