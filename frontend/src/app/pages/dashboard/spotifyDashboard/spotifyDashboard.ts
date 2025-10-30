import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { SpotifyService } from '../../../services/spotifyService';
import { topArtistsResponse } from '../../../models/spotify/topArtistsResponse';
import Chart from 'chart.js/auto';
import { Colors, Tooltip } from 'chart.js';
import autocolors from 'chartjs-plugin-autocolors';
import { topTracksResponse } from '../../../models/spotify/topTracksResponse';
@Component({
  selector: 'app-register',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './spotifyDashboard.html',
  styleUrls: ['./spotifyDashboard.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SpotifyDashboard {
  private spotifyService = inject(SpotifyService);

  loading = signal(false);
  error = signal<string | null>(null);
  topArtists = signal<topArtistsResponse | null>(null);
  topTracks = signal<topTracksResponse | null>(null);
  topAlbums = signal<topTracksResponse | null>(null);
  isSpotifyConnected = false;
  spotifyToken = signal<string | null>(null);
  ngOnInit() {
    this.spotifyService.getTopArtists().subscribe({
      next: (response) => {
        this.topArtists.set(response);
        this.topArtists()!.top_artists.forEach((artist) => {
          artist.genres = artist.genres.map((genre) => {
            return this.capitalizeFirstLetter(genre);
          });
        });
        this.updateGenreChart();
      },
    });

    this.spotifyService.getTopTracks(10, 'medium_term', 10).subscribe({
      next: (response) => {
        this.topTracks.set(response);
      },
    });

    // Récupérer 16 albums différents :
    this.spotifyService.getTopTracks(50).subscribe({
      next: (response) => {
        console.log(response);
        const seenAlbums = new Set<string>();
        const uniqueTracks = response.top_tracks.filter((track) => {
          if (seenAlbums.has(track.album_id) || track.album_type !== 'album') {
            return false;
          }
          seenAlbums.add(track.album_id);
          return true;
        });
        this.topAlbums.set({ top_tracks: uniqueTracks.slice(0, 16) });
      },
    });
  }

  // DOUGHNUT CODE :

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

    new Chart(canvas, {
      type: 'doughnut',
      data: {
        labels: Object.keys(genreCount), // Assure-toi que les labels sont définis
        datasets: [
          {
            data: data,
            borderWidth: 0,
            hoverOffset: 20,
          },
        ],
      },
      options: {
        cutout: '60%',
        animation: {
          animateScale: true,
          animateRotate: true,
        },
        plugins: {
          tooltip: {
            enabled: false,
          },
          legend: {
            position: 'bottom',
            align: 'center',
            fullSize: true,
            labels: {
              usePointStyle: true,
              pointStyle: 'circle',
              boxWidth: 12,
              padding: 20,
              font: {
                size: 14,
                family: 'Inter, Arial, sans-serif',
                weight: 'bold',
              },
              color: '#333',
            },
          },
        },
        layout: {
          padding: {
            top: 20,
            bottom: 10,
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
}
