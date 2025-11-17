import {
  ChangeDetectionStrategy,
  ChangeDetectorRef,
  Component,
  effect,
  inject,
  signal,
} from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { SpotifyService } from '../../../services/spotifyService';
import { topArtistsResponse } from '../../../models/spotify/topArtistsResponse';
import Chart from 'chart.js/auto';
import autocolors from 'chartjs-plugin-autocolors';
import { topTracksResponse } from '../../../models/spotify/topTracksResponse';
import { currentTrackResponse } from '../../../models/spotify/currentTrackResponse';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './spotifyDashboard.html',
  styleUrls: [
    './scss/spotifyDashboard.scss',
    './scss/spotifyPlayer.scss',
    './scss/spotifyAlbums.scss',
  ],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SpotifyDashboard {
  private spotifyService = inject(SpotifyService);
  private cdr = inject(ChangeDetectorRef);

  loading = signal(false);
  loadingButton = signal(false);
  isLoading = signal(false);

  error = signal<string | null>(null);
  topArtists = signal<topArtistsResponse | null>(null);
  topTracks = signal<topTracksResponse | null>(null);
  topAlbums = signal<topTracksResponse | null>(null);
  currentTrack = signal<currentTrackResponse | null>(null);
  filter = signal<string>('long_term');
  isSpotifyConnected = false;
  spotifyToken = signal<string | null>(null);

  artistsLoaded = signal(false);
  tracksLoaded = signal(false);
  albumsLoaded = signal(false);

  constructor() {
    effect(() => {
      if (this.artistsLoaded() && this.tracksLoaded() && this.albumsLoaded()) {
        this.isLoading.set(false);
        this.updateGenreChart();
      }
    });
  }

  ngOnInit() {
    this.updateFilter(this.filter());
    this.getCurrentTrack();
    setInterval(() => {
      this.getCurrentTrack();
    }, 30000);
  }

  updateFilter(filter: string) {
    this.filter.set(filter);
    this.isLoading.set(true);
    this.artistsLoaded.set(false);
    this.tracksLoaded.set(false);
    this.albumsLoaded.set(false);
    this.loadTopArtists(filter);
    this.loadTopTracks(filter);
    this.loadTopAlbums(filter);
  }

  loadTopArtists(filter: string) {
    this.spotifyService.getTopArtists(filter, 5).subscribe({
      next: (response) => {
        this.topArtists.set(response);
        this.topArtists()!.top_artists.forEach((artist) => {
          artist.genres = artist.genres.map(this.capitalizeFirstLetter);
        });
        this.artistsLoaded.set(true);
      },
      error: () => this.artistsLoaded.set(true),
    });
  }

  loadTopTracks(filter: string) {
    this.spotifyService.getTopTracks(filter, 5, 10).subscribe({
      next: (response) => {
        this.topTracks.set(response);
        this.tracksLoaded.set(true);
      },
      error: () => this.tracksLoaded.set(true),
    });
  }

  loadTopAlbums(filter: string) {
    this.spotifyService.getTopTracks(filter, 50).subscribe({
      next: (response) => {
        const seenAlbums = new Set<string>();
        const uniqueTracks = response.top_tracks.filter((track) => {
          if (seenAlbums.has(track.album_id) || track.album_type !== 'album') return false;
          seenAlbums.add(track.album_id);
          return true;
        });
        this.topAlbums.set({ top_tracks: uniqueTracks.slice(0, 16) });
        this.albumsLoaded.set(true);
      },
      error: () => this.albumsLoaded.set(true),
    });
  }

  // DOUGHNUT CODE :
  chart: Chart | null = null;
  updateGenreChart() {
    if (!this.topArtists) return;
    const genreCount: Record<string, number> = {};
    var genreRealSize = 0;

    this.topArtists()!.top_artists.forEach((artist) => {
      artist.genres.forEach((genre) => {
        genreCount[genre] = (genreCount[genre] || 0) + 1;
        genreRealSize += 1;
      });
    });

    const data = Object.values(genreCount);
    const canvas = document.getElementById('genreDonut') as HTMLCanvasElement;
    const labels = Object.keys(genreCount);

    if (this.chart) {
      this.chart.data.labels = labels;
      this.chart.data.datasets[0].data = data;
      this.chart.update();
      return;
    }
    this.chart = new Chart(canvas, {
      type: 'doughnut',
      data: {
        labels: Object.keys(genreCount),
        datasets: [
          {
            data: data,
            borderWidth: 0,
            hoverOffset: 20,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '73%',
        animation: {
          animateScale: true,
          animateRotate: true,
        },
        plugins: {
          tooltip: {
            enabled: false,
          },
          legend: {
            display: false,
          },
        },
        layout: {
          padding: {
            top: 10,
            bottom: 10,
            left: 10,
            right: 10,
          },
        },
      },

      plugins: [
        {
          id: 'centerText',
          beforeDraw(chart) {
            const { ctx, chartArea } = chart;
            const centerX = (chartArea.left + chartArea.right) / 2;
            const centerY = (chartArea.top + chartArea.bottom) / 2;

            ctx.save();
            ctx.font = 'bold 1rem Arial';
            ctx.fillStyle = '#000';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';

            const active = chart.getActiveElements();
            let text = '';
            if (active.length > 0) {
              const index = active[0].index;
              const label = chart.data.labels![index];
              const value = Math.floor((chart.data.datasets[0].data[index] / genreRealSize) * 100);
              text = `${label} : ${value}%`;
            }

            ctx.fillText(text, centerX, centerY);
            ctx.restore();
          },
        },
      ],
    });

    Chart.register(autocolors);
  }

  capitalizeFirstLetter(val: string): string {
    return String(val).charAt(0).toUpperCase() + String(val).slice(1);
  }

  // Spotify Player
  temp = {
    name: 'You are currently not listening to any track',
    artists: ['Artist'],
    image: 'test',
    track_url: 'temp',
    progress: 0,
    album_name: 'Album name',
    duration: 0,
    timestamp: 0,
  };
  isPlaying = true;

  progressInterval: any;
  displayProgress = '0:00';
  displayDuration = '0:00';
  currentProgressMs = 0;
  currentDurationMs = 0;

  getCurrentTrack() {
    this.spotifyService.getCurrentTrack().subscribe({
      next: (response) => {
        if (response.image === 'image_url') {
          response.image = 'assets/img/album_placeholder.png';
        }
        this.currentTrack.set(response);
        // Réinitialiser les valeurs
        this.currentProgressMs = response.progress || 0;
        this.currentDurationMs = response.duration || 0;
        this.displayProgress = this.formatTime(this.currentProgressMs);
        this.displayDuration = this.formatTime(this.currentDurationMs);

        // Lancer l'animation locale
        this.startProgressUpdater();
      },
      error: (err) => {
        console.error('Erreur lors de la récupération du morceau', err);
      },
    });
  }
  startProgressUpdater() {
    if (this.progressInterval) {
      clearInterval(this.progressInterval);
      this.progressInterval = null;
    }

    this.progressInterval = setInterval(() => {
      if (!this.currentTrack()) return;

      if (this.currentProgressMs < this.currentDurationMs) {
        this.currentProgressMs += 1000;
        this.displayProgress = this.formatTime(this.currentProgressMs);
        this.cdr.markForCheck();
      } else {
        clearInterval(this.progressInterval);
      }
    }, 1000);
  }

  skipPreviousTrack() {
    this.spotifyService.skipPreviousTrack().subscribe({
      next: () => {
        this.getCurrentTrack();
      },
    });
  }

  skipNextTrack() {
    this.spotifyService.skipNextTrack().subscribe({
      next: () => {
        this.getCurrentTrack();
      },
    });
  }

  get progressPercent(): number {
    if (!this.currentDurationMs) return 0;
    return (this.currentProgressMs / this.currentDurationMs) * 100;
  }

  formatTime(ms: number): string {
    const minutes = Math.floor(ms / 60000);
    const seconds = Math.floor((ms % 60000) / 1000);
    return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
  }
}
