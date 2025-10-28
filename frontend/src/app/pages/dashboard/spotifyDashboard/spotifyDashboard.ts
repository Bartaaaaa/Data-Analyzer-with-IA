import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { SpotifyService } from '../../../services/spotifyService';
import { topArtistsResponse } from '../../../models/spotify/topArtistsResponse';
@Component({
  selector: 'app-register',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './spotifyDashboard.html',
  styleUrls: ['./spotifyDashboard.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SpotifyDashboard {
  private fb = inject(FormBuilder);
  private router = inject(Router);
  private route = inject(ActivatedRoute);
  private spotifyService = inject(SpotifyService);

  loading = signal(false);
  error = signal<string | null>(null);
  topArtists = signal<topArtistsResponse | null>(null);
  isSpotifyConnected = false;
  spotifyToken = signal<string | null>(null);
  ngOnInit() {
    this.spotifyService.getTopArtists().subscribe({
      next: (response) => {
        this.topArtists.set(response);
        console.log(response);
      },
    });
  }
}
